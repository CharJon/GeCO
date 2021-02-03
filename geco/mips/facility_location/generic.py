import itertools

import numpy as np
import pyscipopt as scip
from networkx.utils import py_random_state


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
