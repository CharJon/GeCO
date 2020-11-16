import pyscipopt as scip

from networkx.utils import py_random_state


@py_random_state(1)
def yang_instance(m, seed=0):
    """Yu Yang, Natashia Boland, Bistra Dilkina, Martin Savelsbergh,
    "Learning Generalized Strong Branching for Set Covering,
    Set Packing, and 0-1 Knapsack Problems", 2020.
    """
    return set_cover(*yang_parameter(m, seed))


@py_random_state(1)
def yang_parameter(m, seed=0):
    """Yu Yang, Natashia Boland, Bistra Dilkina, Martin Savelsbergh,
    "Learning Generalized Strong Branching for Set Covering,
    Set Packing, and 0-1 Knapsack Problems", 2020.
    """
    n = 10 * m

    costs = [seed.randint(1, 100) for _ in range(n)]

    sets = []
    for _ in range(m):
        num_nonzero = seed.randint(2 * n // 25 + 1, 3 * n // 25 - 1)
        sets.append(set(j for j in seed.sample(range(n), k=num_nonzero)))

    return costs, sets


def set_cover(costs, sets):
    model = scip.Model("Set Cover")

    # add variables and their cost
    variables = [
        model.addVar(lb=0, ub=1, obj=c, name=f"v_{i}", vtype="B")
        for i, c in enumerate(costs)
    ]

    # add constraints
    for s in sets:
        model.addCons(scip.quicksum(variables[i] for i in s) >= 1)

    model.setMinimize()

    return model
