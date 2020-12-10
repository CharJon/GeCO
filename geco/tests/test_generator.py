import itertools

import pyscipopt as scip

from geco.generator import *
from geco.mips.facility_location import cornuejols_instance


def test_generator_class():
    gen = Generator(cornuejols_instance, n_customers=10, n_facilities=3, ratio=2)
    gen.seed(0)
    for model in itertools.islice(gen, 10):
        assert type(model) == scip.Model


def test_generate():
    gen = generate(lambda seed: cornuejols_instance(10, 5, 2, seed))
    for model in itertools.islice(gen, 10):
        assert type(model) == scip.Model


def test_generate_n():
    gen = generate_n(lambda seed: cornuejols_instance(6, 3, 2, seed), n=400)
    all_models = []
    for i, model in gen:
        assert type(model) == scip.Model
        all_models.append(model)
    assert len(all_models) == 400
