from networkx.utils import py_random_state


@py_random_state(-1)
def generate(generating_function, seed=0):
    """
    Convenience wrapper to generate multiple instances.

    Parameters
    ----------
    generating_function:
        A function that accepts a seed and returns an instance.
    seed: int, random state or None
        seed for randomization.

    Returns
    -------
     A pyscipopt model.
    """
    while True:
        yield generating_function(seed)


@py_random_state(-1)
def generate_n(generating_function, n, seed=0):
    """
    Convenience wrapper to generate n instances.

    Parameters
    ----------
    generating_function:
        A function that accepts a seed and returns an instance.
    n: int
        Number of instances to generate.
    seed: int, random state or None
        seed for randomization.

    Returns
    -------
     Tuple (instance_number, instance)
    """
    for i in range(n):
        yield i, generating_function(seed)
