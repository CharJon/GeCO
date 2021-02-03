import itertools

import pyscipopt as scip
from networkx.utils import py_random_state
from geco.mips.scheduling.generic import *


@py_random_state(-1)
def hooker_params(number_of_facilities, number_of_tasks, seed=0):
    """Generates late tasks mip instance described in section 4 in [1].

    Parameters
    ----------
    number_of_facilities: int
        the number of facilities to schedule on
    number_of_tasks: int
        the number of tasks to assign to facilities
    seed: int, random object or None
        for randomization

    Returns
    -------
    processing_times: dict[int,int]
        time steps to process each task
    capacities: list[int]
        capacity of each facility
    assignment_costs: dict[int,int]
        cost of assigning a task to a facility
    release_times: list[int]
        time step at which a job is released
    deadlines: dict[int, float]
        deadline (time step) to finish a job

    References
    ----------
    .. [1] Hooker, John. (2005). Planning and Scheduling to Minimize
     Tardiness. 314-327. 10.1007/11564751_25.
    """
    return generate_params(number_of_facilities, number_of_tasks, seed)[:-1]


@py_random_state(-1)
def hooker_instance(number_of_facilities, number_of_tasks, time_steps, seed=0):
    """Generates late tasks mip instance described in section 4 in [1].

    Parameters
    ----------
    number_of_facilities: int
        the number of facilities to schedule on
    number_of_tasks: int
        the number of tasks to assign to facilities
    time_steps:
        the number of time steps starting from 0 (corresponds to "N" in the paper)

    Returns
    -------
        model: SCIP model of the late tasks instance

    References
    ----------
    .. [1] Hooker, John. (2005). Planning and Scheduling to Minimize
     Tardiness. 314-327. 10.1007/11564751_25.
    """
    return hooker_formulation(
        number_of_facilities,
        number_of_tasks,
        time_steps,
        *hooker_params(number_of_facilities, number_of_tasks, seed),
        name="Hooker Scheduling Instance",
    )


def hooker_formulation(
    number_of_facilities,
    number_of_tasks,
    time_steps,
    processing_times,
    capacities,
    assignment_costs,
    release_dates,
    deadlines,
    name="Hooker Scheduling Late Tasks Formulation",
):
    """Generates late tasks mip formulation described in section 4 in [1].

    Parameters
    ----------
    number_of_facilities: int
        the number of facilities to schedule on
    number_of_tasks: int
        the number of tasks to assign to facilities
    time_steps:
        the number of time steps starting from 0 (corresponds to "N" in the paper)
    processing_times: dict[int,int]
        time steps to process each task
    capacities: list[int]
        capacity of each facility
    assignment_costs: dict[int,int]
        cost of assigning a task to a facility
    release_dates: list[int]
        time step at which a job is released
    deadlines: dict[int, float]
        deadline (time step) to finish a job
    name: str
        assigned name to generated instance

    Returns
    -------
        model: SCIP model of the late tasks instance

    References
    ----------
    .. [1] Hooker, John. (2005). Planning and Scheduling to Minimize
     Tardiness. 314-327. 10.1007/11564751_25.
    """
    model = scip.Model(name)

    start_time = min(release_dates)
    time_steps = range(start_time, start_time + time_steps)

    # add variables and their cost
    L = []
    for i in range(number_of_tasks):
        var = model.addVar(lb=0, ub=1, obj=1, name=f"L_{i}", vtype="B")
        L.append(var)

    # assignment vars
    x = {}
    for j, i, t in itertools.product(
        range(number_of_tasks), range(number_of_facilities), time_steps
    ):
        var = model.addVar(lb=0, ub=1, obj=0, name=f"x_{j}_{i}_{t}", vtype="B")
        x[j, i, t] = var

    # add constraints
    # constraint (a)
    for j, t in itertools.product(range(number_of_tasks), time_steps):
        model.addCons(
            len(time_steps) * L[j]
            >= scip.quicksum(
                (
                    (t + processing_times[j, i]) * x[j, i, t] - deadlines[j]
                    for i in range(number_of_facilities)
                )
            )
        )

    # constraint (b)
    for j in range(number_of_tasks):
        vars = (
            x[j, i, t]
            for i, t in itertools.product(range(number_of_facilities), time_steps)
        )
        model.addCons(scip.quicksum(vars) == 1)

    # constraint (c)
    for i, t in itertools.product(range(number_of_facilities), time_steps):
        vars = []
        for j in range(number_of_tasks):
            vars += [
                assignment_costs[j, i] * x[j, i, t_prime]
                for t_prime in range(t - processing_times[j, i] + 1, t + 1)
                if (j, i, t_prime) in x
            ]
        model.addCons(scip.quicksum(vars) <= capacities[i])

    # constraint (d)
    for i, j, t in itertools.product(
        range(number_of_facilities), range(number_of_tasks), time_steps
    ):
        if t < release_dates[j] or t > len(time_steps) - processing_times[j, i]:
            model.addCons(x[j, i, t] == 0)

    model.setMinimize()

    return model


def generate_hookers_instances():
    number_of_tasks = [10 + 2 * i for i in range(7)]
    time_steps = [10, 100]
    seeds = range(10)
    for n, t, seed in itertools.product(number_of_tasks, time_steps, seeds):
        params = 3, n, t, seed
        yield params, hooker_instance(*params)
