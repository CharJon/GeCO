import dwave_networkx as dwave
from networkx import write_weighted_edgelist
from random import random
import numpy as np
from networkx.utils import py_random_state


def draw_intra_weight(seed):
    return seed.random() - 0.5


def draw_inter_weight(seed):
    return seed.random() * 2 - 1


def _initialize_weights_pegasus(
    pegasus_graph, size, draw_inter_weight, draw_intra_weight, draw_other_weight
):
    # 'nice' coordinate indices names (as per d-wave's documentation):
    p_coor = dwave.pegasus_coordinates(size)

    for _from, _to in pegasus_graph.edges:
        _from_nice = p_coor.linear_to_nice(_from)
        _to_nice = p_coor.linear_to_nice(_to)
        if not in_chimera_subgraph(_from_nice, _to_nice):
            pegasus_graph.add_edge(_from, _to, weight=draw_other_weight())
        else:
            if in_same_chimera_tile(_from_nice, _to_nice):
                # edge from one side to the other (internal edge)
                if not on_same_side(_from_nice, _to_nice):
                    pegasus_graph.add_edge(_from, _to, weight=draw_intra_weight())
                else:  # odd couplers
                    pegasus_graph.add_edge(_from, _to, weight=draw_other_weight())
            else:
                pegasus_graph.add_edge(_from, _to, weight=draw_inter_weight())


def in_chimera_subgraph(_from_nice, _to_nice):
    t = 0
    return _from_nice[t] + _to_nice[t] == 0


def on_same_side(_from_nice, _to_nice):
    u = 3
    return _from_nice[u] == _to_nice[u]


def in_same_chimera_tile(_from_nice, _to_nice):
    y, x = 1, 2
    return _from_nice[y] == _to_nice[y] and _from_nice[x] == _to_nice[x]


@py_random_state(-1)
def dwave_pegasus_graph(
    size,
    draw_inter_weight=draw_inter_weight,
    draw_intra_weight=draw_intra_weight,
    draw_other_weight=draw_inter_weight,
    seed=0,
):
    """
    Generate DWave Pegasus graph as described in [1] using dwave_networkx.

    Parameters
    ----------
    size: int
       Size of generated pegasus graph
    draw_inter_weight: function (seed) -> number
        Function to call for weights of inter-cell edges
    draw_intra_weight: function (seed) -> number
        Function to call for weights of intra-cell edges
    draw_other_weight: function (seed) -> number
        Function to call for weights of intra-cell edges

    Returns
    -------
    graph: nx.Graph
        The generated Pegasus graph

    References
    ----------
    ..[1] https://docs.ocean.dwavesys.com/en/latest/concepts/topology.html
    """
    g = dwave.pegasus_graph(size)
    _initialize_weights_pegasus(
        pegasus_graph=g,
        size=size,
        draw_inter_weight=lambda: draw_inter_weight(seed),
        draw_intra_weight=lambda: draw_intra_weight(seed),
        draw_other_weight=lambda: draw_other_weight(seed),
    )
    return g
