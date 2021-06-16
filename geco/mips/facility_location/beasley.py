import numpy as np
from networkx.utils import random_state

from geco.mips.facility_location.generic import capacitated_facility_location


@random_state(-1)
def beasley_instance(n_customers, n_facilities, capacity, n_desired_open, seed=0):
    """
    Generates a Capacitated Facility Location MIP formulation following [1].

    Parameters
    ----------
    n_customers: int
        Number of customers
    n_facilities: int
        Number of facilities
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] Beasley, J. E. (1988).
    An algorithm for solving large capacitated warehouse location problems.
    European Journal of Operational Research, 33(3), 314-325.
    """
    return capacitated_facility_location(
        n_customers,
        n_facilities,
        *beasley_params(n_customers, n_facilities, capacity, n_desired_open, seed),
    )


@random_state(-1)
def beasley_params(n_customers, n_facilities, capacity, n_desired_open, seed=0):
    """
    Generates a Capacitated Facility Location instance params following [1].

    Parameters
    ----------
    n_customers: int
        Number of customers
    n_facilities: int
        Number of facilities
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    trans_costs: numpy array [float]
        Matrix of transportation costs from customer i to facility j [i,j]
    demands: numpy array [int]
        Demands of each customer
    fixed_costs: numpy array [int]
        Fixed costs of operating each facility
    capacities: numpy array [int]
        Capacities of each facility

    References
    ----------
    .. [1] Beasley, J. E. (1988).
    An algorithm for solving large capacitated warehouse location problems.
    European Journal of Operational Research, 33(3), 314-325.
    """
    # locations for customers
    # in a 1000 x 1000 square
    customer_x = seed.randint(0, 1000 + 1, size=n_customers)
    customer_y = seed.randint(0, 1000 + 1, size=n_customers)

    # locations for facilities
    # in a 1000 x 1000 square
    facility_x = seed.randint(0, 1000 + 1, size=n_facilities)
    facility_y = seed.randint(0, 1000 + 1, size=n_facilities)

    euclidean_distances = np.sqrt(
        (customer_x.reshape((-1, 1)) - facility_x.reshape((1, -1))) ** 2
        + (customer_y.reshape((-1, 1)) - facility_y.reshape((1, -1))) ** 2
    )

    # random int [1,100]
    demands = seed.randint(1, 100 + 1, size=n_customers)
    # proportional to euclidean distance times random number from [1, 1.25]
    trans_costs = (euclidean_distances
                   * seed.uniform(1.0, 1.25, size=(n_customers, n_facilities))
                   * demands.reshape((-1, 1)))

    # same capacity for all
    capacities = np.full(n_facilities, capacity)

    one_more = seed.choice(np.arange(n_facilities), size=n_desired_open + 1, replace=False)
    d_1 = sum(np.min(trans_costs[:, one_more], axis=1))
    one_less = seed.choice(one_more, size=n_desired_open - 1, replace=False)
    d_2 = sum(np.min(trans_costs[:, one_less], axis=1))
    fixed_costs = seed.uniform(0.75, 1.25, size=n_facilities) * ((d_2 - d_1) / 2)

    return trans_costs, demands, fixed_costs, capacities
