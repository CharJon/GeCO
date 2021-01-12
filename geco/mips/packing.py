import pyscipopt as scip
from networkx.utils import py_random_state


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


def packing(n, m, costs, constraint_coefficients, limits, binary, name="Packing"):
    """Generates a packing instance as described in A.2 in [1].

    Parameters:
    ----------
    n: int
        Number of variables
    m: int
        Number of constraints
    costs: list[number] of size n
        Coefficients of objective function
    constraint_coefficients: list[list[number]] of dimensions (m x n)
        Coefficients of each variable for each constraint
    limits: list[number] of size m
        Limits of each constraint
    name: str
        Name of the model

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References:
    ----------
    .. [1] Tang, Y., Agrawal, S., & Faenza, Y. (2019). Reinforcement learning for integer
    programming: Learning to cut. arXiv preprint arXiv:1906.04859.
    """
    model = scip.Model(name)

    # add variables and their cost
    vars = []
    for i in range(n):
        cost = costs[i]
        if binary:
            var = model.addVar(lb=0, ub=1, obj=cost, name=f"v_{i}", vtype="B")
        else:
            var = model.addVar(lb=0, ub=None, obj=cost, name=f"v_{i}", vtype="I")
        vars.append(var)

    # add constraints
    for i in range(m):
        constraint_vars = (
            constraint_coefficients[i][j] * var for j, var in enumerate(vars)
        )
        model.addCons(scip.quicksum(constraint_vars) <= limits[i])

    # contrary to the paper (as of 05/11/2020) as a result of correspondence of with one of the authors
    model.setMaximize()

    return model
