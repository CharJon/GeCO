import pyscipopt as scip
import geco.mips.loading.orlib as orlib
from geco.mips.facility_location.generic import capacitated_warehouse_location


def cap_numeric_reader(file):
    """
    Reads cap(NUMBER) Capacitated Warehouse Location instance params mentioned in [1].

    Parameters
    ----------
    file: file-like object

    Returns
    -------
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

    References
    ----------
    ..[1] http://people.brunel.ac.uk/~mastjjb/jeb/orlib/capinfo.html
    """
    num_of_warehouses, num_of_customers = orlib.read_numbers(file.readline())
    capacities = []
    fixed_costs = []
    demands = []
    allocation_cost_per_warehouse = {}

    for _ in range(num_of_warehouses):
        capacity, fixed_cost = orlib.read_numbers(file.readline())
        capacities.append(capacity)
        fixed_costs.append(fixed_cost)

    for i in range(num_of_customers):
        demand = orlib.read_number(file.readline())
        allocation_costs = orlib.read_multiline_numbers(file, num_of_warehouses)
        demands.append(demand)
        for j, cost in enumerate(allocation_costs):
            allocation_cost_per_warehouse[i, j] = cost

    return (
        num_of_customers,
        num_of_warehouses,
        allocation_cost_per_warehouse,
        demands,
        fixed_costs,
        capacities,
    )


def cap_alpha_reader(file, capacity):
    """
    Reads cap(LETTER) Capacitated Warehouse Location instance params mentioned in [1].

    Parameters
    ----------
    file: file-like object

    Returns
    -------
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

    References
    ----------
    ..[1] http://people.brunel.ac.uk/~mastjjb/jeb/orlib/capinfo.html
    """
    num_of_warehouses, num_of_customers = orlib.read_numbers(file.readline())
    capacities = []
    fixed_costs = []
    demands = []
    allocation_cost_per_warehouse = {}

    for _ in range(num_of_warehouses):
        capacity, fixed_cost = capacity, float(file.readline().strip().split(b" ")[-1])
        capacities.append(capacity)
        fixed_costs.append(fixed_cost)

    for i in range(num_of_customers):
        demand = orlib.read_number(file.readline())
        allocation_costs = orlib.read_multiline_numbers(file, num_of_warehouses)
        demands.append(demand)
        for j, cost in enumerate(allocation_costs):
            allocation_cost_per_warehouse[i, j] = cost

    return (
        num_of_customers,
        num_of_warehouses,
        allocation_cost_per_warehouse,
        demands,
        fixed_costs,
        capacities,
    )


PSET_CAPACITIES = {
    "a": [8_000, 10_000, 12_000, 14_000],
    "b": [5_000, 6_000, 7_000, 8_000],
    "c": [5_000, 5_750, 6_500, 7_250],
}


def orlib_instance(instance_name):
    """
    Loads an orlib Capacitated Warehouse Location instance

    Parameters
    ----------
    instance_name: str
        Name of the capacitated warehouse location file. example: "cap41.txt"
        for files from problem sets A,B,C. To get the first problem of problem set A
        pass instance_name as "capa1.txt"

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the loaded instance
    """
    # TODO: assert that instance_name correlated to one of the listed capacitated warehouse location files
    if instance_name[:3] == "cap" and instance_name[3].isnumeric():
        return orlib.orlib_load_instance(
            instance_name,
            reader=cap_numeric_reader,
            formulation=capacitated_warehouse_location,
        )
    elif instance_name[:3] == "cap" and instance_name[3].isalpha():
        problem_number = int(instance_name[4])
        problem_set = instance_name[3]
        capacity = PSET_CAPACITIES[problem_set][problem_number - 1]
        return orlib.orlib_load_instance(
            instance_name[:4] + ".txt",
            reader=lambda file: cap_alpha_reader(file, capacity),
            formulation=capacitated_warehouse_location,
        )
    else:
        raise ValueError(
            f'"{instance_name}" is not a valid file name for Capacitated Warehouse Location'
            f"files listed in http://people.brunel.ac.uk/~mastjjb/jeb/orlib/capinfo.html"
        )
