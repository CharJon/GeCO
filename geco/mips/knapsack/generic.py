import pyscipopt as scip


def knapsack(weights, profits, capacity, name="Knapsack"):
    """Given profits, weights and capacity. It returns a SCIP model
        for the corresponding MIP formulation of the knapsack instance

    Parameters:
    ----------
        profits: list[float]
            list of profits of each item
        weights: list[float]
            list of weights of each item
        capacity: float
            capacity of knapsack
    Returns:
    --------
        model: SCIP model of the knapsack instance
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
