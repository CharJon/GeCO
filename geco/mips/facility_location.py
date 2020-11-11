import itertools

import numpy as np
import pyscipopt as scip
from networkx.utils import py_random_state


def capacitated_facility_location(n_customers, n_facilities, transportation_cost, demands, fixed_costs, capacities):
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
    transportation_cost:
        Matrix of transportation costs from customer i to facility j [i,j]
    demands: numpy array [int]
        Demands of each customer.
    fixed_costs: numpy array [int]
        Fixed costs of operating each facility.
    capacities: numpy array [int]
        Capacities of each facility.
    """
    total_demand = demands.sum()
    total_capacity = capacities.sum()

    model = scip.Model("Capacitated Facility Location")

    model.setMinimize()

    customer_facility_vars = {}
    facility_vars = []
    # add customer-facility vars
    for i, j in itertools.product(range(n_customers), range(n_facilities)):
        var = model.addVar(lb=0, ub=1, obj=transportation_cost[i, j], name=f"x_{i}_{j}", vtype="B")
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


@py_random_state(3)
def cornuejols_instance_params(n_customers, n_facilities, ratio, seed):
    # locations for customers
    c_x = np.array([seed.random() for _ in range(n_customers)])
    c_y = np.array([seed.random() for _ in range(n_customers)])

    # locations for facilities
    f_x = np.array([seed.random() for _ in range(n_facilities)])
    f_y = np.array([seed.random() for _ in range(n_facilities)])

    demands = np.array(seed.sample(range(5, 35 + 1), k=n_customers))
    capacities = np.array(seed.sample(range(10, 160 + 1), k=n_facilities))
    fixed_costs = np.array(seed.sample(range(100, 110 + 1), k=n_facilities) * np.sqrt(capacities)) + np.array(
        seed.sample(range(90 + 1), k=n_facilities))
    fixed_costs = fixed_costs.astype(int)

    # adjust capacities according to ratio
    total_demand = demands.sum()
    total_capacity = capacities.sum()
    capacities = capacities * ratio * total_demand / total_capacity
    capacities = capacities.astype(int)

    # transportation cost
    trans_costs = np.sqrt(
        (c_x.reshape((-1, 1)) - f_x.reshape((1, -1))) ** 2 \
        + (c_y.reshape((-1, 1)) - f_y.reshape((1, -1))) ** 2) * 10 * demands.reshape((-1, 1))
    return trans_costs, demands, fixed_costs, capacities