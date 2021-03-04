import pyscipopt as scip
import itertools
import networkx as nx


def assignment(
    graph, color_upperbound, name="Assignment Graph Coloring", with_variables=False
):
    """
    Generates a graph coloring ILP formulation (ASS-S) as described in [1].

    Parameters
    ----------
    graph: networkx graph
        Input graph
    color_upperbound: int
        Maximum number of colors to use
    name: str
        Name of the model
    with_variables: bool
        return variables with the generated model (used to extend model)

    Returns
    -------
       model: scip.Model
        pyscipopt model of the generated instance

    References
    ----------
    .. [1] A.Jabrayilov, P.Mutzel "New Integer Linear Programming Models for the Vertex Coloring Problem"
    """
    model = scip.Model(name)

    graph = nx.convert_node_labels_to_integers(graph, first_label=0)
    colors = range(color_upperbound)

    # add variables and their cost
    x = {
        (vertex, color): model.addVar(
            lb=0, ub=1, obj=0, name=f"x_{vertex}_{color}", vtype="B"
        )
        for vertex, color in itertools.product(graph.nodes, colors)
    }

    w = {
        color: model.addVar(lb=0, ub=1, obj=1, name=f"w_{color}", vtype="B")
        for color in colors
    }

    # add constraint (2)
    for v in graph.nodes:
        model.addCons(scip.quicksum(x[v, color] for color in colors) == 1)

    # add constraint (3)
    for u, v in graph.edges:
        for color in colors:
            model.addCons(x[u, color] + x[v, color] <= w[color])

    model.setMinimize()
    if with_variables:
        return model, w, x
    else:
        return model


def assignment_asymmetric(
    graph, color_upperbound, name="Assignment Extended Graph Coloring"
):
    """
    Generates a graph coloring ILP formulation (ASS) as described in [1] which
    uses symmetry breaking rules from [2].

    Parameters
    ----------
    graph: networkx graph
        Input graph
    color_upperbound: int
        Maximum number of colors to use
    name: str
        Name of the model

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] A.Jabrayilov, P.Mutzel "New Integer Linear Programming Models for the Vertex Coloring Problem"
    .. [2] I.Mendez, P.Zabala "A Branch-and-Cut Algorithm for Graph Coloring"
    """
    model, w, x = assignment(graph, color_upperbound, name, with_variables=True)

    graph = nx.convert_node_labels_to_integers(graph, first_label=0)
    colors = list(range(color_upperbound))

    # add constraint (5)
    for color in colors:
        model.addCons(w[color] <= scip.quicksum(x[v, color] for v in graph.nodes))

    # add constraint (6)
    for color in colors[1:]:
        model.addCons(w[color] <= w[color - 1])
    return model


def representatives(graph, name="Representatives Graph Coloring"):
    """
    Generates a graph coloring ILP formulation (REP) as described in [1].

    Parameters
    ----------
    graph: networkx graph
        Input graph
    name: str
        Name of the model

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] A.Jabrayilov, P.Mutzel "New Integer Linear Programming Models for the Vertex Coloring Problem"
    """
    model = scip.Model(name)

    graph = nx.convert_node_labels_to_integers(graph, first_label=0)

    # add variables and their cost
    x = {}
    for (u, v) in itertools.product(graph.nodes, graph.nodes):
        if not graph.has_edge(u, v) or u == v:
            obj = 1 if u == v else 0
            x[u, v] = model.addVar(lb=0, ub=1, obj=obj, name=f"x_{u}_{v}", vtype="B")

    # add constraint (8)
    for v in graph.nodes:
        non_adjacent_vertices = (graph.nodes - graph.neighbors(v)).union({v})
        model.addCons(scip.quicksum(x[u, v] for u in non_adjacent_vertices) >= 1)

    # add constraint (9)
    for u in graph.nodes:
        non_adjacent_vertices = graph.nodes - graph.neighbors(u) - {u}
        for v, w in graph.edges:
            if v in non_adjacent_vertices and w in non_adjacent_vertices:
                model.addCons(x[u, v] + x[u, w] <= x[u, u])

    model.setMinimize()
    return model


def set_covering(graph, subsets, name="Set Covering Graph Coloring"):
    """
    Generates a graph coloring ILP formulation (COV) as described in [1].

    Parameters
    ----------
    graph: networkx graph
        Input graph
    subsets: Iterable of sets
        Independent Sets of nodes
    name: str
        Name of the model

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] A.Jabrayilov, P.Mutzel "New Integer Linear Programming Models for the Vertex Coloring Problem"
    """
    model = scip.Model(name)

    graph = nx.convert_node_labels_to_integers(graph, first_label=0)

    x = {
        tuple(s): model.addVar(lb=0, ub=1, obj=1, name=f"x_{s}", vtype="B")
        for s in subsets
    }

    for v in graph.nodes:
        model.addCons(scip.quicksum(x[tuple(s)] for s in subsets if v in s) >= 1)

    model.setMinimize()

    return model


def _partial_ordering_base_model(graph, colors, model):
    q = 0

    # add variables and their cost
    y = {
        (color, vertex): model.addVar(
            lb=0,
            ub=1,
            obj=1 if vertex == q else 0,
            name=f"y_{color}_{vertex}",
            vtype="B",
        )
        for vertex, color in itertools.product(graph.nodes, colors)
    }

    z = {
        (vertex, color): model.addVar(
            lb=0, ub=1, obj=0, name=f"z_{vertex}_{color}", vtype="B"
        )
        for vertex, color in itertools.product(graph.nodes, colors)
    }

    # add constraint (16) and (17)
    for v in graph.nodes:
        model.addCons(z[v, 1] == 0)
        model.addCons(y[colors[-1], v] == 0)

    # add constraint (18), (19) and (21)
    for v, c in itertools.product(graph.nodes, colors[:-1]):
        model.addCons(y[c, v] - y[c + 1, v] >= 0)
        model.addCons(y[c, v] + z[v, c + 1] == 1)
        model.addCons(y[c, q] - y[c, v] >= 0)

    model.setMinimize()

    return model, y, z


def partial_ordering(graph, color_upperbound, name="Partial Ordering Graph Coloring"):
    """
    Generates a graph coloring ILP formulation (POP) as described in [1].

    Parameters
    ----------
    graph: networkx graph
        Input graph
    color_upperbound: int
        Maximum number of colors to use
    name: str
        Name of the model

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] A.Jabrayilov, P.Mutzel "New Integer Linear Programming Models for the Vertex Coloring Problem"
    """
    model = scip.Model(name)

    graph = nx.convert_node_labels_to_integers(graph, first_label=0)
    colors = list(range(color_upperbound))

    model, y, z = _partial_ordering_base_model(graph, colors, model)

    # add constraint (20)
    for (u, v), c in itertools.product(graph.edges, colors[:-1]):
        model.addCons(y[c, u] + z[u, c] + y[c, v] + z[v, c] >= 1)

    return model


def hybrid_partial_ordering(
    graph, color_upperbound, name="Hybrid Partial Ordering Graph Coloring"
):
    """
    Generates a graph coloring ILP formulation (POP2) as described in [1].

    Parameters
    ----------
    graph: networkx graph
        Input graph
    color_upperbound: int
        Maximum number of colors to use
    name: str
        Name of the model

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] A.Jabrayilov, P.Mutzel "New Integer Linear Programming Models for the Vertex Coloring Problem"
    """
    model = scip.Model(name)

    graph = nx.convert_node_labels_to_integers(graph, first_label=0)
    colors = list(range(color_upperbound))

    # add variables and their cost
    x = {
        (vertex, color): model.addVar(
            lb=0, ub=1, obj=0, name=f"x_{vertex}_{color}", vtype="B"
        )
        for vertex, color in itertools.product(graph.nodes, colors)
    }

    model, y, z = _partial_ordering_base_model(graph, colors, model)

    # add constraint (14)
    for v, c in itertools.product(graph.nodes, colors):
        model.addCons(x[v, c] == 1 - (y[c, v] + z[v, c]))

    # add constraint (23)
    for (u, v), c in itertools.product(graph.edges, colors):
        model.addCons(x[u, c] + x[v, c] <= 1)

    return model
