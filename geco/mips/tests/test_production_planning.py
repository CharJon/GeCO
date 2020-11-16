from geco.mips.production_planning import *


def test_tang():
    T = 100
    model = tang_instance(T)
    assert model.getNVars() == (T + 1) * 3 - 1
    assert model.getNConss() == 2 * T + 2
    assert model.getObjectiveSense() == 'minimize'


def test_seeding():
    T = 100
    params1 = tang_params(T, seed=1)
    params2 = tang_params(T, seed=2)
    assert params1 != params2
