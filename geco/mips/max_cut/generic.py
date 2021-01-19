import itertools
import pyscipopt as scip

import geco.mips.utilities.naming as naming


def naive(graph):
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


def triangle(graph):
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
