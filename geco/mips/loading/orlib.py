from urllib.request import urlopen

FILES_BASE_URL = "http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/"


def read_number(line):
    if not line:
        return None
    return _str_to_number(line.strip().split(b" ")[0])


def read_numbers(line):
    return (_str_to_number(n) for n in line.strip().split(b" "))


def read_multiline_numbers(file, number_to_read):
    numbers = []
    while file:
        if len(numbers) == number_to_read:
            break
        elif len(numbers) > number_to_read:
            raise ValueError("Found more numbers than expected")
        else:
            line = file.readline()
            numbers_in_line = list(read_numbers(line))
            numbers += numbers_in_line
    return numbers


def _str_to_number(string):
    if b"." in string:
        return float(string)
    else:
        return int(string)


def zero_index(numbers):
    return map(lambda x: x - 1, numbers)


def orlib_load_instance(instance_name, reader, formulation):
    """
    Parameters
    ----------
    instance_name: str
        Name of instance file
    reader: function (file) -> params: tuple
        Takes a file-like object and returns the read parameters
    formulation: function (params: tuple) -> scip.model
        Takes a tuple of params and returns the generated model

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the loaded instance

    References
    ----------
    ..[1] http://people.brunel.ac.uk/~mastjjb/jeb/info.html
    """

    content_as_file = urlopen(FILES_BASE_URL + instance_name)
    params = reader(content_as_file)
    return formulation(*params)
