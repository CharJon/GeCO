import pyscipopt as scip


def knapsack(weights, profits, capacity, name="Knapsack"):
    """Generates a knapsack MIP formulation.

    Parameters:
    ----------
        profits: list[float]
            List of profits of each item
        weights: list[float]
            List of weights of each item
        capacity: float
            Capacity of knapsack

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance
    """
    assert len(weights) == len(profits)
    assert capacity >= 0
    assert all(w >= 0 for w in weights)
    assert all(p >= 0 for p in profits)

    model = scip.Model(name)
    # add variables and their cost
    variables = [model.addVar(lb=0, ub=1, obj=profit, vtype="B") for profit in profits]
    # add constraints
    model.addCons(
        scip.quicksum(weight * variable for weight, variable in zip(weights, variables))
        <= capacity
    )

    model.setMaximize()

    return model
