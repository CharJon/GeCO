from geco.generator import *

import itertools


def test_generator():
    from geco.mips.facility_location import capacitated_facility_location
    gen = Generator(capacitated_facility_location, n_customers=10, n_facilities=3, ratio=2)
    gen.seed(0)
    for model in itertools.islice(gen, 10):
        print(model)
