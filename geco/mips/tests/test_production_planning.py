from geco.mips.production_planning import *


def test_tang():
    T = 100
    m_1 = tang(T)
    assert m_1.getNVars() == (T + 1) * 3 - 1
    assert m_1.getNConss() == 2 * T + 2
    assert m_1.getObjectiveSense() == 'minimize'
