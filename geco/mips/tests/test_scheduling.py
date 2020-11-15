from geco.mips.scheduling import *


def test_late_tasks_formulation():
    main_params = number_of_facilities, number_of_tasks, time_steps = 3, 10, 100
    params = p, C, c, R, d = generate_params(*main_params[:-1], seed=0)[:-1]

    model = hooker_late_tasks_formulation(
        *main_params, *params
    )
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


def test_heinz_formulation():
    main_params = number_of_facilities, number_of_tasks = 3, 20
    params = p, C, c, R, d, r = generate_params(*main_params, seed=0)
    time_steps = int(max(d.values()) - min(R))
    model = heinz_formulation(*main_params, *params)
    x_vars_count = number_of_facilities * number_of_tasks
    y_vars_lowerbound = number_of_facilities * number_of_tasks
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


def test_param_generation_seeding():
    n_resources, n_tasks = 10, 10
    seed1 = 1
    seed2 = 2
    params1 = generate_params(n_resources, n_tasks, seed1)
    params2 = generate_params(n_resources, n_tasks, seed2)

    one_number_is_different = False
    for i, param in enumerate(params1):
        for key in get_keys(param):
            assert key in get_keys(params2[i])
            if params2[i][key] != param[key]: one_number_is_different = True
    assert one_number_is_different


def get_keys(iterable):
    """
    Given a list or a dict returns keys(indices)

    Returns
    -------
    an iterable of keys
    """
    if isinstance(iterable, list):
        return range(len(iterable))
    elif isinstance(iterable, dict):
        return iterable.keys()
    else:
        raise ValueError("iterable given should be of type list or dict")