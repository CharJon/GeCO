import pyscipopt as scip
from networkx.utils import py_random_state


@py_random_state(-1)
def yang_instance(m, seed=0):
    """
    Set packing instance following [1]

    Parameters
    ----------
    m: int
        Number of constraints.
    seed: int, random state or None
        Seed for randomization.

    Returns
    -------
        A pyscipopt model for the instance.

    References
    ----------
    .. [1] Yu Yang, Natashia Boland, Bistra Dilkina, Martin Savelsbergh,
    "Learning Generalized Strong Branching for Set Covering,
    Set Packing, and 0-1 Knapsack Problems", 2020.
    """
    return set_packing(m, *yang_parameters(m, seed), name="Yang Set Packing")


@py_random_state(-1)
def yang_parameters(m, seed=0):
    n = 5 * m
    costs = [seed.randint(1, 100) for _ in range(n)]
    num_nonzero_vars_for_constraint = [
        seed.randint(2 * n // 25 + 1, 3 * n // 25 - 1) for _ in range(m)
    ]
    nonzero_vars_for_constraint = [
        seed.sample(range(n), k=num) for num in num_nonzero_vars_for_constraint
    ]
    return n, costs, nonzero_vars_for_constraint


def set_packing(m, n, costs, nonzero_vars_for_constraint, name="Set Packing"):
    model = scip.Model(name)

    # add variables and their cost
    vars = []
    for i in range(n):
        var = model.addVar(lb=0, ub=1, obj=costs[i], name=f"v_{i}", vtype="B")
        vars.append(var)

    # add constraints
    for i in range(m):
        nonzero_vars = (vars[j] for j in nonzero_vars_for_constraint[i])
        model.addCons(scip.quicksum(nonzero_vars) <= 1)

    model.setMaximize()

    return model
