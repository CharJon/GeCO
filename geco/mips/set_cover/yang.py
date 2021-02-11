from networkx.utils import py_random_state

from geco.mips.set_cover.generic import set_cover


@py_random_state(-1)
def yang_instance(m, seed=0):
    """
    Generates instance for set cover generation as described in [1].

    Parameters
    ----------
    m: int
        Number of set constraints
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
    return set_cover(*yang_params(m, seed))


@py_random_state(-1)
def yang_params(m, seed=0):
    """
    Generates instance params for set cover generation as described in [1].

    Parameters
    ----------
    m: int
        Number of set constraints
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    costs: list[int]
        Element costs in objective function
    sets: list[set]
        Definition of element requirement for each set

    References
    ----------
    .. [1] Yu Yang, Natashia Boland, Bistra Dilkina, Martin Savelsbergh,
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
