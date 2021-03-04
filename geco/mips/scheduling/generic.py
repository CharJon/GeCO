import itertools

from networkx.utils import py_random_state
from pyscipopt import scip


def late_tasks_formulation(
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


def heinz_formulation(
    number_of_facilities,
    number_of_tasks,
    processing_times,
    capacities,
    assignment_costs,
    release_dates,
    deadlines,
    resource_requirements,
    name="Heinz Scheduling Formulation",
):
    """Generates scheduling MIP formulation according to Model 4 in [1].

    Parameters
    ----------
    number_of_facilities: int
        the number of facilities to schedule on
    number_of_tasks: int
        the number of tasks to assign to facilities
    processing_times: dict[(int,int),int]
        time steps to process each task
    capacities: list[int]
        capacity of each facility
    assignment_costs: dict[(int,int),int]
        cost of assigning a task to a facility
    release_dates: list[int]
        time step at which a job is released
    deadlines: dict[int, float]
        deadline (time step) to finish a job
    resource_requirements: dict[(int,int),int]
        resources required for each task assigned to a facility
    name: str
        assigned name to generated instance

    Returns
    -------
        model: SCIP model of generated instance

    References
    ----------
    .. [1] Heinz, J. (2013). Recent Improvements Using Constraint Integer Programming for Resource Allocation and Scheduling.
    In Integration of AI and OR Techniques in Constraint Programming for Combinatorial Optimization Problems
    (pp. 12–27). Springer Berlin Heidelberg.
    """
    model = scip.Model(name)

    time_steps = range(min(release_dates), int(max(deadlines)))

    # objective function
    x = {}
    for j, k in itertools.product(range(number_of_tasks), range(number_of_facilities)):
        var = model.addVar(
            lb=0, ub=1, obj=assignment_costs[j, k], name=f"x_{j}_{k}", vtype="B"
        )
        x[j, k] = var

    # y vars
    y = {}
    for j, k, t in itertools.product(
        range(number_of_tasks), range(number_of_facilities), time_steps
    ):
        if release_dates[j] <= t <= deadlines[j] - processing_times[j, k]:
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
                y[j, k, t]
                for t in range(
                    release_dates[j], int(deadlines[j]) - processing_times[j, k]
                )
                if t < len(time_steps)
            )
            == x[j, k]
        )

    # constraint (14)
    for k, t in itertools.product(range(number_of_facilities), time_steps):
        model.addCons(
            scip.quicksum(
                resource_requirements[j, k] * y[j, k, t_prime]
                for j in range(number_of_tasks)
                for t_prime in range(t - processing_times[j, k], t + 1)
                if (j, k, t_prime) in y
            )
            <= capacities[k]
        )

    # constraint (15)
    epsilon = filter(
        lambda ts: ts[0] < ts[1], itertools.product(release_dates, deadlines)
    )
    for k, (t1, t2) in itertools.product(range(number_of_facilities), epsilon):
        model.addCons(
            scip.quicksum(
                processing_times[j, k] * resource_requirements[j, k] * x[j, k]
                for j in range(number_of_tasks)
                if t1 <= release_dates[j] and t2 >= deadlines[j]
            )
            <= capacities[k] * (t2 - t1)
        )

    return model


def hooker_cost_formulation(
    number_of_facilities,
    number_of_tasks,
    processing_times,
    capacities,
    assignment_costs,
    release_dates,
    deadlines,
    resource_requirements,
    name="Hooker Cost Scheduling Formulation",
):
    """Generates scheduling MIP formulation according to [1].

    Parameters
    ----------
    number_of_facilities: int
        the number of facilities to schedule on
    number_of_tasks: int
        the number of tasks to assign to facilities
    processing_times: dict[(int,int),int]
        time steps to process each task
    capacities: list[int]
        capacity of each facility
    assignment_costs: dict[(int,int),int]
        cost of assigning a task to a facility
    release_dates: list[int]
        time step at which a job is released
    deadlines: dict[int, float]
        deadline (time step) to finish a job
    resource_requirements: dict[(int,int),int]
        resources required for each task assigned to a facility
    name: str
        assigned name to generated instance

    Returns
    -------
        model: SCIP model of generated instance

    References
    ----------
    .. [1] J. N. Hooker, A hybrid method for planning and scheduling, CP 2004.
    """
    model = scip.Model(name)

    time_steps = range(min(release_dates), int(max(deadlines)))

    # objective function
    x = {}
    for j, i, t in itertools.product(
        range(number_of_tasks), range(number_of_facilities), time_steps
    ):
        var = model.addVar(
            lb=0, ub=1, obj=assignment_costs[j, i], name=f"x_{j}_{i}_{t}", vtype="B"
        )
        x[j, i, t] = var

    # add constraints
    # constraints (a)
    for j in range(number_of_tasks):
        model.addCons(
            scip.quicksum(
                x[j, i, t]
                for i, t in itertools.product(range(number_of_facilities), time_steps)
            )
            == 1
        )

    # constraints (b)
    for i, t in itertools.product(range(number_of_facilities), time_steps):
        model.addCons(
            scip.quicksum(
                resource_requirements[j, i] * x[j, i, t] for j in range(number_of_tasks)
            )
            <= capacities[i]
        )

    # constraints (c)
    for j, i, t in itertools.product(
        range(number_of_tasks), range(number_of_facilities), time_steps
    ):
        if (
            deadlines[j] - processing_times[j, i] < t < release_dates[j]
            or t > number_of_tasks - processing_times[j, i]
        ):
            model.addCons(x[j, i, t] == 0)

    return model


@py_random_state(-1)
def generate_params(number_of_facilities, number_of_tasks, seed=0):
    """
    Generic instance parameter generator for heinz [1] and hooker [2] formulations.
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
    resource_requirements: dict[int,int]
        resources required for each task assigned to a facility
    References
    ----------
    .. [1] Heinz, J. (2013). Recent Improvements Using Constraint Integer Programming for Resource Allocation and Scheduling.
    In Integration of AI and OR Techniques in Constraint Programming for Combinatorial Optimization Problems
    (pp. 12–27). Springer Berlin Heidelberg.
    .. [2] Hooker, John. (2005). Planning and Scheduling to Minimize
     Tardiness. 314-327. 10.1007/11564751_25.
    """
    processing_times = {}

    for j, i in itertools.product(range(number_of_tasks), range(number_of_facilities)):
        if number_of_tasks < 22:
            processing_times[j, i] = seed.randint(2, 20 + 5 * i)
        else:
            processing_times[j, i] = seed.randint(5, 20 + 5 * i)

    capacities = [10] * number_of_facilities

    assignment_costs = {}
    for j in range(number_of_tasks):
        value = seed.randint(1, 10)
        for i in range(number_of_facilities):
            assignment_costs[j, i] = value

    release_times = [0] * number_of_tasks

    beta = 20 / 9
    deadlines = [
        seed.uniform(beta * number_of_tasks / 4, beta * number_of_tasks)
        for _ in range(number_of_tasks)
    ]

    resource_requirements = {}
    for j, k in itertools.product(range(number_of_tasks), range(number_of_facilities)):
        resource_requirements[j, k] = seed.randint(1, 9)

    return (
        processing_times,
        capacities,
        assignment_costs,
        release_times,
        deadlines,
        resource_requirements,
    )
