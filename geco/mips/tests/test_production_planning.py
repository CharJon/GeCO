from geco.mips.production_planning import *


def test_tang():
    T = 100
    model = tang_instance(T)
    assert model.getNVars() == (T + 1) * 3 - 1
    assert model.getNConss() == 2 * T + 2
    assert model.getObjectiveSense() == 'minimize'


def test_tang_simple_instance():
    T = 1
    initial_storage, final_storage, p, h, q, d = 0, 20, [1, 1], [1, 1], [1, 1], [0, 0]
    M = 20  # change to less than 20 to make the solution infeasible
    params = M, initial_storage, final_storage, p, h, q, d
    model = production_planning(T, *params)
    model.hideOutput()
    model.optimize()
    assert model.getStatus() == 'optimal'
    assert model.getObjVal() == 20 + 20 + 1


def test_seeding():
    T = 100
    params1 = tang_params(T, seed=1)
    params2 = tang_params(T, seed=2)
    assert params1 != params2
