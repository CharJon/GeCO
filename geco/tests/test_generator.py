import itertools

import pyscipopt as scip
from geco.generator import *


def test_generator():
    from geco.mips.facility_location import cornuejols_instance

    gen = Generator(cornuejols_instance, n_customers=10, n_facilities=3, ratio=2)
    gen.seed(0)
    for model in itertools.islice(gen, 10):
        assert type(model) == scip.Model
