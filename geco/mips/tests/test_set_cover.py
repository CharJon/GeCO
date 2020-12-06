import itertools

import pytest

from geco.mips.set_cover import *


@pytest.mark.parametrize(
    "m,seed", itertools.product([10, 100, 200], [0, 1, 1337, 53115])
)
def test_yang_set_cover_creation(m, seed):
    params = yang_parameter(m, seed=seed)
    model = set_cover(*params)
    assert model.getNVars() == 10 * m
    assert model.getNConss() == m
    assert model.getObjectiveSense() == "minimize"


def test_set_cover_solution_1():
    model = set_cover([1], [{0}])
    model.optimize()
    assert model.getStatus() == "optimal"
    assert model.getObjVal() == 1


def test_set_cover_solution_2():
    model = set_cover([1, 1, 1], [{0}, {1}, {2}])
    model.optimize()
    assert model.getStatus() == "optimal"
    assert model.getObjVal() == 3


@pytest.mark.parametrize(
    "m,seed1,seed2",
    itertools.product([10, 100, 200], [0, 1, 1337, 53115], [0, 1, 1337, 53115]),
)
def test_yang_parameter(m, seed1, seed2):
    params1 = yang_parameter(m, seed=seed1)
    params2 = yang_parameter(m, seed=seed2)
    same_seeds_produce_same_params = seed1 == seed2 and params1 == params2
    different_seeds_produce_different_params = seed1 != seed2 and params1 != params2
    assert same_seeds_produce_same_params or different_seeds_produce_different_params


def test_expand_set_cover():
    base_model = set_cover([1, 1, 1], [{0}, {1}, {2}])
    new_costs = [1, 1]
    new_sets = [{3}, {4}]
    expanded_model = expand_set_cover(base_model, new_costs, new_sets)
    base_model.hideOutput()
    expanded_model.hideOutput()
    base_model.optimize()
    expanded_model.optimize()
    # test that base model didn't change
    assert base_model.getStatus() == "optimal"
    assert base_model.getObjVal() == 3

    # test expanded model
    assert expanded_model.getStatus() == "optimal"
    assert expanded_model.getObjVal() == 5
