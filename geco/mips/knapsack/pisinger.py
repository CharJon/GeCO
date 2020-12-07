"""
This module is based on the knsapsack MIP generation techniques in
David Pisinger. 2005. Where are the hard knapsack problems?
Comput. Oper. Res. 32, 9 (September 2005), 2271–2284.
DOI:https://doi.org/10.1016/j.cor.2004.03.002
"""

import math

from networkx.utils import py_random_state

from geco.mips.knapsack.generic import knapsack


def _correlated_knapsack_template(
    number_of_items, capacity, profit_generator, weight_generator, profit_first
):
    """A template for generating knapsack instances given a relation between the weights and the profits

    Parameters:
    -----------
        number_of_items: list[float]
        capacity: float
        profit_generator: function
            takes a weight and generates a profit
        weight_generator: function
            takes a profit and generates a weight
        profit_first: bool
            defines if the profits are to be generated first

    Returns:
    --------
        model: SCIP model of the knapsack instance
    """
    profits, weights = generate_from_distribution(
        number_of_items, profit_generator, weight_generator, profit_first
    )
    return knapsack(profits, weights, capacity)


def generate_from_distribution(
    number_of_items, profit_generator, weight_generator, profit_first
):
    if profit_first:
        profits = [profit_generator(None) for _ in range(number_of_items)]
        weights = [weight_generator(profit) for profit in profits]
    else:
        weights = [weight_generator(None) for _ in range(number_of_items)]
        profits = [profit_generator(weight) for weight in weights]

    return profits, weights


"""The following functions are generators for each type of 
    knapsack instance described in section 3 in the paper mentioned above
"""


@py_random_state(-1)
def uncorrelated_distribution(R, seed=0):
    return {
        "weight_generator": lambda p: seed.uniform(1, R),
        "profit_generator": lambda w: seed.uniform(1, R),
        "profit_first": True,
    }


@py_random_state(-1)
def uncorrelated(n, c, R=1000, seed=0):
    return _correlated_knapsack_template(
        number_of_items=n, capacity=c, **uncorrelated_distribution(R, seed)
    )


@py_random_state(-1)
def weakly_correlated_distribution(R, seed=0):
    return {
        "weight_generator": lambda p: seed.uniform(1, R),
        "profit_generator": lambda w: max(1, seed.uniform(w - R / 10, w + R / 10)),
        "profit_first": False,
    }


@py_random_state(-1)
def weakly_correlated(n, c, R=1000, seed=0):
    return _correlated_knapsack_template(
        number_of_items=n,
        capacity=c,
        **weakly_correlated_distribution(R, seed),
    )


@py_random_state(-1)
def strongly_correlated_distribution(R, seed=0):
    return {
        "weight_generator": lambda p: seed.uniform(1, R),
        "profit_generator": lambda w: w + R / 10,
        "profit_first": False,
    }


@py_random_state(-1)
def strongly_correlated(n, c, R=1000, seed=0):
    return _correlated_knapsack_template(
        number_of_items=n,
        capacity=c,
        **strongly_correlated_distribution(R, seed),
    )


@py_random_state(-1)
def inverse_strongly_correlated_distribution(R, seed=0):
    return {
        "weight_generator": lambda p: p + R / 10,
        "profit_generator": lambda w: seed.uniform(1, R),
        "profit_first": True,
    }


@py_random_state(-1)
def inverse_strongly_correlated(n, c, R=1000, seed=0):
    return _correlated_knapsack_template(
        number_of_items=n,
        capacity=c,
        **inverse_strongly_correlated_distribution(R, seed),
    )


@py_random_state(-1)
def almost_strongly_correlated_distribution(R, seed=0):
    return {
        "weight_generator": lambda p: seed.uniform(1, R),
        "profit_generator": lambda w: seed.uniform(
            w + R / 10 - R / 500, w + R / 10 - R / 500
        ),
        "profit_first": False,
    }


@py_random_state(-1)
def almost_strongly_correlated(n, c, R=1000, seed=0):
    return _correlated_knapsack_template(
        number_of_items=n,
        capacity=c,
        **almost_strongly_correlated_distribution(R, seed),
    )


@py_random_state(-1)
def subset_sum_distribution(R, seed=0):
    return {
        "weight_generator": lambda p: seed.uniform(1, R),
        "profit_generator": lambda w: w,
        "profit_first": False,
    }


@py_random_state(-1)
def subset_sum(n, c, R=1000, seed=0):
    return _correlated_knapsack_template(
        number_of_items=n, capacity=c, **subset_sum_distribution(R, seed)
    )


@py_random_state(-1)
def uncorrelated_with_similar_weights_distribution(R, seed=0):
    return {
        "weight_generator": lambda p: seed.uniform(100_000, 100_100),
        "profit_generator": lambda w: seed.uniform(1, 1000),
        "profit_first": False,
    }


@py_random_state(-1)
def uncorrelated_with_similar_weights(n, c, R=1000, seed=0):
    return _correlated_knapsack_template(
        number_of_items=n,
        capacity=c,
        **uncorrelated_with_similar_weights_distribution(R, seed),
    )


@py_random_state(-1)
def spanner(v, m, n, distribution, capacity, R=1000, seed=0):
    # generate the spanner set of v items
    profits, weights = generate_from_distribution(v, **distribution(R, seed))

    # normalize the spanner set # TODO: this might require a list instead of a map
    spanner_profits = [p / m + 1 for p in profits]
    spanner_weights = [w / m + 1 for w in weights]

    # generate n items from spanner set
    profits = []
    weights = []
    spanner_set_indices = list(range(v))
    for _ in range(n):
        idx = seed.choice(spanner_set_indices)
        multiplier = seed.uniform(1, m)
        profit, weight = (
            multiplier * spanner_profits[idx],
            multiplier * spanner_weights[idx],
        )
        profits.append(profit)
        weights.append(weight)

    return knapsack(profits, weights, capacity)


@py_random_state(-1)
def profit_ceiling(n, c, d=3, R=1000, seed=0):
    return _correlated_knapsack_template(
        number_of_items=n,
        capacity=c,
        profit_generator=lambda w: d * math.ceil(w / d),
        weight_generator=lambda p: seed.uniform(1, R),
        profit_first=False,
    )


@py_random_state(-1)
def circle(n, c, d=2 / 3, R=1000, seed=0):
    return _correlated_knapsack_template(
        number_of_items=n,
        capacity=c,
        profit_generator=lambda w: d * math.sqrt(4 * (R ** 2) - (w - 2 * R) ** 2),
        weight_generator=lambda p: seed.uniform(1, R),
        profit_first=False,
    )


@py_random_state(-1)
def multiple_strongly_correlated(n, c, k1, k2, d, R=1000, seed=0):
    return _correlated_knapsack_template(
        number_of_items=n,
        capacity=c,
        profit_generator=lambda w: w + k1 if w % d == 0 else w + k2,
        weight_generator=lambda p: seed.uniform(1, R),
        profit_first=False,
    )
