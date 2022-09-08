import pytest

import random

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


def test_pm1s_no_zeros():
    g = pm1s_graph(100, 0, False)
    g_info = graph_properties(g)

    assert g_info["density"] <= 0.1
    assert g_info["num_nodes"] == 100
    assert g_info["num_of_zero_edgeweights"] == 0


def test_pm1s_save():
    i = 140
    g = pm1s_graph(i, 0, False)
    nx.write_weighted_edgelist(g, f"pm1s_{i}.el")


def test_pm1d():
    g = pm1d_graph(200, 0)
    g_info = graph_properties(g)

    assert g_info["density"] == 0.99
    assert g_info["num_nodes"] == 200


def test_pm1d_no_zeros():
    g = pm1d_graph(200, 0, False)
    g_info = graph_properties(g)

    assert g_info["density"] <= 0.99
    assert g_info["num_nodes"] == 200
    assert g_info["num_of_zero_edgeweights"] == 0


def test_pwd():
    g = pwd_graph(100, 0.3, 0)
    g_info = graph_properties(g)

    assert g_info["density"] == 0.3
    assert g_info["num_nodes"] == 100
    assert g_info["min_edgeweight"] >= 0


def test_pwd_no_zeros():
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


@pytest.mark.parametrize(
    "n", [5, 10, 15]
)
def test_t2g(n):
    g = t2g_graph(n)
    g_info = graph_properties(g, "weight")

    assert g_info["num_nodes"] == n ** 2
    assert g_info["max_degree"] == 4
    assert g_info["avg_degree"] == 4
    assert g_info["max_edgeweight"] != g_info["min_edgeweight"]


@pytest.mark.parametrize(
    "n", [5, 10, 15]
)
def test_t2g_ones(n):
    g = t2g_one(n)
    g_info = graph_properties(g)

    assert g_info["num_nodes"] == n ** 2
    assert g_info["max_degree"] == 4
    assert g_info["avg_degree"] == 4

    num_ones = 0
    num_minus_ones = 0
    for u, v, d in g.edges(data=True):
        w = d["weight"]
        if w == -1:
            num_minus_ones += 1
        elif w == 1:
            num_ones += 1
        else:
            assert False
    assert (num_ones == num_minus_ones) or (num_ones + 1 == num_minus_ones) or (num_ones == num_minus_ones + 1)
