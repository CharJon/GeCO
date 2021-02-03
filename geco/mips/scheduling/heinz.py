import itertools

import pyscipopt as scip
from networkx.utils import py_random_state
from geco.mips.scheduling.generic import *


@py_random_state(-1)
def heinz_params(number_of_facilities, number_of_tasks, seed=0):
    """Generates scheduling MIP instance params according to [1].

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
    """
    return generate_params(number_of_facilities, number_of_tasks, seed)


@py_random_state(-1)
def heinz_instance(number_of_facilities, number_of_tasks, seed=0):
    """Generates scheduling MIP instance according to [1].

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
        model: SCIP model of generated instance

    References
    ----------
    .. [1] Heinz, J. (2013). Recent Improvements Using Constraint Integer Programming for Resource Allocation and Scheduling.
    In Integration of AI and OR Techniques in Constraint Programming for Combinatorial Optimization Problems
    (pp. 12–27). Springer Berlin Heidelberg.
    """
    return heinz_formulation(
        number_of_facilities,
        number_of_tasks,
        *heinz_params(number_of_facilities, number_of_tasks, seed),
        name="Heinz Scheduling Instance",
    )


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
    resource_requirements: dict[int,int]
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

    time_steps = range(min(release_dates), int(max(deadlines.values())))

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
        lambda ts: ts[0] < ts[1], itertools.product(release_dates, deadlines.values())
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
