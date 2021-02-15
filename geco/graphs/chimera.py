import numpy as np
import networkx as nx
from networkx.utils import py_random_state, np_random_state
from numpy.random import random
import dwave_networkx as dwave


@py_random_state(-1)
def draw_intra_weight(seed=0):
    return seed.random() - 0.5


@py_random_state(-1)
def draw_inter_weight(seed=0):
    return seed.random() * 2 - 1


def chimera_graph(n, m, t, inter=lambda: 0, intra=lambda: 0):
    """
    Generate DWave Chimera graph as described in [1].

    Parameters
    ----------
    n: int
        Number of cells per row
    m: int
        Number of cells per column
    t: int
        Number of nodes on each side of a bipartite cell subgraph
    inter: function (seed) -> number
        Function to call for weights of inter-cell edges
    intra: function (seed) -> number
        Function to call for weights of intra-cell edges

    Returns
    -------
    graph: nx.Graph
        The generated Chimera graph

    References
    ----------
    ..[1] https://docs.ocean.dwavesys.com/en/latest/concepts/topology.html
    """
    graph = nx.Graph()
    # add nodes
    for cur_n in range(n):
        for cur_m in range(m):
            for cur_t in range(t):
                for cur_s in range(2):
                    graph.add_node((cur_n, cur_m, cur_t, cur_s))

    # add intra-cell edges
    for cur_n in range(n):
        for cur_m in range(m):
            for left_t in range(t):
                for right_t in range(t):
                    graph.add_edge(
                        (cur_n, cur_m, left_t, 0),
                        (cur_n, cur_m, right_t, 1),
                        weight=inter(),
                    )

    # add horizontal inter-cell edges
    for cur_n in range(n):
        for cur_m in range(m - 1):
            for cur_t in range(t):
                graph.add_edge(
                    (cur_n, cur_m, cur_t, 1),
                    (cur_n, cur_m + 1, cur_t, 1),
                    weight=intra(),
                )

    # add vertical inter-cell edges
    for cur_n in range(n - 1):
        for cur_m in range(m):
            for cur_t in range(t):
                graph.add_edge(
                    (cur_n, cur_m, cur_t, 0),
                    (cur_n + 1, cur_m, cur_t, 0),
                    weight=intra(),
                )

    return graph


"""
Parameterised graph generators
"""


@np_random_state(-1)
def selby_c(m, seed=0):
    """
    Generate Selby Chimera graph as described in section 7.3 in [1].

    Parameters
    ----------
    m: int
        Number of cells per column
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    graph: nx.Graph
        The generated Chimera graph

    References
    ----------
    ..[1] Jünger, M., Lobe, E., Mutzel, P., Reinelt, G., Rendl, F., Rinaldi, G., & Stollenwerk, T. (2019).
    Performance of a quantum annealer for Ising ground state computations on chimera graphs.
    arXiv preprint arXiv:1904.11965.
    """

    def inter_w():
        return seed.randint(low=-10, high=10 + 1) / 10.0

    def intra_w():
        return seed.randint(low=-5, high=5 + 1) / 10.0

    graph = chimera_graph(m, m, 4, inter=inter_w, intra=intra_w)

    graph.graph["name"] = f"selby_c{m}"
    graph.graph["seed"] = seed

    return graph


def _initialize_weights_chimera(
    chimera_graph, size, draw_inter_weight, draw_intra_weight, draw_other_weight
):
    c_coor = dwave.chimera_coordinates(size)
    for _from, _to in chimera_graph.edges:
        _from_nice = c_coor.linear_to_chimera(_from)
        _to_nice = c_coor.linear_to_chimera(_to)
        if in_same_chimera_tile(_from_nice, _to_nice):
            # edge from one side to the other (internal edge)
            if not on_same_side(_from_nice, _to_nice):
                chimera_graph.add_edge(_from, _to, weight=draw_intra_weight())
            else:  # odd couplers
                chimera_graph.add_edge(_from, _to, weight=draw_other_weight())
        else:
            chimera_graph.add_edge(_from, _to, weight=draw_inter_weight())


def on_same_side(_from_nice, _to_nice):
    u = 2
    return _from_nice[u] == _to_nice[u]


def in_same_chimera_tile(_from_nice, _to_nice):
    y, x = 0, 1
    return _from_nice[y] == _to_nice[y] and _from_nice[x] == _to_nice[x]


@py_random_state(-1)
def dwave_chimera_graph(
    m,
    n=None,
    t=4,
    draw_inter_weight=draw_inter_weight,
    draw_intra_weight=draw_intra_weight,
    draw_other_weight=draw_inter_weight,
    seed=0,
):
    """
    Generate DWave Chimera graph as described in [1] using dwave_networkx.

    Parameters
    ----------
    m: int
        Number of cells per column
    n: int
        Number of cells per row
    t: int
        Number of nodes on each side of a bipartite cell subgraph
    draw_inter_weight: function (seed) -> number
        Function to call for weights of inter-cell edges
    draw_intra_weight: function (seed) -> number
        Function to call for weights of intra-cell edges
    draw_other_weight: function (seed) -> number
            Function to call for weights of intra-cell edges
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    graph: nx.Graph
        The generated Chimera graph

    References
    ----------
    ..[1] https://docs.ocean.dwavesys.com/en/latest/concepts/topology.html
    """
    if not n:
        n = m
    g = dwave.chimera_graph(m, n, t)
    _initialize_weights_chimera(
        chimera_graph=g,
        size=m,
        draw_inter_weight=lambda: draw_inter_weight(seed),
        draw_intra_weight=lambda: draw_intra_weight(seed),
        draw_other_weight=lambda: draw_other_weight(seed),
    )
    return g


@py_random_state(-1)
def mgw(m=8, faulty=73, seed=0):
    """
    Generates McGeoch-Wang instances as described in [1].


    Parameters
    ----------
    m: int
        Chimera graph size parameter (produces mxm lattice)
    faulty: int
        Number of faulty nodes
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    graph: nx.Graph
        The generated Chimera graph

    References
    ----------
    ..[1] Michael Juenger, Elisabeth Lobe, Petra Mutzel, Gerhard Reinelt, Franz Rendl, Giovanni Rinaldi,
        & Tobias Stollenwerk. (2019). Performance of a Quantum Annealer for Ising Ground State Computations
        on Chimera Graphs.
    """

    def draw(seed):
        seed.choice((1, -1))

    graph = dwave_chimera_graph(
        m=m,
        draw_inter_weight=draw,
        draw_intra_weight=draw,
        draw_other_weight=draw,
        seed=seed,
    )
    faulty_nodes = set(seed.choices(range(graph.number_of_nodes()), k=faulty))
    to_be_removed_edges = set()
    for u, v in graph.edges():
        if u in faulty_nodes or v in faulty_nodes:
            to_be_removed_edges.add((u, v))
    graph.remove_edges_from(to_be_removed_edges)
    return graph
