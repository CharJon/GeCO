import math

from networkx.utils import py_random_state

from geco.mips.knapsack.generic import knapsack


@py_random_state(-1)
def yang_params(n, seed=0):
    """
    Generates knapsack instance params according to [1].

    Parameters
    ----------
    n: int
        Number of items
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    profits: list[int]
        Profit of each item
    weights: list[int]
        Weight of each item
    capacity: float
        Capacity of knapsack

    References
    ----------
    .. [1] Yu Yang, Natashia Boland, Bistra Dilkina, Martin Savelsbergh,
        "Learning Generalized Strong Branching for Set Covering,
        Set Packing, and 0-1 Knapsack Problems", 2020.
    """

    def draw_value():
        return seed.randint(1, 10 * n)

    profits = [draw_value() for _ in range(n)]
    weights = [draw_value() for _ in range(n)]
    capacity = math.floor(sum(weights) / 5)

    return profits, weights, capacity


@py_random_state(-1)
def yang_instance(n, seed=0):
    """
    Generates knapsack instance according to [1].

    Parameters
    ----------
    n: int
        Number of items
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] Yu Yang, Natashia Boland, Bistra Dilkina, Martin Savelsbergh,
        "Learning Generalized Strong Branching for Set Covering,
        Set Packing, and 0-1 Knapsack Problems", 2020.
    """
    return knapsack(*yang_params(n, seed))
