import itertools

import networkx as nx
import pyscipopt as scip
from networkx.utils import py_random_state

import geco.mips.utilities.naming as naming


@py_random_state(2)
def tang_instance(n, m, seed=0):
    """Generates a max-cut instance as described in A.2 in
    Tang, Y., Agrawal, S., & Faenza, Y. (2019). Reinforcement learning for integer
    programming: Learning to cut. arXiv preprint arXiv:1906.04859.
    Args:
        n (int): number of nodes
        m (int): number of edges
        seed (int, random state or None): seed for randomization
    """

    graph = nx.generators.gnm_random_graph(n, m, seed=seed)
    weights = tang_weights(graph, seed=0)
    for (_, _, data), weight in zip(graph.edges(data=True), weights):
        data["weight"] = weight
    _, model = naive(graph)
    return model


@py_random_state(1)
def tang_weights(graph, seed=0):
    weights = []
    for _ in graph.edges:
        weights.append(seed.randint(0, 10))
    return weights


def empty_edge(graph: nx):
    model = scip.Model("Odd-Cycle MaxCut")

    edge_variables = {}
    for u, v, d in graph.edges(data=True):
        edge_name = naming.undirected_edge_name(u, v)
        weight = d["weight"]
        edge_variables[edge_name] = model.addVar(
            lb=0, ub=1, obj=weight, name=edge_name, vtype="B"
        )

    model.setMaximize()

    return edge_variables, model


def naive(graph: nx):
    model = scip.Model("Naive MaxCut")

    node_variables = {}
    for v in graph.nodes():
        node_variables[v] = model.addVar(lb=0, ub=1, obj=0, name=str(v), vtype="B")

    edge_variables = {}
    all_non_negative = True
    for u, v, d in graph.edges(data=True):
        edge_name = naming.undirected_edge_name(u, v)
        weight = d["weight"]
        edge_variables[edge_name] = model.addVar(
            lb=0, ub=1, obj=weight, name=edge_name, vtype="B"
        )
        if weight < 0:
            all_non_negative = False

    model.setMaximize()

    for u, v, d in graph.edges(data=True):
        edge_name = naming.undirected_edge_name(u, v)
        model.addCons(
            node_variables[u] + node_variables[v] + edge_variables[edge_name] <= 2
        )
        model.addCons(
            -node_variables[u] - node_variables[v] + edge_variables[edge_name] <= 0
        )
        if not all_non_negative:
            model.addCons(
                node_variables[u] - node_variables[v] - edge_variables[edge_name] <= 0
            )
            model.addCons(
                -node_variables[u] + node_variables[v] - edge_variables[edge_name] <= 0
            )

    return (node_variables, edge_variables), model


def triangle(graph: nx):
    model = scip.Model("Triangle MaxCut")

    edge_variables = {}

    for u, v in itertools.combinations(graph.nodes(), 2):
        edge_name = naming.undirected_edge_name(u, v)
        if graph.has_edge(u, v):
            weight = graph.get_edge_data(u, v)["weight"]
        else:
            weight = 0
        edge_variables[edge_name] = model.addVar(
            lb=0, ub=1, obj=weight, name=edge_name, vtype="B"
        )

    model.setMaximize()

    for i, j, k in itertools.combinations(graph.nodes(), 3):
        x_ij = _get_edge_variable(i, j, edge_variables)
        x_ik = _get_edge_variable(i, k, edge_variables)
        x_kj = _get_edge_variable(k, j, edge_variables)
        model.addCons(x_ij <= x_ik + x_kj)
        model.addCons(x_ij + x_ik + x_kj <= 2)

    return edge_variables, model


def _get_edge_variable(u, v, edge_variables):
    edge_name = naming.undirected_edge_name(u, v)
    return edge_variables[edge_name]
