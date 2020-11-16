import pytest
import itertools

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


def test_yang_parameter():
    params_1 = yang_parameter(10, seed=1)
    params_2 = yang_parameter(10, seed=11)
    assert params_1 != params_2
