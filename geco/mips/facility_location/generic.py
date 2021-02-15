import itertools

import pyscipopt as scip


def capacitated_facility_location(
    n_customers,
    n_facilities,
    transportation_cost,
    demands,
    fixed_costs,
    capacities,
    name="Capacitated Facility Location",
):
    """
    Generate a Capacitated Facility Location MIP formulation following [1].

    Parameters
    ----------
    n_customers: int
        The desired number of customers
    n_facilities: int
        The desired number of facilities
    transportation_cost: numpy array [float]
        Matrix of transportation costs from customer i to facility j [i,j]
    demands: numpy array [int]
        Demands of each customer
    fixed_costs: numpy array [int]
        Fixed costs of operating each facility
    capacities: numpy array [int]
        Capacities of each facility
    name: str
        Name of the model

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] Cornuejols G, Sridharan R, Thizy J-M (1991)
        A Comparison of Heuristics and Relaxations for the Capacitated Plant Location Problem.
        European Journal of Operations Research 50:280-297.
    """
    model = scip.Model(name)

    total_demand = demands.sum()

    model.setMinimize()

    customer_facility_vars = {}
    facility_vars = []
    # add customer-facility vars
    for i, j in itertools.product(range(n_customers), range(n_facilities)):
        var = model.addVar(
            lb=0, ub=1, obj=transportation_cost[i, j], name=f"x_{i}_{j}", vtype="B"
        )
        customer_facility_vars[i, j] = var
    # add facility vars
    for j in range(n_facilities):
        var = model.addVar(lb=0, ub=1, obj=fixed_costs[j], name=f"y_{j}", vtype="B")
        facility_vars.append(var)

    # add constraints
    for i in range(n_customers):
        model.addCons(
            scip.quicksum(customer_facility_vars[i, j] for j in range(n_facilities))
            >= 1
        )
    for j in range(n_facilities):
        model.addCons(
            scip.quicksum(
                demands[i] * customer_facility_vars[i, j] for i in range(n_customers)
            )
            <= capacities[j] * facility_vars[j]
        )

    # optional constraints

    # total capacity constraint
    model.addCons(
        scip.quicksum(capacities[j] * facility_vars[j] for j in range(n_facilities))
        >= total_demand
    )

    # affectation constraints
    for i, j in itertools.product(range(n_customers), range(n_facilities)):
        model.addCons(customer_facility_vars[i, j] <= facility_vars[j])

    return model


def capacitated_warehouse_location(
    n_customers,
    n_facilities,
    transportation_cost,
    demands,
    fixed_costs,
    capacities,
    name="Capacitated Warehouse Location",
):
    """
    Generate a Capacitated Warehouse Location MIP formulation following [1].

    Parameters
    ----------
    n_customers: int
        The desired number of customers
    n_facilities: int
        The desired number of warehouses
    transportation_cost: numpy array [float]
        Matrix of transportation costs from customer i to warehouse j [i,j]
    demands: numpy array [int]
        Demands of each customer
    fixed_costs: numpy array [int]
        Fixed costs of operating each warehouse
    capacities: numpy array [int]
        Capacities of each warehouse
    name: str
        Name of the model

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] J.E. Beasley, An algorithm for solving large capacitated warehouse location problems,
        European Journal of Operational Research, Volume 33, Issue 3, 1988,
        Pages 314-325, ISSN 0377-2217,
        https://doi.org/10.1016/0377-2217(88)90175-0.
    """
    model = scip.Model(name)

    model.setMinimize()

    customer_facility_vars = {}
    facility_vars = []

    # add customer-facility vars
    for i, j in itertools.product(range(n_customers), range(n_facilities)):
        var = model.addVar(
            lb=0, ub=1, obj=transportation_cost[i, j], name=f"x_{i}_{j}", vtype="C"
        )
        customer_facility_vars[i, j] = var

    # add facility vars
    for j in range(n_facilities):
        var = model.addVar(lb=0, ub=1, obj=fixed_costs[j], name=f"y_{j}", vtype="B")
        facility_vars.append(var)

    # add constraints

    # constraints (2)
    for i in range(n_customers):
        model.addCons(
            scip.quicksum(customer_facility_vars[i, j] for j in range(n_facilities))
            >= 1
        )

    # constraints (3)
    for j in range(n_facilities):
        model.addCons(
            scip.quicksum(
                demands[i] * customer_facility_vars[i, j] for i in range(n_customers)
            )
            <= capacities[j] * facility_vars[j]
        )

    # constraints (4) and (5) are skipped because no data of bounds are given in problem data in OR-Library

    # constraints (6)
    for i, j in itertools.product(range(n_customers), range(n_facilities)):
        model.addCons(
            customer_facility_vars[i, j]
            <= min(1, capacities[j] / demands[i]) * facility_vars[j]
        )

    return model
