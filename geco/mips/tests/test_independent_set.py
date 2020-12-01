import itertools

import pytest

from geco.mips.independent_set.barabasi_albert import *
from geco.mips.independent_set.gasse import *
from geco.mips.independent_set.generic import *


@pytest.mark.parametrize(
    "graph",
    [
        nx.generators.complete_graph(3),
        nx.generators.complete_graph(10),
        nx.generators.complete_graph(50),
    ],
)
def test_independent_set(graph):
    model = independent_set(graph)
    n = len(graph.nodes)
    assert model.getNVars() == n
    assert model.getNConss() == n * (n - 1) / 2
    assert model.getObjectiveSense() == "maximize"


def test_simple_instance():
    graph = nx.generators.complete_graph(3)
    model = independent_set(graph)
    model.hideOutput()
    model.optimize()
    assert model.getStatus() == "optimal"
    assert model.getObjVal() == 1


@pytest.mark.parametrize(
    "graph",
    [
        nx.generators.complete_graph(3),
        nx.generators.complete_graph(10),
        nx.generators.complete_graph(50),
    ],
)
def test_clique_independent_set(graph):
    model = clique_independent_set(graph)
    assert model.getNVars() == len(graph.nodes)
    assert model.getNConss() <= len(graph.edges)
    assert model.getObjectiveSense() == "maximize"


def test_clique_simple_instance():
    graph = nx.generators.complete_graph(3)
    model = clique_independent_set(graph)
    model.hideOutput()
    model.optimize()
    assert model.getStatus() == "optimal"
    assert model.getObjVal() == 1


@pytest.mark.parametrize(
    "n,p,seed", itertools.product([10, 50], [0.5, 0.9], [0, 1, 1337, 53115])
)
def test_gasse(n, p, seed):
    model = gasse_instance(n, p, seed)
    assert model.getNVars() == n
    assert model.getNConss() <= n * (n - 1) / 2
    assert model.getObjectiveSense() == "maximize"


@pytest.mark.parametrize(
    "n,p,seed1,seed2",
    itertools.product([10, 50], [0.5, 0.9], [0, 1, 1337, 53115], [0, 1, 1337, 53115]),
)
def test_gasse_seeding(n, p, seed1, seed2):
    graph1 = gasse_params(n, p, seed=seed1)
    graph2 = gasse_params(n, p, seed=seed2)
    same_edges = set(graph1.edges) == set(graph2.edges)
    same_seeds_produce_same_params = seed1 == seed2 and same_edges
    different_seeds_produce_different_params = seed1 != seed2 and not same_edges
    assert same_seeds_produce_same_params or different_seeds_produce_different_params


@pytest.mark.parametrize(
    "n,m,seed", itertools.product([10, 50], [5, 9], [0, 1, 1337, 53115])
)
def test_barabasi_albert(n, m, seed):
    model = barabasi_albert_instance(n, m, seed)
    assert model.getNVars() == n
    assert model.getNConss() <= n * (n - 1) / 2
    assert model.getObjectiveSense() == "maximize"


@pytest.mark.parametrize(
    "n,m,seed1,seed2",
    itertools.product([100, 500], [5, 10], [0, 1, 1337, 53115], [0, 1, 1337, 53115]),
)
def test_barabasi_albert_seeding(n, m, seed1, seed2):
    graph1 = barabasi_albert_params(n, m, seed=seed1)
    graph2 = barabasi_albert_params(n, m, seed=seed2)
    same_edges = set(graph1.edges) == set(graph2.edges)
    same_degrees = dict(graph1.degree) == dict(graph2.degree)
    same = same_edges and same_degrees
    same_seeds_produce_same_params = seed1 == seed2 and same
    different_seeds_produce_different_params = seed1 != seed2 and not same
    assert same_seeds_produce_same_params or different_seeds_produce_different_params
