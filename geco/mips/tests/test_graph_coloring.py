import networkx as nx
import pytest

from geco.mips.graph_coloring.generic import *


def _test_cycle_instance_output(model):
    model.hideOutput()
    model.optimize()
    assert model.getStatus() == "optimal"
    assert model.getObjVal() == 3


def test_assignment():
    graph = nx.cycle_graph(5)
    H = 5
    model = assignment(graph, H)
    n = len(graph.nodes)
    m = len(graph.edges)

    # test variables and constraints
    assert model.getNVars() == n * H + H
    assert model.getNConss() == n + m * H

    _test_cycle_instance_output(model)


def test_assignment_asymmetric():
    graph = nx.cycle_graph(5)
    H = 5
    model = assignment_asymmetric(graph, H)
    n = len(graph.nodes)
    m = len(graph.edges)

    # test variables and constraints
    assert model.getNVars() == n * H + H
    assert model.getNConss() == n + m * H + H + (H - 1)

    _test_cycle_instance_output(model)


def test_representatives():
    graph = nx.cycle_graph(5)
    model = representatives(graph)
    n = len(graph.nodes)
    m = len(graph.edges)

    # test variables and constraints
    assert n <= model.getNVars() <= n ** 2
    assert n <= model.getNConss() <= n + n * m

    _test_cycle_instance_output(model)


def test_set_covering():
    graph = nx.cycle_graph(5)
    subsets = [{0, 1}, {2, 3}, {4}]
    model = set_covering(graph, subsets)
    n = len(graph.nodes)

    # test variables and constraints
    assert 1 <= model.getNVars() <= 2 ** n
    assert n <= model.getNConss() <= n * (2 ** n)

    _test_cycle_instance_output(model)


def test_partial_ordering():
    graph = nx.cycle_graph(5)
    H = 5
    model = partial_ordering(graph, H)
    n = len(graph.nodes)

    # test variables and constraints
    assert model.getNVars() == 2 * n * H
    assert n <= model.getNConss() == 2 * n + 4 * n * (H - 1)

    _test_cycle_instance_output(model)


def test_hybrid_partial_ordering():
    graph = nx.cycle_graph(5)
    H = 5
    model = hybrid_partial_ordering(graph, H)
    n = len(graph.nodes)

    # test variables and constraints
    assert model.getNVars() == 3 * n * H
    assert n + n * H <= model.getNConss() == 2 * n + 3 * n * (H - 1) + n * H + n * H

    _test_cycle_instance_output(model)


def test_node_labeling():
    g = nx.karate_club_graph()
    g = nx.convert_node_labels_to_integers(g, first_label=1)
    H = 10
    models = [
        representatives(g),
        assignment(g, H),
        assignment_asymmetric(g, H),
        partial_ordering(g, H),
        hybrid_partial_ordering(g, H),
    ]
    for m in models:
        m.hideOutput()
        m.optimize()
        assert m.getStatus() == "optimal" and m.getObjVal() == 5
