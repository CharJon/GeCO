import networkx as nx
import random


def generate_weighted_random_graph(n, d, weight_func, seed=0, keep_zero_edges=True):
    """
    Generate a random weighted graph with target density using specified weight function.

    Parameters
    ----------
    n: int
        Size of the graph
    d: float
        target density
    weight_func: function() -> number
      Function which returns an edge weight
    seed: int
        Seed for random generation
    keep_zero_edges: bool
        If True zero edges are kept in the graph, if False zero weight edges are discarded

    Returns
    -------
        graph: nx.Graph
            generated random graph

    """

    m = int(d * (n * (n - 1)) / 2)

    graph = nx.gnm_random_graph(n, m, seed)
    random.seed(seed)

    for e in graph.edges:
        w = weight_func(seed)

        if w != 0 or keep_zero_edges:
            graph.add_edge(e[0], e[1], weight=w)
        else:
            graph.remove_edge(e[0], e[1])

    return graph


def negative_one_to_one():
    return random.randint(-1, 1)


def negative_ten_to_ten():
    return random.randint(-10, 10)


def zero_to_ten():
    return random.randint(0, 10)


def g05_n(n, seed=0):
    """
    Generates a g05 graph as described in [1], using networkx

    Parameters
    ----------
    n: int
        Size of generated graph
    seed:
        Seed for random generation

    Returns
    -------
    graph: nx.Graph
        The generated g05 graph with n nodes.

    References
    ----------
    ..[1] https://biqmac.aau.at/biqmaclib.html
    """

    graph = nx.gnp_random_graph(n, 0.5, seed)

    return graph


def pm1s_graph(n, seed, keep_zero_edges=True):
    """
    Generates a pm1s graph as described in [1], using networkx

    Parameters
    ----------
    n: int
        Size of generated graph
    seed:
        Seed for random generation
    keep_zero_edges: bool
        If True zero edges are kept in the graph, if False zero weight edges are discarded

    Returns
    -------
    graph: nx.Graph
        The generated g05 graph with n nodes.

    References
    ----------
    ..[1] https://biqmac.aau.at/biqmaclib.html
    """
    return generate_weighted_random_graph(n, 0.1, negative_one_to_one, seed, keep_zero_edges)


def pm1d_graph(n, seed, keep_zero_edges=True):
    """
    Generates a pm1d graph as described in [1], using networkx

    Parameters
    ----------
    n: int
        Size of generated graph
    seed:
        Seed for random generation
    keep_zero_edges: bool
        If True zero edges are kept in the graph, if False zero weight edges are discarded

    Returns
    -------
    graph: nx.Graph
        The generated g05 graph with n nodes.

    References
    ----------
    ..[1] https://biqmac.aau.at/biqmaclib.html
    """
    return generate_weighted_random_graph(n, 0.99, negative_one_to_one, seed, keep_zero_edges)


def wd_graph(n, d, seed, keep_zero_edges=True):
    """
    Generates a wd_n graph as described in [1], using networkx

    Parameters
    ----------
    n: int
        Size of generated graph
    d: float
        Density of the graph
    seed:
        Seed for random generation
    keep_zero_edges: bool
        If True zero edges are kept in the graph, if False zero weight edges are discarded

    Returns
    -------
    graph: nx.Graph
        The generated g05 graph with n nodes.

    References
    ----------
    ..[1] https://biqmac.aau.at/biqmaclib.html
    """
    return generate_weighted_random_graph(n, d, negative_ten_to_ten, seed, keep_zero_edges)


def pwd_graph(n, d, seed, keep_zero_edges=True):
    """
    Generates a pwd_n graph as described in [1], using networkx

    Parameters
    ----------
    n: int
        Size of generated graph
    d: float
        Density of the graph
    seed:
        Seed for random generation
    keep_zero_edges: bool
        If True zero edges are kept in the graph, if False zero weight edges are discarded

    Returns
    -------
    graph: nx.Graph
        The generated g05 graph with n nodes.

    References
    ----------
    ..[1] https://biqmac.aau.at/biqmaclib.html
    """
    return generate_weighted_random_graph(n, d, zero_to_ten, seed, keep_zero_edges)
