import itertools
import math

import pyscipopt as scip
from geco.mips.scheduling.generic import generate_params
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
    return late_tasks_formulation(
        number_of_facilities,
        number_of_tasks,
        time_steps,
        *hooker_params(number_of_facilities, number_of_tasks, seed),
        name="Hooker Scheduling Instance",
    )


def generate_hookers_instances():
    number_of_tasks = [10 + 2 * i for i in range(7)]
    time_steps = [10, 100]
    seeds = range(10)
    for n, t, seed in itertools.product(number_of_tasks, time_steps, seeds):
        params = 3, n, t, seed
        yield params, hooker_instance(*params)


def _common_hooker_params(number_of_facilities, number_of_tasks, seed):
    capacities = [10] * number_of_facilities
    resource_requirements = {}
    for i in range(number_of_tasks):
        cur_res_requirement = seed.randrange(1, 10)
        for j in range(number_of_facilities):
            resource_requirements[i, j] = cur_res_requirement
    return capacities, resource_requirements


@py_random_state(-1)
def c_instance_params(seed=0):
    for m, n in itertools.product(range(2, 4 + 1), range(10, 38 + 1, 2)):
        yield c_params_generator(m, n, seed)


@py_random_state(-1)
def c_params_generator(number_of_facilities, number_of_tasks, seed=0):
    """
    Generate instance parameters for the c problem set mentioned in [1].

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
    release_times: list[int]
        time step at which a job is released
    deadlines: dict[int, int]
        deadline (time step) to finish a job
    resource_requirements: dict[(int,int),int]
        resources required for each task assigned to a facility

    References
    ----------
    ..[1] http://public.tepper.cmu.edu/jnh/instances.htm
    """
    capacities, resource_requirements = _common_hooker_params(
        number_of_facilities, number_of_tasks, seed
    )

    release_dates = [0] * number_of_tasks
    due_dates = [
        _due_date_helper(1 / 3, number_of_facilities, number_of_tasks)
    ] * number_of_tasks

    processing_times = {}
    for i in range(number_of_facilities):
        for j in range(number_of_tasks):
            processing_times[j, i] = seed.randrange(i + 1, 10 * (i + 1))

    processing_costs = {}
    for i in range(number_of_facilities):
        for j in range(number_of_tasks):
            processing_costs[j, i] = seed.randrange(
                2 * (number_of_facilities - i), 20 * (number_of_facilities - i)
            )

    return (
        number_of_facilities,
        number_of_tasks,
        processing_times,
        capacities,
        processing_costs,
        release_dates,
        due_dates,
        resource_requirements,
    )


@py_random_state(-1)
def e_instance_params(seed=0):
    for m in range(2, 10 + 1):
        yield e_params_generator(m, 5 * m, seed)


@py_random_state(-1)
def e_params_generator(number_of_facilities, number_of_tasks, seed=0):
    """
    Generate instance parameters for the e problem set mentioned in [1].

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
    release_times: list[int]
        time step at which a job is released
    deadlines: dict[int, int]
        deadline (time step) to finish a job
    resource_requirements: dict[(int,int),int]
        resources required for each task assigned to a facility

    References
    ----------
    ..[1] http://public.tepper.cmu.edu/jnh/instances.htm
    """
    capacities, resource_requirements = _common_hooker_params(
        number_of_facilities, number_of_tasks, seed
    )

    release_dates = [0] * number_of_tasks
    due_dates = [33] * number_of_tasks

    processing_times = {}
    for i in range(number_of_facilities):
        for j in range(number_of_tasks):
            processing_times[j, i] = seed.randrange(
                2, int(25 - i * (10 / (number_of_facilities - 1)))
            )

    processing_costs = {}
    for i in range(number_of_facilities):
        for j in range(number_of_tasks):
            processing_costs[j, i] = seed.randrange(
                math.floor(400 / (25 - i * (10 / (number_of_facilities - 1)))),
                math.ceil(800 / (25 - i * (10 / (number_of_facilities - 1)))),
            )

    return (
        number_of_facilities,
        number_of_tasks,
        processing_times,
        capacities,
        processing_costs,
        release_dates,
        due_dates,
        resource_requirements,
    )


@py_random_state(-1)
def de_instance_params(seed=0):
    for n in range(14, 28 + 1, 2):
        yield de_params_generator(3, n, seed)


@py_random_state(-1)
def de_params_generator(number_of_facilities, number_of_tasks, seed=0):
    """
    Generate instance parameters for the de problem set mentioned in [1].

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
    release_times: list[int]
        time step at which a job is released
    deadlines: dict[int, int]
        deadline (time step) to finish a job
    resource_requirements: dict[(int,int),int]
        resources required for each task assigned to a facility

    References
    ----------
    ..[1] http://public.tepper.cmu.edu/jnh/instances.htm
    """
    capacities, resource_requirements = _common_hooker_params(
        number_of_facilities, number_of_tasks, seed
    )

    release_dates = [0] * number_of_tasks
    due_dates = [
        seed.randrange(
            _due_date_helper((1 / 4) * (1 / 3), number_of_facilities, number_of_tasks),
            _due_date_helper(1 / 3, number_of_facilities, number_of_tasks),
        )
        for _ in range(number_of_tasks)
    ]

    processing_times = {}
    range_start = 2 if number_of_facilities <= 20 else 5  # P1 in the reference website
    for i in range(number_of_facilities):
        for j in range(number_of_tasks):
            processing_times[j, i] = seed.randrange(range_start, 30 - i * 5)

    processing_costs = {}
    for i in range(number_of_facilities):
        for j in range(number_of_tasks):
            processing_costs[j, i] = seed.randrange(10 + 10 * i, 40 + 10 * i)

    return (
        number_of_facilities,
        number_of_tasks,
        processing_times,
        capacities,
        processing_costs,
        release_dates,
        due_dates,
        resource_requirements,
    )


@py_random_state(-1)
def df_instance_params(seed=0):
    for n in range(14, 28 + 1, 2):
        yield df_params_generator(3, n, seed)


@py_random_state(-1)
def df_params_generator(number_of_facilities, number_of_tasks, seed=0):
    """
    Generate instance parameters for the df problem set mentioned in [1].

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
    release_times: list[int]
        time step at which a job is released
    deadlines: dict[int, int]
        deadline (time step) to finish a job
    resource_requirements: dict[(int,int),int]
        resources required for each task assigned to a facility

    References
    ----------
    ..[1] http://public.tepper.cmu.edu/jnh/instances.htm
    """
    capacities, resource_requirements = _common_hooker_params(
        number_of_facilities, number_of_tasks, seed
    )

    release_dates = [0] * number_of_tasks

    random_release_time = seed.choice(release_dates)
    due_dates = [
        seed.randrange(
            random_release_time
            + _due_date_helper(1 / 4 * 1 / 2, number_of_facilities, number_of_tasks),
            random_release_time
            + _due_date_helper(1 / 2, number_of_facilities, number_of_tasks),
        )
        for _ in range(number_of_tasks)
    ]

    processing_times = {}
    range_start = 2 if number_of_facilities <= 20 else 5  # P1 in the reference website
    for i in range(number_of_facilities):
        for j in range(number_of_tasks):
            processing_times[j, i] = seed.randrange(range_start, 30 - i * 5)

    processing_costs = {}
    for i in range(number_of_facilities):
        for j in range(number_of_tasks):
            processing_costs[j, i] = seed.randrange(10 + 10 * i, 40 + 10 * i)

    return (
        number_of_facilities,
        number_of_tasks,
        processing_times,
        capacities,
        processing_costs,
        release_dates,
        due_dates,
        resource_requirements,
    )


def _due_date_helper(a, number_of_facilities, number_of_tasks):
    return math.ceil(
        5 * a * number_of_tasks * (number_of_facilities + 1) / number_of_facilities
    )
