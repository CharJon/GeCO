import pytest

from geco.mips.independent_set import *


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
