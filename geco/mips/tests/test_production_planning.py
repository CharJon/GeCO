import itertools

import pytest

from geco.mips.production_planning.tang import *


def test_tang():
    T = 100
    model = tang_instance(T)
    assert model.getNVars() == (T + 1) * 3 - 1
    assert model.getNConss() == 2 * T + 2
    assert model.getObjectiveSense() == "minimize"


def test_tang_simple_feasible():
    T = 1
    initial_storage, final_storage, p, h, q, d = 0, 20, [1, 1], [1, 1], [1, 1], [0, 0]
    M = 20
    params = M, initial_storage, final_storage, p, h, q, d
    model = uncapacitated_lot_sizing(T, *params)
    model.hideOutput()
    model.optimize()
    assert model.getStatus() == "optimal"
    assert model.getObjVal() == 20 + 20 + 1


def test_tang_simple_infeasible():
    T = 1
    initial_storage, final_storage, p, h, q, d = 0, 20, [1, 1], [1, 1], [1, 1], [0, 0]
    M = 19
    params = M, initial_storage, final_storage, p, h, q, d
    model = uncapacitated_lot_sizing(T, *params)
    model.hideOutput()
    model.optimize()
    assert model.getStatus() == "infeasible"


@pytest.mark.parametrize(
    "T,seed1,seed2",
    itertools.product([10, 100, 200], [0, 1, 1337, 53115], [0, 1, 1337, 53115]),
)
def test_seeding(T, seed1, seed2):
    params1 = tang_params(T, seed=seed1)
    params2 = tang_params(T, seed=seed2)
    same_seeds_produce_same_params = seed1 == seed2 and params1 == params2
    different_seeds_produce_different_params = seed1 != seed2 and params1 != params2
    assert same_seeds_produce_same_params or different_seeds_produce_different_params
