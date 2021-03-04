import itertools

import pytest

from geco.graphs.chimera import *


@pytest.mark.parametrize(
    "m, n, t",
    itertools.product(
        [2, 4, 6],
        [2, 4, 6],
        [2, 4, 6],
    ),
)
def test_chimera(m, n, t):
    g = chimera_graph(n, m, t)
    assert g.number_of_nodes() == m * n * t * 2
    assert g.number_of_edges() == n * m * t * t + n * (m - 1) * t + m * (n - 1) * t


@pytest.mark.parametrize(
    "m, n, t",
    itertools.product(
        [2, 4, 6],
        [2, 4, 6],
        [2, 4, 6],
    ),
)
def test_dwave_chimera(m, n, t):
    g = dwave_chimera_graph(m, n, t)
    assert g.number_of_nodes() == m * n * t * 2
    assert g.number_of_edges() == n * m * t * t + n * (m - 1) * t + m * (n - 1) * t


@pytest.mark.parametrize("m", [3, 5, 10])
def test_selby(m):
    graph = selby_c(m)
    assert graph.number_of_nodes() == m * m * 8
    assert graph.number_of_edges() == 24 * m * m - 8 * m


@pytest.mark.parametrize("m, faulty", itertools.product([3, 8, 10], [20, 50, 73]))
def test_mgw(m, faulty):
    graph = mgw(m=m, faulty=faulty)
    assert graph.number_of_nodes() == m * m * 8
    max_degree = 6
    maximum_edges_connected_to_faulty_nodes = faulty * max_degree
    assert (
        graph.number_of_edges()
        >= (24 * m * m - 8 * m) - maximum_edges_connected_to_faulty_nodes
    )
