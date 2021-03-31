import collections
import itertools

import pytest

from geco.mips.set_cover.yang import *
from geco.mips.set_cover.sun import *
from geco.mips.set_cover.orlib import *
from geco.mips.set_cover.gasse import *

"""
Generic Tests
"""


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


"""
Yang Tests
"""


@pytest.mark.parametrize(
    "m,seed", itertools.product([10, 100, 200], [0, 1, 1337, 53115])
)
def test_yang_set_cover_creation(m, seed):
    model = yang_instance(m, seed)
    assert model.getNVars() == 10 * m
    assert model.getNConss() == m
    assert model.getObjectiveSense() == "minimize"


@pytest.mark.parametrize(
    "m,seed1,seed2",
    itertools.product([10, 100, 200], [0, 1, 1337, 53115], [0, 1, 1337, 53115]),
)
def test_yang_parameter(m, seed1, seed2):
    params1 = yang_params(m, seed=seed1)
    params2 = yang_params(m, seed=seed2)
    same_seeds_produce_same_params = seed1 == seed2 and params1 == params2
    different_seeds_produce_different_params = seed1 != seed2 and params1 != params2
    assert same_seeds_produce_same_params or different_seeds_produce_different_params


"""
Sun Tests
"""


@pytest.mark.parametrize(
    "n,m,seed", itertools.product([10, 100, 200], [10, 100, 200], [0, 1, 1337, 53115])
)
def test_sun_set_cover_creation(n, m, seed):
    model = sun_instance(n, m, seed)
    assert model.getNVars() == n
    assert model.getNConss() == m
    assert model.getObjectiveSense() == "minimize"


@pytest.mark.parametrize(
    "n,m,seed1,seed2",
    itertools.product(
        [10, 100, 200], [10, 100, 200], [0, 1, 1337, 53115], [0, 1, 1337, 53115]
    ),
)
def test_sun_params(n, m, seed1, seed2):
    params1 = sun_params(n, m, seed=seed1)
    params2 = sun_params(n, m, seed=seed2)
    same_seeds_produce_same_params = seed1 == seed2 and params1 == params2
    different_seeds_produce_different_params = seed1 != seed2 and params1 != params2
    assert same_seeds_produce_same_params or different_seeds_produce_different_params


@pytest.mark.parametrize(
    "n,m,seed", itertools.product([10, 100, 200], [10, 100, 200], [0, 1, 1337, 53115])
)
def test_sun_at_least_two_elements_in_set(n, m, seed):
    _, sets = sun_params(n, m, seed=seed)
    counter = collections.defaultdict(int)
    for s in sets:
        for e in s:
            counter[e] += 1
    assert all([count >= 2 for count in counter.values()])


@pytest.mark.parametrize(
    "n,base_n,base_m,seed1,seed2",
    itertools.product(
        [10, 100, 200],
        [1, 5, 9],
        [10, 100, 200],
        [0, 1, 1337, 53115],
        [0, 1, 1337, 53115],
    ),
)
def test_expand_sun_params(n, base_n, base_m, seed1, seed2):
    base_costs1, base_sets1 = sun_params(base_n, base_m, seed1)
    base_costs2, base_sets2 = sun_params(base_n, base_m, seed2)
    params1 = costs1, sets1 = expand_sun_params((n,), (base_costs1, base_sets1), seed1)
    params2 = costs2, sets2 = expand_sun_params((n,), (base_costs2, base_sets2), seed2)

    # test seeding
    same_seeds_produce_same_params = seed1 == seed2 and params1 == params2
    different_seeds_produce_different_params = seed1 != seed2 and params1 != params2
    assert same_seeds_produce_same_params or different_seeds_produce_different_params

    # test correct size
    assert len(costs1) == len(costs2) == n
    assert len(sets1) == len(sets2) == base_m


"""
OR-Library tests
"""


def test_scp_orlib():
    instance_name = "scp41.txt"
    instance = orlib_instance(instance_name)
    assert instance.getNVars() == 1000
    assert instance.getNConss() == 200


def test_rail_orlib():
    instance_name = "rail507.txt"
    instance = orlib_instance(instance_name)
    assert instance.getNVars() == 63009
    assert instance.getNConss() == 507


"""
Gasse tests
"""


@pytest.mark.parametrize(
    "nrows,ncols,density,seed1,seed2",
    itertools.product(
        [100, 200],
        [10, 100, 200],
        [0.2, 0.3, 0.5],
        [0, 1, 1337, 53115],
        [0, 1, 1337, 53115],
    ),
)
def test_gasse_params(nrows, ncols, density, seed1, seed2):
    params1 = gasse_params(nrows, ncols, density, seed=seed1)
    params2 = gasse_params(nrows, ncols, density, seed=seed2)
    same_seeds_produce_same_params = seed1 == seed2 and params1 == params2
    different_seeds_produce_different_params = seed1 != seed2 and params1 != params2
    assert same_seeds_produce_same_params or different_seeds_produce_different_params


@pytest.mark.parametrize(
    "nrows,ncols,density,seed",
    itertools.product(
        [100, 200],
        [50, 70],
        [0.2, 0.3, 0.5],
        [0, 1, 1337, 53115],
    ),
)
def test_gasse_instance(nrows, ncols, density, seed):
    model = gasse_instance(nrows, ncols, density, max_coef=10, seed=seed)
    assert model.getNVars() == ncols
    assert model.getNConss() == nrows
    assert model.getObjectiveSense() == "minimize"
