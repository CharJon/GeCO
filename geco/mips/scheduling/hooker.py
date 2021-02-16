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


@py_random_state(-1)
def c_instances(seed=0):
    # TODO: use correct formulation
    for params in c_params_generator(seed):
        yield heinz_formulation(*params, name="Hooker C instance")


@py_random_state(-1)
def c_params_generator(seed=0):
    yield from _hooker_base_parameter_generator(
        number_of_facilities_vals=(2, 3, 4),
        number_of_tasks_vals=range(10, 38 + 1, 2),
        release_time_fn=lambda: 0,
        capacity_fn=lambda: 10,
        deadlines_fn=lambda facs, tasks, _: 5 * 1 / 3 * tasks * (facs + 1) / facs,
        resource_requirements_fn=lambda seed: seed.randint(1, 10),
        processing_times_fn=lambda facs, seed: seed.randint(facs, facs * 10),
        assignment_costs_fn=lambda fac, num_facs, seed: seed.randint(2 * (num_facs - fac + 1),
                                                                     20 * (num_facs - fac + 1)),
        seed=seed
    )


def _hooker_base_parameter_generator(
    number_of_facilities_vals,
    number_of_tasks_vals,
    release_time_fn,
    capacity_fn,
    deadlines_fn,
    resource_requirements_fn,
    processing_times_fn,
    assignment_costs_fn,
    seed
):
    for number_of_tasks, number_of_facilities in itertools.product(number_of_tasks_vals, number_of_facilities_vals):
        release_times = [release_time_fn()] * number_of_tasks
        capacities = [capacity_fn()] * number_of_facilities
        deadlines = {j: deadlines_fn(number_of_facilities, number_of_tasks, seed) for j in range(number_of_tasks)}
        resource_requirements = {(i, j): resource_requirements_fn(seed) for i, j in
                                 itertools.product(range(number_of_tasks), range(number_of_facilities))}
        processing_times = {(i, j): processing_times_fn(number_of_facilities, seed) for i, j in
                            itertools.product(range(number_of_tasks), range(number_of_facilities))}
        assignment_costs = {
            (i, j): assignment_costs_fn(j, number_of_facilities, seed)
            for i, j in
            itertools.product(range(number_of_tasks), range(number_of_facilities))}

        yield (
            number_of_facilities,
            number_of_tasks,
            processing_times,
            capacities,
            assignment_costs,
            release_times,
            deadlines,
            resource_requirements
        )
