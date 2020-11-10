import itertools
import random

import networkx as nx
import pyscipopt as scip

import geco.mips.utilities.naming as naming


def tang(n, m, seed=0):
    """Generates a max-cut instance as described in A.2 in
        Tang, Y., Agrawal, S., & Faenza, Y. (2019). Reinforcement learning for integer
        programming: Learning to cut. arXiv preprint arXiv:1906.04859.
        Args:
            n (int): number of nodes
            m (int): number of edges
            seed (int): seed for randomization
    """
    random.seed(seed)
    graph = nx.generators.gnm_random_graph(n, m)
    for _, _, data in graph.edges(data=True):
        data['weight'] = random.randint(0, 10)
    _, model = naive(graph)
    return model


def empty_edge(graph: nx):
    model = scip.Model("Odd-Cycle MaxCut")

    edge_variables = {}
    for u, v, d in graph.edges(data=True):
        edge_name = naming.undirected_edge_name(u, v)
        weight = d["weight"]
        edge_variables[edge_name] = model.addVar(lb=0, ub=1, obj=weight, name=edge_name, vtype='B')

    model.setMaximize()

    return edge_variables, model


def naive(graph: nx):
    model = scip.Model("Naive MaxCut")

    node_variables = {}
    for v in graph.nodes():
        node_variables[v] = model.addVar(lb=0, ub=1, obj=0, name=str(v), vtype="B")

    edge_variables = {}
    for u, v, d in graph.edges(data=True):
        edge_name = naming.undirected_edge_name(u, v)
        weight = d["weight"]
        edge_variables[edge_name] = model.addVar(lb=0, ub=1, obj=weight, name=edge_name, vtype="B")

    model.setMaximize()

    for u, v, d in graph.edges(data=True):
        edge_name = naming.undirected_edge_name(u, v)
        model.addCons(node_variables[u] + node_variables[v] + edge_variables[edge_name] <= 2)
        model.addCons(-node_variables[u] - node_variables[v] + edge_variables[edge_name] <= 0)
        model.addCons(node_variables[u] - node_variables[v] - edge_variables[edge_name] <= 0)
        model.addCons(-node_variables[u] + node_variables[v] - edge_variables[edge_name] <= 0)

    return (node_variables, edge_variables), model


def triangle(graph: nx):
    model = scip.Model("Triangle MaxCut")

    edge_variables = {}

    for u, v in itertools.combinations(graph.nodes(), 2):
        edge_name = naming.undirected_edge_name(u, v)
        if graph.has_edge(u, v):
            weight = graph.get_edge_data(u, v)['weight']
        else:
            weight = 0
        edge_variables[edge_name] = model.addVar(lb=0, ub=1, obj=weight, name=edge_name, vtype="B")

    model.setMaximize()

    for i, j, k in itertools.combinations(graph.nodes(), 3):
        Xij = _get_edge_variable(i, j, edge_variables)
        Xik = _get_edge_variable(i, k, edge_variables)
        Xkj = _get_edge_variable(k, j, edge_variables)
        model.addCons(Xij <= Xik + Xkj)
        model.addCons(Xij + Xik + Xkj <= 2)

    return edge_variables, model


def _get_edge_variable(u, v, edge_variables):
    edge_name = naming.undirected_edge_name(u, v)
    alternative_edge_name = naming.undirected_edge_name(v, u)
    if edge_name in edge_variables:
        return edge_variables[edge_name]
    else:
        return edge_variables[alternative_edge_name]
