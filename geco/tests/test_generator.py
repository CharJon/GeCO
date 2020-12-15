import itertools

import pyscipopt as scip

from geco.generator import *
from geco.mips.facility_location import cornuejols_instance


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
