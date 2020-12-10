import numpy as np
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
            seed for randomization

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
        Number of instances to generate
    seed: int, random state or None
            seed for randomization

    Returns
    -------
     Tuple (instance_number, instance)
    """
    for i in range(n):
        yield i, generating_function(seed)


class Generator:
    def __init__(self, generating_function, **parameter):
        self.generate_instance = generating_function
        self.parameter = parameter
        self.rng = np.random.RandomState()

    def __iter__(self):
        return self

    def __next__(self):
        return self.generate_instance(
            **self.parameter, seed=self.rng.randint(2 ** 32 - 1)
        )

    def seed(self, seed: int):
        self.rng.seed(seed)
