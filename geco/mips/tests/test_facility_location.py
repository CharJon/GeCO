from geco.mips.facility_location import *


def test_capacitated_facility_location():
    n_customers, n_facilities, ratio = 25, 10, 2
    instance_params = cornuejols_instance_params(n_customers, n_facilities, ratio, seed=0)
    model = capacitated_facility_location(n_customers, n_facilities, *instance_params)
    assert model.getNVars() == n_customers * n_facilities + n_facilities
    assert model.getNConss() == n_customers + n_facilities + 1 + n_customers * n_facilities
    assert model.getObjectiveSense() == "minimize"
    model.optimize()
    assert 5856 <= model.getObjVal() <= 5857


def test_seeding():
    n_customers, n_facilities, ratio = 10, 10, 3
    params1 = cornuejols_instance_params(n_customers, n_facilities, ratio, seed=1)
    params2 = cornuejols_instance_params(n_customers, n_facilities, ratio, seed=2)
    something_different = False
    for param1, param2 in zip(params1, params2):
        if (param1 != param2).any():
            something_different = True
            break
    assert something_different
