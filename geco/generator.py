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
    instance_params_generation_function,
    base_params,
    new_params,
    expand_params_function,
    seed=0,
):
    """
    Generates instances that have common substructure

    Parameters
    ----------
    instance_generation_function:
        base function that defines MIP
    instance_params_generation_function:
        function to generate parameters for instance_generation_function
    base_params:
        parameters for the common substructure
    new_params:
        parameters for the required expanded instance
    expand_params_function:
        function to expand instance params using new_params
    seed: int, random object or None
        for randomization

    Returns
    -------
        generator object
    """
    while True:
        base_result = instance_params_generation_function(*base_params, seed=seed)
        yield instance_generation_function(
            *expand_params_function(new_params, base_result, seed=seed)
        )
