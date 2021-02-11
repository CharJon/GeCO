import pyscipopt as scip

from geco.mips.loading.orlib import *
from geco.mips.set_cover.generic import set_cover
from geco.mips.loading.orlib import orlib_load_instance
from geco.mips.set_cover.generic import set_cover


def scp_reader(file):
    """
    Reads scp set-cover instances mentioned in [1].

    Parameters
    ----------
    file: file-like object

    Returns
    -------
    costs: list[int]
        Element costs in objective function
    sets: list[set]
        Definition of element requirement for each set

    References
    ----------
    ..[1] http://people.brunel.ac.uk/~mastjjb/jeb/orlib/scpinfo.html
    """

    number_of_cons, number_of_vars = read_numbers(file.readline())
    costs = read_multiline_numbers(file, number_of_vars)
    sets = []
    while file:
        number_of_vars_in_constraint = read_number(file.readline())
        if not number_of_vars_in_constraint:
            break
        constraint = list(read_multiline_numbers(file, number_of_vars_in_constraint))
        constraint = zero_index(constraint)
        sets.append(constraint)
    assert len(costs) == number_of_vars and len(sets) == number_of_cons
    return costs, sets


def rail_reader(file):
    """
    Reads rail set-cover instances mentioned in [1].

    Parameters
    ----------
    file: file-like object

    Returns
    -------
    costs: list[int]
        Element costs in objective function
    sets: list[set]
        Definition of element requirement for each set

    References
    ----------
    ..[1] http://people.brunel.ac.uk/~mastjjb/jeb/orlib/scpinfo.html
    """

    number_of_cons, number_of_vars = read_numbers(file.readline())

    costs = []
    sets = [[] for _ in range(number_of_cons)]
    col_idx = 0
    while file:
        line = file.readline()
        if not line:
            break

        numbers = list(read_numbers(line))
        costs.append(numbers[0])
        rows_covered = zero_index(numbers[2:])

        for row in rows_covered:
            sets[row].append(col_idx)
        col_idx += 1
    sets = list(filter(lambda l: len(l) > 0, sets))
    assert len(costs) == number_of_vars and len(sets) == number_of_cons
    return costs, sets


def orlib_instance(instance_name):
    """
    Loads an orlib Set-cover instance

    Parameters
    ----------
    instance_name: str
        Name of the set-cover file. example: "scp41.txt"

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the loaded instance
    """
    # TODO: assert that instance_name correlated to one of the listed set-cover files
    if instance_name[:3] == "scp":
        return orlib_load_instance(
            instance_name, reader=scp_reader, formulation=set_cover
        )
    elif instance_name[:4] == "rail":
        return orlib_load_instance(
            instance_name, reader=rail_reader, formulation=set_cover
        )
