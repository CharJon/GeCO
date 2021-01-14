import pyscipopt as scip
from networkx.utils import py_random_state
from geco.mips.packing.generic import *


@py_random_state(-1)
def tang_instance(n, m, binary=False, seed=0):
    """Generates a packing instance as described in A.2 in [1].

    Parameters:
    ----------
    n: int
        number of variables
    m: int
        number of constraints
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References:
    ----------
    .. [1] Tang, Y., Agrawal, S., & Faenza, Y. (2019). Reinforcement learning for integer
    programming: Learning to cut. arXiv preprint arXiv:1906.04859.
    """
    return packing(n, m, *tang_params(n, m, binary, seed), binary, name="Tang Packing")


@py_random_state(-1)
def tang_params(n, m, binary, seed=0):
    """Generates a packing instance as described in A.2 in [1].

    Parameters:
    ----------
    n: int
        Number of variables
    m: int
        Number of constraints
    binary: bool
        Use binary variables coefficients or (non-negative) integer variables coefficients
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    costs: list[number] of size n
        Coefficients of objective function
    constraint_coefficients: list[list[number]] of dimensions (m x n)
        Coefficients of each variable for each constraint
    limits: list[number] of size m
        Limits of each constraint

    References:
    ----------
    .. [1] Tang, Y., Agrawal, S., & Faenza, Y. (2019). Reinforcement learning for integer
    programming: Learning to cut. arXiv preprint arXiv:1906.04859.
    """
    costs = [seed.randint(1, 10) for _ in range(n)]

    if binary:
        constraint_coefficients = [
            [seed.randint(5, 30) for _ in range(n)] for _ in range(m)
        ]
        limits = [seed.randint(10 * n, 20 * n) for _ in range(m)]
    else:
        constraint_coefficients = [
            [seed.randint(0, 5) for _ in range(n)] for _ in range(m)
        ]
        limits = [seed.randint(9 * n, 10 * n) for _ in range(m)]

    return costs, constraint_coefficients, limits
