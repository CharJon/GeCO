import itertools

import pytest

from geco.generator import *
from geco.mips.set_cover import *


def test_generator():
    from geco.mips.facility_location import cornuejols_instance

    gen = Generator(cornuejols_instance, n_customers=10, n_facilities=3, ratio=2)
    gen.seed(0)
    for model in itertools.islice(gen, 10):
        assert type(model) == scip.Model


@pytest.mark.parametrize(
    "n,m,seed", itertools.product([10, 100, 200], [10, 100, 200], [0, 1, 1337, 53115])
)
def test_common_substructure_generator_set_cover(n, m, seed):
    gen = common_substructure_generator(
        instance_generation_function=set_cover,
        backbone=sun_params(n, m),
        expand_params_function=lambda backbone, seed: expand_sun_params((n + 10, m), backbone, seed=seed),
        seed=seed,
    )
    for model in itertools.islice(gen, 10):
        assert model.getNVars() == n + 10
        assert model.getNConss() == m
        assert model.getObjectiveSense() == "minimize"
