from geco.mips.facility_location import *


def test_capacitated_facility_location():
    n_customers, n_facilities, ratio = 25, 10, 2
    m_1 = capacitated_facility_location(n_customers, n_facilities, ratio)
    assert m_1.getNVars() == n_customers * n_facilities + n_facilities
    assert m_1.getNConss() == n_customers + n_facilities + 1 + n_customers * n_facilities
    assert m_1.getObjectiveSense() == "minimize"
    m_1.optimize()
    assert 5679 <= m_1.getObjVal() <= 5680
