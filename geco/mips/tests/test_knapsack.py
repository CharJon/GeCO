from geco.mips.knapsack import *


def test_knapsack():
    n = 100
    m_1 = knapsack(n)
    assert m_1.getNVars() == n
    assert m_1.getNConss() == 1
    assert m_1.getObjectiveSense() == 'maximize'
