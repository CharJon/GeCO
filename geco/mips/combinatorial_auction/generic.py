import pyscipopt as scip


def combinatorial_auction(bids, n_dummy_items, n_items, name="Combinatorial Auction"):
    model = scip.Model(name)

    # add vars
    bids_per_item = [[] for item in range(n_items + n_dummy_items)]
    x = []
    for i, bid in enumerate(bids):
        bundle, price = bid
        var = model.addVar(lb=0, ub=1, obj=price, name=f"x_{i + 1}", vtype="B")
        x.append(var)
        for item in bundle:
            bids_per_item[item].append(i)

    # add constraints
    for item_bids in bids_per_item:
        if item_bids:
            vars = (x[i] for i in item_bids)
            model.addCons(scip.quicksum(vars) <= 1)
    model.setMaximize()
    return model
