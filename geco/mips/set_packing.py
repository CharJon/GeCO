import pyscipopt as scip
from networkx.utils import py_random_state


@py_random_state(-1)
def yang_instance(m, seed=0):
    """
    Generates a set packing instance following [1].

    Parameters
    ----------
    m: int
        Number of constraints
    seed: int, random state or None
        Seed for randomizatio.

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
    return set_packing(m, *yang_parameters(m, seed), name="Yang Set Packing")


@py_random_state(-1)
def yang_parameters(m, seed=0):
    """
    Generates a set packing instance following [1].

    Parameters
    ----------
    m: int
        Number of constraints
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    n: int
        Number of elements
    values: list[int]
        Value you get for packing each item
    nonzero_vars_for_constraint: list[list[int]]
        Nonzero variables list for each constraint

    References
    ----------
    .. [1] Yu Yang, Natashia Boland, Bistra Dilkina, Martin Savelsbergh,
    "Learning Generalized Strong Branching for Set Covering,
    Set Packing, and 0-1 Knapsack Problems", 2020.
    """
    n = 5 * m
    values = [seed.randint(1, 100) for _ in range(n)]
    num_nonzero_vars_for_constraint = [
        seed.randint(2 * n // 25 + 1, 3 * n // 25 - 1) for _ in range(m)
    ]
    nonzero_vars_for_constraint = [
        seed.sample(range(n), k=num) for num in num_nonzero_vars_for_constraint
    ]
    return n, values, nonzero_vars_for_constraint


def set_packing(m, n, values, nonzero_vars_for_constraint, name="Set Packing"):
    """
    Generates a set packing formulation following [1].

    Parameters
    ----------
    m: int
        Number of constraints
    n: int
        Number of elements
    values: list[int]
        Value you get for packing each item
    nonzero_vars_for_constraint: list[list[int]]
        Nonzero variables list for each constraint
    name: str
        Name of the model

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
    model = scip.Model(name)

    # add variables and their cost
    vars = []
    for i in range(n):
        var = model.addVar(lb=0, ub=1, obj=values[i], name=f"v_{i}", vtype="B")
        vars.append(var)

    # add constraints
    for i in range(m):
        nonzero_vars = (vars[j] for j in nonzero_vars_for_constraint[i])
        model.addCons(scip.quicksum(nonzero_vars) <= 1)

    model.setMaximize()

    return model
