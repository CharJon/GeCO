import itertools

import pytest

from geco.generator import *
from geco.mips.facility_location.cornuejols import cornuejols_instance
from geco.mips.set_cover.generic import *
from geco.mips.set_cover.sun import *


def test_generate():
    gen = generate(lambda seed: cornuejols_instance(10, 5, 2, seed))
    for model in itertools.islice(gen, 10):
        assert type(model) == scip.Model


def test_generate_n():
    n = 50
    gen = generate_n(lambda seed: cornuejols_instance(6, 3, 2, seed), n=n)
    all_models = []
    for i, model in gen:
        assert type(model) == scip.Model
        all_models.append(model)
    assert len(all_models) == n

    for model1, model2 in itertools.combinations(all_models, 2):
        obj_coeffs_1 = [v.getObj() for v in model1.getVars()]
        obj_coeffs_2 = [v.getObj() for v in model2.getVars()]
        assert obj_coeffs_1 != obj_coeffs_2


@pytest.mark.parametrize(
    "n,m,seed", itertools.product([10, 100, 200], [10, 100, 200], [0, 1, 1337, 53115])
)
def test_common_substructure_generator_set_cover(n, m, seed):
    gen = common_substructure_generator(
        instance_generation_function=set_cover,
        backbone=sun_params(n, m),
        expand_params_function=lambda backbone, seed: expand_sun_params(
            (n + 10, m), backbone, seed=seed
        ),
        seed=seed,
    )
    for model in itertools.islice(gen, 10):
        assert model.getNVars() == n + 10
        assert model.getNConss() == m
        assert model.getObjectiveSense() == "minimize"
