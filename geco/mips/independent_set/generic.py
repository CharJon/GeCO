import networkx as nx
import pyscipopt as scip


def independent_set(graph, name="Independent Set"):
    """
    Generates an independent set instance according to [1].

    Parameters
    ----------
    graph: nx.Graph
        Networkx undirected graph
    name: str
        Name of the generated model

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] https://www.princeton.edu/~aaa/Public/Teaching/ORF523/S16/ORF523_S16_Lec11_gh.pdf
    """
    graph = nx.relabel.convert_node_labels_to_integers(graph)
    model = scip.Model(name)

    vars = {
        str(node): model.addVar(lb=0, ub=1, obj=1, name=str(node), vtype="B")
        for node in graph.nodes
    }

    for u, v in graph.edges:
        model.addCons(vars[str(u)] + vars[str(v)] <= 1)

    model.setMaximize()

    return model


def _get_cliques(graph):
    """
    Partition the graph into cliques using a greedy algorithm, this code is
    based on the code from [1].

    Parameters
    ----------
    graph: nx.Graph
        Networkx undirected graph

    Returns
    -------
    cliques: list[set]
        The resulting clique partition

    References
    ----------
    .. [1] https://github.com/ds4dm/learn2branch/blob/master/01_generate_instances.py
    """
    cliques = []

    # sort nodes in descending order of degree
    leftover_nodes = sorted(list(graph.nodes), key=lambda node: -graph.degree[node])

    while leftover_nodes:
        clique_center, leftover_nodes = leftover_nodes[0], leftover_nodes[1:]
        clique = {clique_center}
        neighbors = set(graph.neighbors(clique_center)).intersection(leftover_nodes)
        densest_neighbors = sorted(neighbors, key=lambda node: -graph.degree[node])
        for neighbor in densest_neighbors:
            if all(
                [neighbor in graph.neighbors(clique_node) for clique_node in clique]
            ):
                clique.add(neighbor)
        cliques.append(clique)
        leftover_nodes = [node for node in leftover_nodes if node not in clique]

    return cliques


def clique_independent_set(graph, name="Clique Independent Set"):
    """
    Generates an independent set instance according to [1, 4.6.4].

    Parameters
    ----------
    graph: nx.Graph
        Networkx undirected graph
    name: str
        Name of the generated model

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] David Bergman, Andre A. Cire, Willem-Jan Van Hoeve, and John Hooker. Decision diagrams
    for optimization. Springer, 2016.
    """
    graph = nx.relabel.convert_node_labels_to_integers(graph)
    model = scip.Model(name)

    cliques = _get_cliques(graph)

    vars = {
        str(node): model.addVar(lb=0, ub=1, obj=1, name=str(node), vtype="B")
        for node in graph.nodes
    }

    for clique in cliques:
        model.addCons(scip.quicksum(vars[str(node)] for node in clique) <= 1)

    model.setMaximize()

    return model
