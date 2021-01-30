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
        constraint = map(lambda x: x - 1, constraint)  # make it zero-indexed
        sets.append(constraint)
    assert len(costs) == number_of_vars and len(sets) == number_of_cons
    return set_cover(costs, sets)


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
    raise NotImplementedError


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
