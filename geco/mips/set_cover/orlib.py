import pyscipopt as scip
from geco.mips.loading.orlib import orlib_load_instance
from geco.mips.set_cover.generic import set_cover


def _read_number(line):
    if not line:
        return None
    return int(line.strip().split(b" ")[0])


def _read_numbers(line):
    if len(line) == 0:
        return []
    return (int(n) for n in line.strip().split(b" "))


def _read_multiline_numbers(file, number_to_read):
    costs = []
    while file:
        if len(costs) >= number_to_read:
            break
        else:
            line = file.readline()
            numbers = list(_read_numbers(line))
            costs += numbers
    return costs


def _scp_reader(file):
    """
    Reads scp set-cover instances mentioned in [1].

    Parameters
    ----------
    file: file-like object

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the loaded instance

    References
    ----------
    ..[1] http://people.brunel.ac.uk/~mastjjb/jeb/orlib/scpinfo.html
    """
    number_of_cons, number_of_vars = _read_numbers(file.readline())
    costs = _read_multiline_numbers(file, number_of_vars)
    sets = []
    while file:
        number_of_vars_in_constraint = _read_number(file.readline())
        if not number_of_vars_in_constraint:
            break
        constraint = list(_read_multiline_numbers(file, number_of_vars_in_constraint))
        constraint = _zero_index(constraint)
        sets.append(constraint)
    assert len(costs) == number_of_vars and len(sets) == number_of_cons
    return set_cover(costs, sets)


def _zero_index(numbers):
    return map(lambda x: x - 1, numbers)


def _rail_reader(file):
    """
    Reads rail set-cover instances mentioned in [1].

    Parameters
    ----------
    file: file-like object

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the loaded instance

    References
    ----------
    ..[1] http://people.brunel.ac.uk/~mastjjb/jeb/orlib/scpinfo.html
    """
    number_of_cons, number_of_vars = _read_numbers(file.readline())
    costs = []
    sets = [[] for _ in range(number_of_cons)]
    col_idx = 0
    while file:
        line = file.readline()
        if not line:
            break
        numbers = list(_read_numbers(line))
        costs.append(numbers[0])
        rows_covered = _zero_index(numbers[2:])
        for row in rows_covered:
            sets[row].append(col_idx)
        col_idx += 1
    sets = list(filter(lambda l: len(l) > 0, sets))
    assert len(costs) == number_of_vars and len(sets) == number_of_cons
    return set_cover(costs, sets)


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
    if instance_name[:3] == "scp":  # prefix of set cover files
        return orlib_load_instance(instance_name, reader=_scp_reader)
    elif instance_name[:4] == "rail":
        return orlib_load_instance(instance_name, reader=_rail_reader)
