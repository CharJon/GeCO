import pyscipopt as scip
import geco.mips.loading.orlib as orlib
from geco.mips.facility_location.generic import capacitated_warehouse_location


def _cap_numeric_reader(file):
    """
    Reads cap(NUMBER) Capacitated Warehouse Location instances mentioned in [1].

    Parameters
    ----------
    file: file-like object

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the loaded instance

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

    return capacitated_warehouse_location(
        n_customers=num_of_customers,
        n_facilities=num_of_warehouses,
        transportation_cost=allocation_cost_per_warehouse,
        demands=demands,
        capacities=capacities,
        fixed_costs=fixed_costs,
    )


def _cap_alpha_reader():
    raise NotImplementedError


def orlib_instance(instance_name):
    """
    Loads an orlib Capacitated Warehouse Location instance

    Parameters
    ----------
    instance_name: str
        Name of the set-cover file. example: "scp41.txt"

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the loaded instance
    """
    # TODO: assert that instance_name correlated to one of the listed capacitated warehouse location files
    if instance_name[:3] == "cap" and instance_name[3].isnumeric():
        return orlib.orlib_load_instance(instance_name, reader=_cap_numeric_reader)
    elif instance_name[:3] == "cap" and instance_name[3].isalpha():
        return orlib.orlib_load_instance(instance_name, reader=_cap_alpha_reader)
    else:
        raise ValueError(
            f'"{instance_name}" is not a valid file name for Capacitated Warehouse Location'
            f"files listed in http://people.brunel.ac.uk/~mastjjb/jeb/orlib/capinfo.html"
        )
