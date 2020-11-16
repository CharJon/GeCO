import pytest

from geco.mips.facility_location import *


def test_capacitated_facility_location():
    n_customers, n_facilities, ratio = 25, 10, 2
    instance_params = cornuejols_instance_params(n_customers, n_facilities, ratio, seed=0)
    model = capacitated_facility_location(n_customers, n_facilities, *instance_params)
    assert model.getNVars() == n_customers * n_facilities + n_facilities
    assert model.getNConss() == n_customers + n_facilities + 1 + n_customers * n_facilities
    assert model.getObjectiveSense() == "minimize"
    model.hideOutput()
    model.optimize()
    assert 5403 <= model.getObjVal() <= 5404


@pytest.mark.parametrize("n_customers, n_facilities, ratio ,seed1, seed2",
                         itertools.product([3, 10, 15], [3, 10, 15], [1, 2], [0, 1, 1337, 53115],
                                           [0, 1, 1337, 53115]))
def test_seeding(n_customers, n_facilities, ratio, seed1, seed2):
    params1 = cornuejols_instance_params(n_customers, n_facilities, ratio, seed=seed1)
    params2 = cornuejols_instance_params(n_customers, n_facilities, ratio, seed=seed2)
    something_different = False
    for param1, param2 in zip(params1, params2):
        if (param1 != param2).any():
            something_different = True
            break
    assert seed1 == seed2 or something_different
