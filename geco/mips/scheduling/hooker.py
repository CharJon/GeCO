import itertools
from math import ceil

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
def c_params_generator(seed=0):
    """
    Generate instance parameters for the c problem set mentioned in [1].

    Parameters
    ----------
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
    yield from _hooker_base_parameter_generator(
        number_of_facilities_vals=(2, 3, 4),
        number_of_tasks_fn=lambda *_: range(10, 38 + 1, 2),
        release_time_fn=lambda *_: 0,
        capacity_fn=lambda: 10,
        deadlines_fn=lambda facs, tasks, _: _due_date_helper(1 / 3, facs, tasks),
        resource_requirements_fn=lambda seed: seed.randint(1, 10),
        processing_times_fn=lambda _, num_facs, seed: seed.randint(
            num_facs, num_facs * 10
        ),
        assignment_costs_fn=lambda fac, num_facs, seed: seed.randint(
            2 * (num_facs - fac + 1), 20 * (num_facs - fac + 1)
        ),
        seed=seed,
    )


@py_random_state(-1)
def e_params_generator(seed=0):
    """
    Generate instance parameters for the e problem set mentioned in [1].

    Parameters
    ----------
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
    yield from _hooker_base_parameter_generator(
        number_of_facilities_vals=range(2, 10 + 1),
        number_of_tasks_fn=lambda fac, num_fac_vals: 5 * (fac + 1),
        release_time_fn=lambda *_: 0,
        capacity_fn=lambda: 10,
        deadlines_fn=lambda facs, tasks, seed: seed.randint(
            _due_date_helper((1 / 4) * (1 / 3), facs, tasks),
            _due_date_helper(1 / 3, facs, tasks),
        ),
        resource_requirements_fn=lambda seed: seed.randint(1, 10),
        processing_times_fn=lambda fac, num_facs, seed: seed.randint(
            2, int(25 - (fac - 1) * (10 / (num_facs - 1)))
        ),
        assignment_costs_fn=lambda fac, num_facs, seed: seed.randint(
            int(400 / (25 - (fac - 1) * (10 / (num_facs - 1)))),
            int(800 / (25 - (fac - 1) * (10 / (num_facs - 1)))),
        ),
        seed=seed,
    )


@py_random_state(-1)
def de_params_generator(seed=0):
    """
    Generate instance parameters for the de problem set mentioned in [1].

    Parameters
    ----------
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

    def processing_time_generator(fac, num_facs, seed):
        range_start = 2 if num_facs <= 20 else 5  # P1 in the reference website
        return seed.randint(range_start, 30 - fac * 5)

    yield from _hooker_base_parameter_generator(
        number_of_facilities_vals=[3],
        number_of_tasks_fn=lambda *_: range(14, 28 + 1, 2),
        release_time_fn=lambda *_: 0,
        capacity_fn=lambda: 10,
        deadlines_fn=lambda *_: 33,
        resource_requirements_fn=lambda seed: seed.randint(1, 10),
        processing_times_fn=lambda fac, num_facs, seed: processing_time_generator,
        assignment_costs_fn=lambda fac, num_facs, seed: seed.randint(
            10 + 10 * fac, 40 + 10 * fac
        ),
        seed=seed,
    )


@py_random_state(-1)
def df_params_generator(seed=0):
    """
    Generate instance parameters for the df problem set mentioned in [1].

    Parameters
    ----------
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

    def processing_time_generator(fac, num_facs, seed):
        range_start = 2 if num_facs <= 20 else 5  # P1 in the reference website
        return seed.randint(range_start, 30 - fac * 5)

    yield from _hooker_base_parameter_generator(
        number_of_facilities_vals=[3],
        number_of_tasks_fn=lambda *_: range(14, 28 + 1, 2),
        release_time_fn=lambda facs, tasks, seed: seed.randint(
            0, _due_date_helper(1 / 2, facs, tasks)
        ),
        capacity_fn=lambda: 10,
        deadlines_fn=lambda *_: 33,
        resource_requirements_fn=lambda seed: seed.randint(1, 10),
        processing_times_fn=lambda fac, num_facs, seed: processing_time_generator,
        assignment_costs_fn=lambda fac, num_facs, seed: seed.randint(
            10 + 10 * fac, 40 + 10 * fac
        ),
        seed=seed,
    )


def _due_date_helper(a, number_of_facilities, number_of_tasks):
    return ceil(
        5 * a * number_of_tasks * (number_of_facilities + 1) / number_of_facilities
    )


def _hooker_base_parameter_generator(
    number_of_facilities_vals,
    number_of_tasks_fn,
    release_time_fn,
    capacity_fn,
    deadlines_fn,
    resource_requirements_fn,
    processing_times_fn,
    assignment_costs_fn,
    seed,
):
    for number_of_facilities in number_of_facilities_vals:
        number_of_tasks_vals = number_of_tasks_fn(
            number_of_facilities, number_of_facilities_vals
        )
        if isinstance(number_of_tasks_vals, int):
            number_of_tasks_vals = [number_of_tasks_vals]
        for number_of_tasks in number_of_tasks_vals:
            release_times = [
                release_time_fn(number_of_facilities, number_of_tasks, seed)
            ] * number_of_tasks
            capacities = [capacity_fn()] * number_of_facilities
            deadlines = {
                j: deadlines_fn(number_of_facilities, number_of_tasks, seed)
                for j in range(number_of_tasks)
            }
            resource_requirements = {
                (i, j): resource_requirements_fn(seed)
                for i, j in itertools.product(
                    range(number_of_tasks), range(number_of_facilities)
                )
            }
            processing_times = {
                (i, j): processing_times_fn(j, number_of_facilities, seed)
                for i, j in itertools.product(
                    range(number_of_tasks), range(number_of_facilities)
                )
            }
            assignment_costs = {
                (i, j): assignment_costs_fn(j, number_of_facilities, seed)
                for i, j in itertools.product(
                    range(number_of_tasks), range(number_of_facilities)
                )
            }

            yield (
                number_of_facilities,
                number_of_tasks,
                processing_times,
                capacities,
                assignment_costs,
                release_times,
                deadlines,
                resource_requirements,
            )
