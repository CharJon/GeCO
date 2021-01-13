import pyscipopt as scip


def set_cover(costs, sets):
    """
    Generates basic set cover formulation.

    Parameters
    ----------
    costs: list[float]
        Cost for covering each element
    sets: list[set]
        Set constraints for elements

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    """
    model = scip.Model("Set Cover")

    # add variables and their cost
    variables = [
        model.addVar(lb=0, ub=1, obj=c, name=f"v_{i}", vtype="B")
        for i, c in enumerate(costs)
    ]

    # add constraints
    for s in sets:
        model.addCons(scip.quicksum(variables[i] for i in s) >= 1)

    model.setMinimize()

    return model
