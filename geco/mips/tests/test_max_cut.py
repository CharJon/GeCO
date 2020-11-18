import pytest

from geco.mips.max_cut import *


def test_tang():
    n, m = 100, 50
    model = tang_instance(n, m)
    assert model.getNVars() == m + n
    assert model.getNConss() == 2 * m
    assert model.getObjectiveSense() == "maximize"


def test_empty_edge():
    graph = nx.generators.complete_graph(3)
    for _, _, data in graph.edges(data=True):
        data["weight"] = 1
    _, model = empty_edge(graph)
    assert model.getNVars() == len(graph.edges)
    assert model.getNConss() == 0


def test_triangle():
    graph = nx.generators.complete_graph(3)
    for _, _, data in graph.edges(data=True):
        data["weight"] = 1
    _, model = triangle(graph)
    m = len(graph.edges)
    assert model.getNVars() == m
    assert model.getNConss() == 2
    model.hideOutput()
    model.optimize()
    assert model.getStatus() == "optimal"
    assert model.getObjVal() == 2


def test_naive_negative():
    graph = nx.generators.complete_graph(3)
    for _, _, data in graph.edges(data=True):
        data["weight"] = -1
    _, model = naive(graph)
    n, m = len(graph), len(graph.edges)
    assert model.getNVars() == n + m
    assert model.getNConss() == 4 * m
    model.hideOutput()
    model.optimize()
    assert model.getStatus() == "optimal"
    assert model.getObjVal() == 0


def test_naive_non_negative():
    graph = nx.generators.complete_graph(3)
    for _, _, data in graph.edges(data=True):
        data["weight"] = 1
    _, model = naive(graph)
    n, m = len(graph), len(graph.edges)
    assert model.getNVars() == n + m
    assert model.getNConss() == 2 * m
    model.hideOutput()
    model.optimize()
    assert model.getStatus() == "optimal"
    assert model.getObjVal() == 2


@pytest.mark.parametrize(
    "n,seed1,seed2",
    itertools.product([3, 10, 100], [0, 1, 1337, 53115], [0, 1, 1337, 53115]),
)
def test_seeding(n, seed1, seed2):
    graph = nx.generators.complete_graph(n)
    weights1 = tang_weights(graph, seed=seed1)
    weights2 = tang_weights(graph, seed=seed2)
    same_seeds_produce_same_params = seed1 == seed2 and weights1 == weights2
    different_seeds_produce_different_params = seed1 != seed2 and weights1 != weights2
    assert same_seeds_produce_same_params or different_seeds_produce_different_params
