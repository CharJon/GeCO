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


def generate_hookers_instances():
    number_of_tasks = [10 + 2 * i for i in range(7)]
    time_steps = [10, 100]
    seeds = range(10)
    for n, t, seed in itertools.product(number_of_tasks, time_steps, seeds):
        params = 3, n, t, seed
        yield params, hooker_instance(*params)
