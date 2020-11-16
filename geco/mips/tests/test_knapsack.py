import itertools

import pytest

from geco.mips.knapsack import *


@pytest.mark.parametrize("n,seed", itertools.product([10, 100, 1000], [0, 1, 1337, 53115]))
def test_yang_knapsack_creation(n, seed):
    params = yang_parameter(n, seed=seed)
    model = knapsack(*params)
    assert model.getNVars() == n
    assert model.getNConss() == 1
    assert model.getObjectiveSense() == 'maximize'


def test_yang_knapsack_solution_1():
    model = knapsack([1], [1], 0)
    model.optimize()
    assert model.getStatus() == "optimal"
    assert model.getObjVal() == 0


def test_yang_knapsack_solution_2():
    model = knapsack([1, 1, 1], [1, 1, 1], 5)
    model.optimize()
    assert model.getStatus() == "optimal"
    assert model.getObjVal() == 3


@pytest.mark.parametrize("n,seed1,seed2", itertools.product([3, 10, 15], [0, 1, 1337, 53115], [0, 1, 1337, 53115]))
def test_seeding(n, seed1, seed2):
    params1 = yang_parameter(n, seed=seed1)
    params2 = yang_parameter(n, seed=seed2)
    assert seed1 == seed2 or params1 != params2
