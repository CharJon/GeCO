from geco.graphs.pegasus import *

import pytest


@pytest.fixture
def g_dwave():
    return dwave_pegasus_graph(6)


def test_nodes(g_dwave):
    # calculated from 8(3M − 1)(M − 1)
    assert g_dwave.number_of_nodes() == 8 * (3 * 6 - 1) * (6 - 1)


def test_edges(g_dwave):
    # from the p6 example in dwave's paper
    assert g_dwave.number_of_edges() == 4484
