import random

import pyscipopt as scip
from networkx.utils import py_random_state


@py_random_state(1)
def tang_instance(T, seed=0):
    """Generates a production planning instance as described in A.2 in
    Tang, Y., Agrawal, S., & Faenza, Y. (2019). Reinforcement learning for integer
    programming: Learning to cut. arXiv preprint arXiv:1906.04859.

    Args:
        T (int): Time horizon
        seed (int, optional): seed for randomization

    Returns:
        model: SCIP model of the generated instance
    """
    random.seed(seed)
    model = scip.Model("Tang Production Planning")

    # add variables and their cost
    production_vars = []
    produce_or_not_vars = []
    storage_vars = []
    M, initial_storage, final_storage, p, h, q, d = tang_params(T, seed)
    for i in range(T + 1):
        var = model.addVar(lb=0, ub=None, obj=p[i], name=f"x_{i}", vtype="I")
        production_vars.append(var)

        var = model.addVar(lb=0, ub=1, obj=h[i], name=f"y_{i}", vtype="B")
        produce_or_not_vars.append(var)

        var = model.addVar(lb=0, ub=None, obj=q[i], name=f"s_{i}", vtype="I")
        storage_vars.append(var)

    # remove unneeded var
    model.delVar(production_vars[0])

    # add constraints
    for i in range(1, T + 1):
        model.addCons(storage_vars[i - 1] + production_vars[i] == d[i] + storage_vars[i])
        model.addCons(production_vars[i] <= M * produce_or_not_vars[i])

    model.addCons(storage_vars[0] == initial_storage)
    model.addCons(storage_vars[T] == final_storage)

    model.setMinimize()

    return model


@py_random_state(1)
def tang_params(T, seed=0):
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
