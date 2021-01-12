import itertools
import types

import pytest

from geco.mips.knapsack.pisinger import *
from geco.mips.knapsack.yang import *

"""
Yang Generators Tests
"""


@pytest.mark.parametrize(
    "n,seed", itertools.product([10, 100, 1000], [0, 1, 1337, 53115])
)
def test_yang_knapsack_creation(n, seed):
    model = yang_instance(n, seed=seed)
    assert model.getNVars() == n
    assert model.getNConss() == 1
    assert model.getObjectiveSense() == "maximize"


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


@pytest.mark.parametrize(
    "n,seed1,seed2",
    itertools.product([3, 10, 15], [0, 1, 1337, 53115], [0, 1, 1337, 53115]),
)
def test_yang_seeding(n, seed1, seed2):
    params1 = yang_params(n, seed=seed1)
    params2 = yang_params(n, seed=seed2)
    same_seeds_produce_same_params = seed1 == seed2 and params1 == params2
    different_seeds_produce_different_params = seed1 != seed2 and params1 != params2
    assert same_seeds_produce_same_params or different_seeds_produce_different_params


"""
Pisinger Generators Tests
"""


def test_pisinger_creation_of_all():
    n = 100
    c = 20
    models = [
        uncorrelated(n, c),
        weakly_correlated(n, c),
        strongly_correlated(n, c),
        inverse_strongly_correlated(n, c),
        almost_strongly_correlated(n, c),
        subset_sum(n, c),
        uncorrelated_with_similar_weights(n, c),
        profit_ceiling(n, c),
        circle(n, c),
        multiple_strongly_correlated(n, c, 7, 10, 3),
        spanner(10, 100, 100, uncorrelated_distribution, 500),
    ]
    for model in models:
        assert model.getNVars() == n
        assert model.getNConss() == 1
        assert model.getObjectiveSense() == "maximize"


@pytest.mark.parametrize(
    "n,R,distribution,seed1,seed2",
    itertools.product(
        [3, 10, 15],
        [10, 100],
        [
            uncorrelated_distribution,
            weakly_correlated_distribution,
            strongly_correlated_distribution,
            inverse_strongly_correlated_distribution,
            almost_strongly_correlated_distribution,
            subset_sum_distribution,
            uncorrelated_with_similar_weights_distribution,
        ],
        [0, 1, 1337, 53115],
        [0, 1, 1337, 53115],
    ),
)
def test_pisinger_seeding(n, R, distribution: types.FunctionType, seed1, seed2):
    params1 = generate_from_distribution(n, **distribution(R=R, seed=seed1))
    params2 = generate_from_distribution(n, **distribution(R=R, seed=seed2))
    same_seeds_produce_same_params = seed1 == seed2 and params1 == params2
    different_seeds_produce_different_params = seed1 != seed2 and params1 != params2
    assert same_seeds_produce_same_params or different_seeds_produce_different_params
