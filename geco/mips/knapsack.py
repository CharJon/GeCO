import math

import pyscipopt as scip
from networkx.utils import py_random_state


@py_random_state(1)
def yang(n, seed=0):
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


def knapsack(weights, profits, capacity, name="Knapsack"):
    assert len(weights) == len(profits)
    assert capacity >= 0
    assert all(w >= 0 for w in weights)
    assert all(p >= 0 for p in profits)

    model = scip.Model(name)
    # add variables and their cost
    variables = [model.addVar(lb=0, ub=1, obj=profit, vtype="B") for profit in profits]
    # add constraints
    model.addCons(scip.quicksum(weight * variable for weight, variable in zip(weights, variables)) <= capacity)

    model.setMaximize()

    return model
