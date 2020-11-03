from geco.mips.facility_location import *


def test_capacited_facility_location():
    n_customers, n_facilities, ratio = 50, 500, 0.5
    m_1 = capacitated_facility_location(n_customers, n_facilities, ratio)
    assert m_1.getNVars() == n_customers * n_facilities + n_facilities
    assert m_1.getNConss() == n_customers + n_facilities + 1 + n_customers * n_facilities
    assert m_1.getObjectiveSense() == "minimize"
