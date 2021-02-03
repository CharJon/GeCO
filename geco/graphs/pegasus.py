import dwave_networkx as dwave
from networkx import write_weighted_edgelist
from random import random
import numpy as np
from networkx.utils import preserve_random_state

__all__ = ["dwave_pegasus_graph"]


def draw_intra_weight():
    return random() - 0.5


def draw_inter_weight():
    return random() * 2 - 1


def _initialize_weights_pegasus(
    pegasus_graph, size, draw_inter_weight, draw_intra_weight, draw_other_weight
):
    # 'nice' coordinate indices names (as per d-wave's documentation):
    n = 0
    t, y, x, u, k = range(5)

    p_coor = dwave.pegasus_coordinates(size)

    for _from, _to in pegasus_graph.edges:
        _from_nice = p_coor.linear_to_nice(_from)
        _to_nice = p_coor.linear_to_nice(_to)
        # if any of the nodes is not in the chimera subgraph (at t=0)
        if _from_nice[t] + _to_nice[t] > 0:
            pegasus_graph.add_edge(_from, _to, weight=draw_other_weight())
        else:
            if _from_nice[y] == _to_nice[y] and _from_nice[x] == _to_nice[x]:
                n += 1
                # edge from one side to the other (internal edge)
                if _from_nice[u] != _to_nice[u]:
                    pegasus_graph.add_edge(_from, _to, weight=draw_intra_weight())
                else:  # odd couplers
                    pegasus_graph.add_edge(_from, _to, weight=draw_other_weight())
            else:
                pegasus_graph.add_edge(_from, _to, weight=draw_inter_weight())


@preserve_random_state
def dwave_pegasus_graph(
    size,
    seed=0,
    draw_inter_weight=draw_inter_weight,
    draw_intra_weight=draw_intra_weight,
    draw_other_weight=draw_inter_weight,
):
    np.random.seed(seed)
    g = dwave.pegasus_graph(size)
    _initialize_weights_pegasus(
        g, size, draw_inter_weight, draw_intra_weight, draw_other_weight
    )
    return g
