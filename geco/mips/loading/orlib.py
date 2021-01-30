from urllib.request import urlopen

FILES_BASE_URL = "http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/"


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
