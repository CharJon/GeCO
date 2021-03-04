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
    processing_times: dict[(int,int),int]
        time steps to process each task
    capacities: list[int]
        capacity of each facility
    assignment_costs: dict[(int,int),int]
        cost of assigning a task to a facility
    release_times: list[int]
        time step at which a job is released
    deadlines: dict[int,int]
        deadline (time step) to finish a job
    resource_requirements: dict[(int,int),int]
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
