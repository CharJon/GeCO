from urllib.request import urlopen

FILES_BASE_URL = "http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/"


def read_number(line):
    if not line:
        return None
    return int(line.strip().split(b" ")[0])


def read_numbers(line):
    if len(line) == 0:
        return []
    return (int(n) for n in line.strip().split(b" "))


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


def zero_index(numbers):
    return map(lambda x: x - 1, numbers)


def orlib_load_instance(instance_name, reader):
    """

    Parameters
    ----------
    instance_name: str
        Name of instance file
    reader: function
        Takes a file-like object and returns the read model

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the loaded instance
    """
    content_as_file = urlopen(FILES_BASE_URL + instance_name)
    return reader(content_as_file)
