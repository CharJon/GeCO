import pytest

from geco.mips.scheduling.heinz import *
from geco.mips.scheduling.hooker import *


def test_hooker_formulation():
    params = number_of_facilities, number_of_tasks, time_steps = 3, 10, 100
    model = hooker_instance(*params)
    _check_hookers_instance(model, number_of_facilities, number_of_tasks, time_steps)


def test_hooker_generation():
    for params, model in generate_hookers_instances():
        _check_hookers_instance(model, *params[:-1])


@pytest.mark.parametrize(
    "number_of_facilities,number_of_tasks,seed",
    itertools.product([1, 2, 3], [5, 10, 15], [0, 1, 1337, 53115]),
)
def test_heinz_formulation(number_of_facilities, number_of_tasks, seed):
    main_params = number_of_facilities, number_of_tasks
    p, C, c, R, d, r = heinz_params(*main_params, seed)
    time_steps = int(max(d.values()) - min(R))
    model = heinz_instance(*main_params)
    x_vars_count = number_of_facilities * number_of_tasks
    y_vars_lowerbound = 0
    y_vars_upperbound = number_of_facilities * number_of_tasks * time_steps
    assert (
        x_vars_count + y_vars_lowerbound
        <= model.getNVars()
        <= x_vars_count + y_vars_upperbound
    )
    constraints_lowerbound = (
        number_of_facilities
        + number_of_facilities * number_of_tasks
        + number_of_tasks
        + number_of_tasks
        + number_of_facilities * number_of_tasks
        + number_of_facilities * number_of_tasks
    )
    constraints_upperbound = (
        number_of_facilities
        + number_of_facilities * number_of_tasks
        + number_of_tasks * time_steps
        + number_of_tasks * (time_steps * (time_steps - 1) // 2)
        + number_of_facilities * number_of_tasks
        + number_of_facilities * number_of_tasks * time_steps
    )
    assert constraints_lowerbound <= model.getNConss() <= constraints_upperbound
    assert model.getObjectiveSense() == "minimize"

    model.optimize()


@pytest.mark.parametrize(
    "n_resources,n_tasks,seed1,seed2",
    itertools.product([1, 2, 3], [5, 10, 15], [0, 1, 1337, 53115], [0, 1, 1337, 53115]),
)
def test_param_generation_seeding(n_resources, n_tasks, seed1, seed2):
    params1 = generate_params(n_resources, n_tasks, seed=seed1)
    params2 = generate_params(n_resources, n_tasks, seed=seed2)
    same_seeds_produce_same_params = seed1 == seed2 and params1 == params2
    different_seeds_produce_different_params = seed1 != seed2 and params1 != params2
    assert same_seeds_produce_same_params or different_seeds_produce_different_params


def test_hooker_simple_instance():
    hooker_model = hooker_formulation(*_simple_instance_params()[:-1])
    hooker_model.hideOutput()
    hooker_model.optimize()
    assert hooker_model.getStatus() == "optimal"
    assert hooker_model.getObjVal() == 0


def test_heinz_simple_instance():
    (
        n_resources,
        n_tasks,
        time_steps,
        processing_times,
        capacities,
        assignment_costs,
        release_times,
        deadlines,
        resource_requirements,
    ) = _simple_instance_params()
    heinz_model = heinz_formulation(
        n_resources,
        n_tasks,
        processing_times,
        capacities,
        assignment_costs,
        release_times,
        deadlines,
        resource_requirements,
    )
    heinz_model.hideOutput()
    heinz_model.optimize()
    assert heinz_model.getStatus() == "optimal"
    assert heinz_model.getObjVal() == 1


def _simple_instance_params():
    n_resources = 1
    n_tasks = 1
    time_steps = 1
    processing_times = {(0, 0): 1}
    capacities = [1]
    assignment_costs = {(0, 0): 1}
    release_times = [0]
    # change the deadline to 0 or 1 to make it infeasible for the heinz formulation
    # and add 1 late task to the hooker formulation
    deadlines = {0: 2}
    resource_requirements = {(0, 0): 1}
    return (
        n_resources,
        n_tasks,
        time_steps,
        processing_times,
        capacities,
        assignment_costs,
        release_times,
        deadlines,
        resource_requirements,
    )


def _check_hookers_instance(model, number_of_facilities, number_of_tasks, time_steps):
    assert (
        model.getNVars()
        == number_of_facilities * number_of_tasks * time_steps + number_of_tasks
    )
    constraints_lowerbound = (
        number_of_tasks * time_steps
        + number_of_tasks
        + number_of_facilities * time_steps
    )
    constraints_upperbound = (
        number_of_tasks * time_steps
        + number_of_tasks
        + number_of_facilities * time_steps
        + number_of_facilities * number_of_tasks * time_steps
    )
    assert constraints_lowerbound <= model.getNConss() <= constraints_upperbound
    assert model.getObjectiveSense() == "minimize"
