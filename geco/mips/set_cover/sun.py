from networkx.utils import py_random_state

from geco.mips.set_cover.generic import set_cover


def _sun_costs(n, seed):
    return [seed.randint(1, 100) for _ in range(n)]


def _sun_sets(n, m, seed, initial_sets=None):
    if not initial_sets:
        sets = [set() for _ in range(m)]
    else:
        sets = list(initial_sets)

    p = 0.05
    for e in range(n):
        # enforce element to appear in at least 2 sets
        for s in (sets[i] for i in seed.sample(range(m), k=2)):
            s.add(e)

        # add element to set with probability p
        for s in sets:
            if seed.random() < p:
                s.add(e)

    return sets


@py_random_state(-1)
def sun_instance(n, m, seed=0):
    """
    Generates instance for set cover generation as described in [1].

    Parameters
    ----------
    n: int
        Number of elements
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
    .. [1] Haoran Sun, Wenbo Chen, Hui Li, & Le Song (2021).
         Improving Learning to Branch via Reinforcement Learning. In Submitted to
         International Conference on Learning
    """
    return set_cover(*sun_params(n, m, seed))


@py_random_state(-1)
def sun_params(n, m, seed=0):
    """
    Generates instance params for set cover generation as described in [1].

    Parameters
    ----------
    n: int
        Number of elements
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
    .. [1] Haoran Sun, Wenbo Chen, Hui Li, & Le Song (2021).
         Improving Learning to Branch via Reinforcement Learning. In Submitted to
         International Conference on Learning
    """
    return _sun_costs(n, seed), _sun_sets(n, m, seed, initial_sets=None)


@py_random_state(-1)
def expand_sun_params(new_params, base_result, seed=0):
    """
    Implements the expansion from an existing set cover instance as described in [1].

    Parameters
    ----------
    new_params: tuple
        New params for sun_params
    base_result: tuple
        Tuple of (costs, sets) that represent instance params of backbone
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    costs: list[int]
        Element costs in objective function
    sets: list[set]
        Definition of element requirement for each set

    References
    __________
    .. [1] Haoran Sun, Wenbo Chen, Hui Li, & Le Song (2021).
     Improving Learning to Branch via Reinforcement Learning. In Submitted to
     International Conference on Learning
    """
    n, *_ = new_params
    base_costs, base_sets = base_result
    assert n > len(base_costs)

    costs = list(base_costs)
    costs += _sun_costs(n - len(base_costs), seed)

    return costs, _sun_sets(n, len(base_sets), seed, initial_sets=base_sets)
