import pytest

from geco.graphs.chimera import *


@pytest.mark.parametrize(
    "m, n, t",
    [
        (4, 4, 4),
        (4, 6, 4),
    ],
)
def test_chimera(m, n, t):
    g = chimera_graph(n, m, t)
    assert g.number_of_nodes() == m * n * t * 2
    assert g.number_of_edges() == 24 * m * n - (m + n) * t


@pytest.mark.parametrize(
    "m, n, t",
    [
        (4, 4, 4),
        (4, 6, 4),
    ],
)
def test_dwave_chimera(m, n, t):
    g = dwave_chimera_graph(m, n, t)
    assert g.number_of_nodes() == m * n * t * 2
    assert g.number_of_edges() == 24 * m * n - (m + n) * t


def test_odd_couplers_not_implemented():
    m, n, t = 2, 4, 2
    with pytest.raises(NotImplementedError):
        dwave_chimera_graph(n, m, t)


@pytest.mark.parametrize("m", [3, 5, 10])
def test_selby(m):
    graph = selby_c(m)
    assert graph.number_of_nodes() == m * m * 8
    assert graph.number_of_edges() == 24 * m * m - 8 * m
