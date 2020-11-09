from geco.graphs.chimera import *

import pytest


@pytest.fixture()
def g1():
    return chimera_graph(4, 4, 4)


@pytest.fixture
def g2():
    return chimera_graph(4, 6, 4)


@pytest.fixture
def g_dwave():
    return dwave_chimera_graph(4)


def test_nodes(g1, g2, g_dwave):
    # calculated from m * n * t * 2
    assert g1.number_of_nodes() == 4 * 4 * 4 * 2
    assert g2.number_of_nodes() == 4 * 6 * 4 * 2
    assert g_dwave.number_of_nodes() == 4 * 4 * 4 * 2


def test_edges(g1, g2, g_dwave):
    # calculated from 24 * m * n - (m+n) * t
    assert g1.number_of_edges() == 24 * 4 * 4 - (4 + 4) * 4
    assert g2.number_of_edges() == 24 * 6 * 4 - (4 + 6) * 4
    assert g_dwave.number_of_edges() == 24 * 4 * 4 - 8 * 4
