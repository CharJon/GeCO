import networkx as nx
import pyscipopt as scip


def independent_set(graph: nx.Graph, name: str = "Independent Set") -> scip.Model:
    """
    Generates an independent set instance according to [1].

    Parameters
    ----------
    graph: nx.Graph
        Networkx undirected graph
    name: str
        name of the generated model

    Returns
    -------
    model: scip.Model
        pyscipopt model of the generated instance

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


def _get_cliques(graph: nx.Graph) -> list:
    """
    Partition the graph into cliques using a greedy algorithm, this code is
    based on the code from [1].

    Returns
    -------
    cliques: list of sets
        The resulting clique partition.

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


def clique_independent_set(graph: nx.Graph, name: str = "Clique Independent Set"):
    """
    Generates an independent set instance according to [1, 4.6.4].

    Parameters
    ----------
    graph: nx.Graph
        Networkx undirected graph
    name: str
        name of the generated model

    Returns
    -------
    model: scip.Model
        pyscipopt model of the generated instance

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


def gasse_params(n: int, p: float, seed=0) -> nx.Graph:
    return nx.generators.erdos_renyi_graph(n, p, seed)


def gasse_instance(n: int, p: float, seed=0) -> scip.Model:
    """
    Generates a maximum independent set instance as described in [1].

    Parameters
    ----------
    n: int
        number of nodes.
    p: float
        edge probability
    seed: int, random state or None
        randomization seed

    Returns
    -------
    model: scip.Model
        pyscipopt model of the instance.

    References
    ----------
    .. [1] "Exact Combinatorial Optimization with Graph Convolutional Neural Networks" (2019)
      Maxime Gasse, Didier Chételat, Nicola Ferroni, Laurent Charlin and Andrea Lodi
      Advances in Neural Information Processing Systems 32 (2019)
    """
    return clique_independent_set(
        gasse_params(n, p, seed), name="Gasse Independent Set"
    )
