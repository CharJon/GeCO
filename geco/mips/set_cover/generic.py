import pyscipopt as scip


def set_cover(costs, sets):
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
