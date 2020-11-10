from geco.mips.facility_location import *


def test_capacitated_facility_location():
    n_customers, n_facilities, ratio, seed = 25, 10, 2, 0
    model = capacitated_facility_location(n_customers, n_facilities, ratio, seed)
    assert model.getNVars() == n_customers * n_facilities + n_facilities
    assert model.getNConss() == n_customers + n_facilities + 1 + n_customers * n_facilities
    assert model.getObjectiveSense() == "minimize"
    model.optimize()
    assert 5856 <= model.getObjVal() <= 5857
