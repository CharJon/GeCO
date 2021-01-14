import pyscipopt as scip
from networkx.utils import py_random_state
from geco.mips.production_planning.generic import *


@py_random_state(-1)
def tang_instance(T, seed=0):
    """Generates a production planning instance as described in A.2 in [1].

    Parameters
    ----------
    T: int
        Time horizon
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] Tang, Y., Agrawal, S., & Faenza, Y. (2019). Reinforcement learning for integer
    programming: Learning to cut. arXiv preprint arXiv:1906.04859.
    """
    return uncapacitated_lot_sizing(
        T, *tang_params(T, seed), name="Tang Production Planning"
    )


@py_random_state(-1)
def tang_params(T, seed=0):
    """Generates production planning instance params as described in A.2 in [1].

    Parameters
    ----------
    T: int
        Time horizon
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    M: int
        Maximum lot size at any time step
    initial_storage: int
        Initial available storage
    final_storage: int
        Storage available at the last time step
    p: list[int]
        Unit production cost at each time step
    h: list[int]
        Unit inventory cost at each time step
    q: list[int]
        Fixed production cost at each time step
    d: list[int]
        Demand at each time step

    References
    ----------
    .. [1] Tang, Y., Agrawal, S., & Faenza, Y. (2019). Reinforcement learning for integer
    programming: Learning to cut. arXiv preprint arXiv:1906.04859.
    """
    initial_storage = 0
    final_storage = 20
    M = 100
    p = []
    h = []
    q = []
    d = []
    for i in range(T + 1):
        p.append(seed.randint(1, 10))
        h.append(seed.randint(1, 10))
        q.append(seed.randint(1, 10))
        d.append(seed.randint(1, 10))
    return M, initial_storage, final_storage, p, h, q, d
