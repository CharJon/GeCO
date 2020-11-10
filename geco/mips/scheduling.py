"""
This module implements the scheduling problem MIP generation techniques from different papers.
"""

import itertools

import pyscipopt as scip
from networkx.utils import py_random_state


def hooker_late_tasks_formulation(
        number_of_facilities,
        number_of_tasks,
        time_steps,
        p,
        C,
        c,
        r,
        d
):
    # TODO: use more expressive param names
    """Generates late tasks mip formulation described in section 4 in
    Hooker, John. (2005). Planning and Scheduling to Minimize Tardiness. 314-327. 10.1007/11564751_25.

    number_of_facilities: the number of facilities to schedule on
    number_of_tasks: the number of tasks to assign to facilities
    time_steps: the number of time steps starting from 0 (corresponds to "N" in the paper)
    Other parameters follow the same naming used in the paper

    Returns:
        model: SCIP model of the late tasks instance
    """
    model = scip.Model("Hooker Scheduling Late Tasks Formulation")
    assert min(r) == 0  # TODO: handle the case that timesteps don't start at 0

    # add variables and their cost
    L = []
    for i in range(number_of_tasks):
        var = model.addVar(lb=0, ub=1, obj=1, name=f"L_{i}", vtype="B")
        L.append(var)

    # assignment vars
    x = {}
    for j, i, t in itertools.product(
            range(number_of_tasks), range(number_of_facilities), range(time_steps)
    ):
        var = model.addVar(lb=0, ub=1, obj=0, name=f"x_{j}_{i}_{t}", vtype="B")
        x[j, i, t] = var

    # add constraints
    # constraint (a)
    for j, t in itertools.product(range(number_of_tasks), range(time_steps)):
        model.addCons(
            time_steps * L[j]
            >= scip.quicksum(
                ((t + p[j, i]) * x[j, i, t] - d[j] for i in range(number_of_facilities))
            )
        )

    # constraint (b)
    for j in range(number_of_tasks):
        vars = (
            x[j, i, t]
            for i, t in itertools.product(
            range(number_of_facilities), range(time_steps)
        )
        )
        model.addCons(scip.quicksum(vars) == 1)

    # constraint (c)
    for i, t in itertools.product(range(number_of_facilities), range(time_steps)):
        vars = []
        for j in range(number_of_tasks):
            vars += [
                c[j, i] * x[j, i, t_prime]
                for t_prime in range(t - p[j, i] + 1, t + 1)
                if (j, i, t_prime) in x
            ]
        model.addCons(scip.quicksum(vars) <= C[i])

    # constraint (d)
    for i, j, t in itertools.product(
            range(number_of_facilities), range(number_of_tasks), range(time_steps)
    ):
        if t < r[j] or t > time_steps - p[j, i]:
            model.addCons(x[j, i, t] == 0)

    model.setMinimize()

    return model


def generate_hookers_instances():
    number_of_tasks = [10 + 2 * i for i in range(7)]
    time_steps = [10, 100]
    seeds = range(10)
    for n, t, seed in itertools.product(number_of_tasks, time_steps, seeds):
        params = 3, n, t, seed
        yield params, hooker_late_tasks_formulation(
            *params[:-1], *generate_params(*params[:-1])[:-1], seed=seed
        )


@py_random_state(2)
def generate_params(number_of_facilities, number_of_tasks, seed=0):
    p = {}

    for j, i in itertools.product(range(number_of_tasks), range(number_of_facilities)):
        if number_of_tasks < 22:
            p[j, i] = seed.randint(2, 20 + 5 * i)
        else:
            p[j, i] = seed.randint(5, 20 + 5 * i)

    C = [10] * number_of_facilities

    c = {}
    for i in range(number_of_facilities):
        value = seed.randint(1, 10)
        for j in range(number_of_tasks):
            c[j, i] = value

    R = [0] * number_of_tasks

    d = {}
    beta = 20 / 9
    for j in range(number_of_tasks):
        d[j] = seed.uniform(beta * number_of_tasks / 4, beta * number_of_tasks)

    r = {}
    for j, k in itertools.product(range(number_of_tasks), range(number_of_facilities)):
        r[j, k] = seed.randint(1, 9)

    return p, C, c, R, d, r


def heinz_formulation(
        number_of_facilities,
        number_of_tasks,
        p,
        C,
        c,
        R,
        d,
        r
):
    """Generates mip formulation according to Model 4 in
    # TODO: Add paper reference

    number_of_facilities: the number of facilities to schedule on
    number_of_tasks: the number of tasks to assign to facilities
    time_steps: the number of time steps starting from 0 (corresponds to "N" in the paper)

    Returns:
        model: SCIP model of the late tasks instance
    """
    model = scip.Model("Heinz Scheduling")
    time_steps = range(min(R), int(max(d.values())))

    # objective function
    x = {}
    for j, k in itertools.product(range(number_of_tasks), range(number_of_facilities)):
        var = model.addVar(lb=0, ub=1, obj=c[j, k], name=f"x_{j}_{k}", vtype="B")
        x[j, k] = var

    # y vars
    y = {}
    for j, k, t in itertools.product(
            range(number_of_tasks), range(number_of_facilities), time_steps
    ):
        if R[j] <= t <= d[j] - p[j, k]:
            var = model.addVar(lb=0, ub=1, obj=0, name=f"y_{j}_{k}_{t}", vtype="B")
            y[j, k, t] = var

    # add constraints
    # constraint (12)
    for j in range(number_of_tasks):
        model.addCons(scip.quicksum(x[j, k] for k in range(number_of_facilities)) == 1)

    # constraint (13)
    for j, k in itertools.product(range(number_of_tasks), range(number_of_facilities)):
        model.addCons(
            scip.quicksum(
                y[j, k, t] for t in range(R[j], int(d[j]) - p[j, k]) if t < len(time_steps)
            )
            == x[j, k]
        )

    # constraint (14)
    for k, t in itertools.product(range(number_of_facilities), time_steps):
        model.addCons(
            scip.quicksum(
                r[j, k] * y[j, k, t_prime]
                for j in range(number_of_tasks)
                for t_prime in range(t - p[j, k], t + 1)
                if (j, k, t_prime) in y
            )
            <= C[k]
        )

    # constraint (15)
    epsilon = filter(lambda ts: ts[0] < ts[1], itertools.product(R, d.values()))
    for k, (t1, t2) in itertools.product(range(number_of_facilities), epsilon):
        model.addCons(
            scip.quicksum(
                p[j, k] * r[j, k] * x[j, k]
                for j in range(number_of_tasks)
                if t1 <= R[j] and t2 >= d[j]
            )
            <= C[k] * (t2 - t1)
        )

    return model
