import random
import math

import pyscipopt as scip


def knapsack(n, seed=0):
    """
    This function is based on the MIP generation techniques described in
    Yu Yang, Natashia Boland, Bistra Dilkina, Martin Savelsbergh,
    "Learning Generalized Strong Branching for Set Covering,
    Set Packing, and 0-1 Knapsack Problems", 2020.
    """
    random.seed(seed)
    model = scip.Model("Yang Knapsack")

    def draw_value():
        return random.randint(1, 10 * n)

    # add variables and their cost
    vars = []
    for i in range(n):
        profit = draw_value()
        var = model.addVar(lb=0, ub=1, obj=profit, vtype="B")
        vars.append(var)

    # add constraints
    weights = [draw_value() for _ in vars]
    weighted_vars = (weight * var for (weight, var) in zip(weights, vars))
    capacity = math.floor(sum(weights) / 5)
    model.addCons(scip.quicksum(weighted_vars) <= capacity)

    model.setMaximize()

    return model
