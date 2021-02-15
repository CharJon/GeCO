import networkx as nx
import pytest

from geco.graphs.utilities import *


def test_edge_properties():
    num_nodes = 7
    graph = nx.path_graph(num_nodes)
    for u, v, data in graph.edges(data=True):
        data["weight"] = u

    max_weight, min_weight, num_of_zero_weighted = edgeweight_properties(graph)
    assert max_weight == num_nodes - 2
    assert min_weight == 0
    assert num_of_zero_weighted == 1


@pytest.mark.parametrize("n", [3, 10, 100])
def test_graph_properties(n):
    graph = nx.path_graph(n)
    for u, v, data in graph.edges(data=True):
        data["weight"] = u

    properties = graph_properties(graph)
    assert properties["num_nodes"] == n
    assert properties["num_edges"] == n - 1
    assert properties["avg_degree"] == 2 * (n - 1) / n
    assert properties["density"] == 2 * (n - 1) / (n * (n - 1))
    assert properties["planar"] == True
    assert properties["max_edgeweight"] == n - 2
    assert properties["min_edgeweight"] == 0
    assert properties["num_of_zero_edgeweights"] == 1
    assert properties["num_of_connected_components"] == 1
    assert properties["max_degree"] == 2
    assert -1.0 <= properties["assortativity_coeff"] <= -0.010204081632620635
    assert properties["number_of_triangles"] == 0
    assert properties["max_k_core"] == 1
    assert properties["average_clustering_coeff"] == 0
