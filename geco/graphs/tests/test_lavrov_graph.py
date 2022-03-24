import networkx as nx
import pytest

from geco.graphs.lavrov_graph import lavrov_graph


@pytest.mark.parametrize(
    "k", [-10, -1, 0, 1, 2]
)
def test_lavrov_graph_wrong_k(k):
    with pytest.raises(ValueError) as e_info:
        g = lavrov_graph(k)


@pytest.mark.parametrize(
    "k", [2 ** k for k in range(2, 10)]
)
def test_lavrov_graph_properties(k):
    g = lavrov_graph(k)
    assert g.number_of_nodes() == k * 2
    assert g.number_of_edges() == k * 4
    assert all(d == 4 for v, d in g.degree)
    assert sum(1 for _ in nx.connected_components(g)) == 1


def test_lavrov_graph_edges():
    g = lavrov_graph(5)
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0),  # inner cycle
             (5, 6), (6, 7), (7, 8), (8, 9), (9, 5),  # outer cycle
             (5, 1), (6, 2), (7, 3), (8, 4), (9, 0),  # forward cross
             (5, 4), (9, 3), (8, 2), (7, 1), (6, 0)]  # backward cross

    for a, b in edges:
        assert g.has_edge(a, b)
