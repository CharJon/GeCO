import networkx as nx
import random

from networkx.utils import py_random_state


def generate_weighted_random_graph(n, d, weight_func, nx_seed=0, keep_zero_edges=True):
    """
    Generate a random weighted graph with 'exact' target density using specified weight function.

    Parameters
    ----------
    n: int
        Size of the graph
    d: float
        target density
    weight_func: function() -> number
      Function which returns an edge weight
    nx_seed: int
        Seed for random generation
    keep_zero_edges: bool
        If True zero edges are kept in the graph, if False zero weight edges are discarded

    Returns
    -------
        graph: nx.Graph
            generated random graph

    """

    m = int(d * (n * (n - 1)) / 2)

    if d <= 0.1:
        graph = nx.gnm_random_graph(n, m, nx_seed)
    else:
        graph = nx.dense_gnm_random_graph(n, m, nx_seed)

    for u, v in graph.edges:
        w = weight_func()

        if w != 0 or keep_zero_edges:
            graph.add_edge(u, v, weight=w)
        else:
            graph.remove_edge(u, v)

    return graph


@py_random_state("seed")
def one_or_minus_one(seed):
    return seed.choices([1, -1], k=1)[0]


@py_random_state("seed")
def negative_ten_to_ten(seed):
    return seed.randint(-10, 10)


@py_random_state("seed")
def zero_to_ten(seed):
    return seed.randint(0, 10)


@py_random_state("seed")
def random_gauss(seed, mu, sigma):
    return seed.gauss(mu, sigma)


@py_random_state("seed")
def g05_graph(n, seed=0):
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


@py_random_state("seed")
def pm1s_graph(n, seed=0, keep_zero_edges=True):
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
        The generated pm1s graph.

    References
    ----------
    ..[1] https://biqmac.aau.at/biqmaclib.html
    """
    return generate_weighted_random_graph(n, 0.1, lambda: one_or_minus_one(seed), seed, keep_zero_edges)


@py_random_state("seed")
def pm1d_graph(n, seed=0, keep_zero_edges=True):
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
        The generated pm1d graph.

    References
    ----------
    ..[1] https://biqmac.aau.at/biqmaclib.html
    """
    return generate_weighted_random_graph(n, 0.99, lambda: one_or_minus_one(seed), seed, keep_zero_edges)


@py_random_state("seed")
def wd_graph(n, d, seed=0, keep_zero_edges=True):
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
        The generated w graph.

    References
    ----------
    ..[1] https://biqmac.aau.at/biqmaclib.html
    """
    return generate_weighted_random_graph(n, d, lambda: negative_ten_to_ten(seed), seed, keep_zero_edges)


@py_random_state("seed")
def pwd_graph(n, d, seed=0, keep_zero_edges=True):
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
        The generated pw graph.

    References
    ----------
    ..[1] https://biqmac.aau.at/biqmaclib.html
    """
    return generate_weighted_random_graph(n, d, lambda: zero_to_ten(seed), seed, keep_zero_edges)


def node_name(i, j):
    return f"({i}, {j})"


@py_random_state("seed")
def equal_many_ones(n, seed):
    num_plus_ones = n
    num_minus_ones = n

    while num_minus_ones + num_plus_ones > 0:
        number = seed.choices([1, -1], weights=[num_plus_ones, num_minus_ones], k=1)
        yield number[0]
        if number[0] == 1:
            num_plus_ones -= 1
        else:
            num_minus_ones -= 1


@py_random_state("seed")
def t2g_base(n, weight_func, seed=0, keep_zero_edges=True):
    """
    Generates a 2d torus graph using the given weight func

    Parameters
    ----------
    n: int
        Size of the grid, number of nodes ill be n*n
    weight_func: function(seed) -> number
        Function for edge weights
    seed:
        Seed for random numbers

    Returns
    -------
    graph: nx.Graph
        The generated t2g graph.

    """
    g = nx.Graph()
    random.seed(seed)

    for i in range(n):
        for j in range(n):
            g.add_node(node_name(i, j))

    for i in range(n):
        for j in range(n):
            next_index = j + 1 if j + 1 < n else 0

            w = weight_func()
            if w != 0 or keep_zero_edges:
                g.add_edge(node_name(i, j), node_name(i, next_index), weight=w)

            w = weight_func()
            if w != 0 or keep_zero_edges:
                g.add_edge(node_name(j, i), node_name(next_index, i), weight=w)

    return g


@py_random_state("seed")
def t2g_graph(n, seed=0, keep_zero_edges=True):
    """
       Generates a 2d torus graph using with gaussian weight as described by [1].
       Weights are drawn from gaussian distribution with mu=0, sigma=1, scaled by 10^5 and rounded.

       Parameters
       ----------
       n: int
           Size of the grid, number of nodes ill be n*n
       weight_func: function(seed) -> number
           Function for edge weights
       seed:
           Seed for random numbers

       Returns
       -------
       graph: nx.Graph
           The generated t2g graph.

       References
       ----------
       ..[1] https://biqmac.aau.at/biqmaclib.html

       """

    return t2g_base(n, lambda: int(10 ** 5 * random_gauss(seed, 0, 1)), seed, keep_zero_edges)


@py_random_state("seed")
def t2g_one(n, seed=0, keep_zero_edges=True):
    """
    Generates a 2d torus graph as described by [1]
    All edges have weight -1 or 1 and there are equal many of each (+-1)

    Parameters
    ----------
    n: int
        Size of the grid, number of nodes ill be n*n
    seed:
        Seed for random numbers

    Returns
    -------
    graph: nx.Graph
        The generated t2g graph.

    References
    ----------
    ..[1] Bonato, T., Jünger, M., Reinelt, G., Rinaldi, G.:
    Lifting and separation procedures for the cut polytope.Math. Prog.146(1–2), 351–378 (2014)

    """

    weight_generator = equal_many_ones(n * n, seed)
    return t2g_base(n, lambda: next(weight_generator), seed, keep_zero_edges)
