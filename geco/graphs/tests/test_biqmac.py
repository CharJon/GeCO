from geco.graphs.biqmac import *
from geco.graphs.utilities import edgeweight_properties, graph_properties

import pytest


def test_generate_weighted_random_graph():
    g = generate_weighted_random_graph(100, 0.5, zero_to_ten, 0, True)
    g_info = graph_properties(g)

    assert g_info["density"] == 0.5
    assert g_info["num_nodes"] == 100
    assert g_info["num_of_zero_edgeweights"] == 241
    assert g_info["number_of_selfloops"] == 0

    # check that setting seed works
    g = generate_weighted_random_graph(100, 0.5, zero_to_ten, 0, True)
    g_info = graph_properties(g)

    assert g_info["density"] == 0.5
    assert g_info["num_nodes"] == 100
    assert g_info["num_of_zero_edgeweights"] == 241
    assert g_info["number_of_selfloops"] == 0

    # test for discarding zero wedges
    g = generate_weighted_random_graph(100, 0.5, zero_to_ten, 0, False)
    g_info = graph_properties(g)

    assert g_info["density"] < 0.5
    assert g_info["num_edges"] == 2234
    assert g_info["num_nodes"] == 100
    assert g_info["num_of_zero_edgeweights"] == 0
    assert g_info["number_of_selfloops"] == 0


def test_g05():
    g = g05_graph(100)
    g_info = graph_properties(g, weight_label=None)

    assert g_info["num_nodes"] == 100
    assert g_info["number_of_selfloops"] == 0


def test_pm1s():
    g = pm1s_graph(100)
    g_info = graph_properties(g)

    assert g_info["density"] == 0.1
    assert g_info["num_nodes"] == 100

    g = pm1s_graph(100, 0, False)
    g_info = graph_properties(g)

    assert g_info["density"] < 0.1
    assert g_info["num_nodes"] == 100
    assert g_info["num_of_zero_edgeweights"] == 0


def test_pm1d():
    g = pm1d_graph(200, 0)
    g_info = graph_properties(g)

    assert g_info["density"] == 0.99
    assert g_info["num_nodes"] == 2000

    g = pm1d_graph(200, 0, False)
    g_info = graph_properties(g)

    assert g_info["density"] < 0.99
    assert g_info["num_nodes"] == 200
    assert g_info["num_of_zero_edgeweights"] == 0


def test_pwd():
    g = pwd_graph(100, 0.3, 0)
    g_info = graph_properties(g)

    assert g_info["density"] == 0.3
    assert g_info["num_nodes"] == 100
    assert g_info["min_edgeweight"] >= 0

    g = pwd_graph(100, 0.3, 0, False)
    g_info = graph_properties(g)

    assert g_info["density"] < 0.3
    assert g_info["num_nodes"] == 100
    assert g_info["num_of_zero_edgeweights"] == 0


def test_wd():
    g = wd_graph(100, 0.6, 0)
    g_info = graph_properties(g)

    assert g_info["density"] == 0.6
    assert g_info["num_nodes"] == 100

    g = wd_graph(100, 0.6, 0, False)
    g_info = graph_properties(g)

    assert g_info["density"] < 0.6
    assert g_info["num_nodes"] == 100
    assert g_info["num_of_zero_edgeweights"] == 0


def test_t2g():
    g = t2g_graph(100)
    g_info = graph_properties(g)

    assert g_info["num_nodes"] == 10000
    assert g_info["max_degree"] == 4
    assert g_info["avg_degree"] == 4
