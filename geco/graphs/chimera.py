import numpy as np
import networkx as nx
from networkx.utils import py_random_state
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
    inter: function () -> number
        Function to call for weights of inter-cell edges
    intra: function () -> number
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


@py_random_state(-1)
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
        return np.random.randint(low=-10, high=10 + 1) / 10.0

    def intra_w():
        return np.random.randint(low=-5, high=5 + 1) / 10.0

    graph = chimera_graph(m, m, 4, inter=inter_w, intra=intra_w)

    # TODO: turn these asserts into tests
    assert graph.number_of_nodes() == m * m * 8
    assert graph.number_of_edges() == 24 * m * m - 8 * m

    graph.graph["name"] = f"selby_c{m}"
    graph.graph["seed"] = seed

    return graph


def _initialize_weights_chimera(
        chimera_graph, size, draw_inter_weight, draw_intra_weight
):
    y, x, u, k = range(4)

    c_coor = dwave.chimera_coordinates(size)
    for _from, _to in chimera_graph.edges:
        _from_nice = c_coor.linear_to_chimera(_from)
        _to_nice = c_coor.linear_to_chimera(_to)

        if _from_nice[y] == _to_nice[y] and _from_nice[x] == _to_nice[x]:
            # edge from one side to the other (internal edge)
            if _from_nice[u] != _to_nice[u]:
                chimera_graph.add_edge(_from, _to, weight=draw_intra_weight())
            else:  # odd couplers
                raise NotImplementedError()
        else:
            chimera_graph.add_edge(_from, _to, weight=draw_inter_weight())


@py_random_state(-1)
def dwave_chimera_graph(
        size,
        draw_inter_weight=draw_inter_weight,
        draw_intra_weight=draw_intra_weight,
        seed=0
):
    g = dwave.chimera_graph(size)
    _initialize_weights_chimera(chimera_graph=g,
                                size=size,
                                draw_inter_weight=lambda: draw_inter_weight(seed),
                                draw_intra_weight=lambda: draw_intra_weight(seed))
    return g
