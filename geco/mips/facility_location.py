import itertools

import numpy as np
import pyscipopt as scip
from networkx.utils import py_random_state


@py_random_state(3)
def capacitated_facility_location(n_customers, n_facilities, ratio, seed=0):
    """
    Generate a Capacited Facility Location problem following
        Cornuejols G, Sridharan R, Thizy J-M (1991)
        A Comparison of Heuristics and Relaxations for the Capacitated Plant Location Problem.
        European Journal of Operations Research 50:280-297.
    Returns a SCIP model.
    Parameters
    ----------
    n_customers: int
        The desired number of customers.
    n_facilities: int
        The desired number of facilities.
    ratio: float
        The desired capacity / demand ratio.
    seed: integer, random_state, or None
        Indicator of random number generation state.
    """
    # locations for customers
    c_x = np.array([seed.random() for _ in range(n_customers)])
    c_y = np.array([seed.random() for _ in range(n_customers)])

    # locations for facilities
    f_x = np.array([seed.random() for _ in range(n_facilities)])
    f_y = np.array([seed.random() for _ in range(n_facilities)])

    demands = np.array(seed.sample(range(5, 35 + 1), k=n_customers))
    capacities = np.array(seed.sample(range(10, 160 + 1), k=n_facilities))
    fixed_costs = np.array(seed.sample(range(100, 110 + 1), k=n_facilities) * np.sqrt(capacities)) \
                  + np.array(seed.sample(range(90 + 1), k=n_facilities))
    fixed_costs = fixed_costs.astype(int)

    total_demand = demands.sum()
    total_capacity = capacities.sum()

    # adjust capacities according to ratio
    capacities = capacities * ratio * total_demand / total_capacity
    capacities = capacities.astype(int)
    total_capacity = capacities.sum()

    # transportation costs
    trans_costs = np.sqrt(
        (c_x.reshape((-1, 1)) - f_x.reshape((1, -1))) ** 2 \
        + (c_y.reshape((-1, 1)) - f_y.reshape((1, -1))) ** 2) * 10 * demands.reshape((-1, 1))

    model = scip.Model("Capacitated Facility Location")

    model.setMinimize()

    customer_facility_vars = {}
    facility_vars = []
    # add customer-facility vars
    for i, j in itertools.product(range(n_customers), range(n_facilities)):
        var = model.addVar(lb=0, ub=1, obj=trans_costs[i, j], name=f"x_{i}_{j}", vtype="B")
        customer_facility_vars[i, j] = var
    # add facility vars
    for j in range(n_facilities):
        var = model.addVar(lb=0, ub=1, obj=fixed_costs[j], name=f"y_{j}", vtype="B")
        facility_vars.append(var)

    # add constraints
    for i in range(n_customers):
        model.addCons(scip.quicksum(customer_facility_vars[i, j] for j in range(n_facilities)) >= 1)
    for j in range(n_facilities):
        model.addCons(
            scip.quicksum(demands[i] * customer_facility_vars[i, j] for i in range(n_customers))
            <= capacities[j] * facility_vars[j])

    # optional constraints

    # total capacity constraint
    model.addCons(scip.quicksum(capacities[j] * facility_vars[j] for j in range(n_facilities)) >= total_demand)

    # affectation constraints
    for i, j in itertools.product(range(n_customers), range(n_facilities)):
        model.addCons(customer_facility_vars[i, j] <= facility_vars[j])

    return model
