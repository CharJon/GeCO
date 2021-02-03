import itertools

import pytest

from geco.mips.packing.tang import *


def test_tang_integral():
    n, m = 10, 10
    model = tang_instance(n, m, binary=False)
    vars = model.getVars()
    assert len(vars) == n
    assert all(var.vtype() == "INTEGER" for var in vars)
    assert model.getNConss() == m
    assert model.getObjectiveSense() == "maximize"


def test_tang_binary():
    n, m = 10, 10
    model = tang_instance(n, m, binary=True)
    vars = model.getVars()
    assert len(vars) == n
    assert all(var.vtype() == "BINARY" for var in vars)
    assert model.getNConss() == m
    assert model.getObjectiveSense() == "maximize"


def test_tang_simple_instance():
    n, m, costs, constraint_coefficients, limits, binary = 1, 1, [1], [[1]], [5], False
    model = packing(n, m, costs, constraint_coefficients, limits, binary)
    model.hideOutput()
    model.optimize()
    assert model.getStatus() == "optimal"
    assert model.getObjVal() == 5


@pytest.mark.parametrize(
    "n,m,binary,seed1,seed2",
    itertools.product(
        [3, 10, 100],
        [3, 10, 100],
        [True, False],
        [0, 1, 1337, 53115],
        [0, 1, 1337, 53115],
    ),
)
def test_seeding(n, m, binary, seed1, seed2):
    params1 = tang_params(n, m, binary, seed=seed1)
    params2 = tang_params(n, m, binary, seed=seed2)
    same_seeds_produce_same_params = seed1 == seed2 and params1 == params2
    different_seeds_produce_different_params = seed1 != seed2 and params1 != params2
    assert same_seeds_produce_same_params or different_seeds_produce_different_params
