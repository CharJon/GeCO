import itertools

from networkx.utils import py_random_state


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
    for i in range(number_of_facilities):
        value = seed.randint(1, 10)
        for j in range(number_of_tasks):
            assignment_costs[j, i] = value

    release_times = [0] * number_of_tasks

    deadlines = {}
    beta = 20 / 9
    for j in range(number_of_tasks):
        deadlines[j] = seed.uniform(beta * number_of_tasks / 4, beta * number_of_tasks)

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
