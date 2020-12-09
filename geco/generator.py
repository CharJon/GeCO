import numpy as np
from networkx.utils import py_random_state


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


@py_random_state(-1)
def common_substructure_generator(
    instance_generation_function,
    backbone,
    expand_params_function,
    seed=0,
):
    """
    Generates instances that have common substructure

    Parameters
    ----------
    instance_generation_function:
        base function that defines MIP
    backbone:
        instance parameters of the common substructure
    expand_params_function:
        function to expand instance params given a backbone and a seed
    seed: int, random object or None
        for randomization

    Returns
    -------
        generator object
    """
    while True:
        yield instance_generation_function(*expand_params_function(backbone, seed=seed))
