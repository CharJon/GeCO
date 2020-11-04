from geco.mips.scheduling import *


def test_late_tasks_formulation():
    main_params = number_of_facilities, number_of_tasks, time_steps = 3, 10, 100
    params = p, C, c, R, d = generate_params(*main_params[:-1], seed=0)[:-1]

    m_1 = hooker_late_tasks_formulation(
        *main_params, *params
    )
    assert (
            m_1.getNVars()
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
    assert constraints_lowerbound <= m_1.getNConss() <= constraints_upperbound
    assert m_1.getObjectiveSense() == "minimize"


def test_heinz_formulation():
    main_params = number_of_facilities, number_of_tasks = 3, 20
    params = p, C, c, R, d, r = generate_params(*main_params, seed=0)
    time_steps = int(max(d.values()) - min(R))
    m_1 = heinz_formulation(*main_params, *params)
    x_vars_count = number_of_facilities * number_of_tasks
    y_vars_lowerbound = number_of_facilities * number_of_tasks
    y_vars_upperbound = number_of_facilities * number_of_tasks * time_steps
    assert (
            x_vars_count + y_vars_lowerbound
            <= m_1.getNVars()
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
    assert constraints_lowerbound <= m_1.getNConss() <= constraints_upperbound
    assert m_1.getObjectiveSense() == "minimize"

    m_1.optimize()
    m_1.writeProblem("schedule_test.lp")
