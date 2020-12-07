import math

from networkx.utils import py_random_state

from geco.mips.knapsack.generic import knapsack


@py_random_state(1)
def yang_instance(n, seed=0):
    return knapsack(*yang_parameter(n, seed))


@py_random_state(1)
def yang_parameter(n, seed=0):
    """
    Generates knapsack instance parameters according to:
        Yu Yang, Natashia Boland, Bistra Dilkina, Martin Savelsbergh,
        "Learning Generalized Strong Branching for Set Covering,
        Set Packing, and 0-1 Knapsack Problems", 2020.
    """

    def draw_value():
        return seed.randint(1, 10 * n)

    profits = [draw_value() for _ in range(n)]
    weights = [draw_value() for _ in range(n)]
    capacity = math.floor(sum(weights) / 5)

    return profits, weights, capacity
