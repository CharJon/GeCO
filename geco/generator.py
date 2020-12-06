import numpy as np


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


class CommonSubstructureGenerator:
    def __init__(self, generating_function, base_params, expansion_function, extra_parameter_generator):
        self.backbone = generating_function(*base_params)
        self.expansion_function = expansion_function
        self.extra_parameters_generator = extra_parameter_generator

    def __iter__(self):
        return self

    def __next__(self):
        return self.expansion_function(self.backbone, *self.extra_parameters_generator())
