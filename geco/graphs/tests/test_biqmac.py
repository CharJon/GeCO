from geco.graphs.biqmac import *
from geco.graphs.utilities import graph_properties


def test_generate_weighted_random_graph():
    seed = 0
    r1 = random.Random(seed)
    r2 = random.Random(seed)
    g_1 = generate_weighted_random_graph(100, 0.5, lambda: zero_to_ten(r1), 0, True)
    g_2 = generate_weighted_random_graph(100, 0.5, lambda: zero_to_ten(r2), 0, True)
    for g in (g_1, g_2):
        g_info = graph_properties(g)

        assert g_info["density"] == 0.5
        assert g_info["num_nodes"] == 100
        assert g_info["number_of_selfloops"] == 0
    assert g_1.number_of_edges() == g_2.number_of_edges()


def test_generate_weighted_random_graph_no_zeros():
    seed = 0
    r = random.Random(seed)
    g = generate_weighted_random_graph(100, 0.5, lambda: zero_to_ten(r), 0, False)
    g_info = graph_properties(g)

    assert g_info["density"] <= 0.5
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
    assert g_info["num_nodes"] == 200

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
