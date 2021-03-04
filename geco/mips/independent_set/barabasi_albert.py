import networkx as nx
import pyscipopt as scip

from geco.mips.independent_set.generic import independent_set


def barabasi_albert_params(n, m, seed=0):
    """
    Generates a maximum independent set instance params of graphs described in [1].

    Parameters
    ----------
    n: int
        Number of nodes
    m: int
        Number of edges to attach from a new node to existing nodes
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    graph: nx.Graph
        A Barabasi-Albert Networkx graph

    References
    ----------
    .. [1] A. L. Barabási and R. Albert “Emergence of scaling in random networks”, Science 286, pp 509-512, 1999.
    """
    return nx.generators.barabasi_albert_graph(n, m, seed)


def barabasi_albert_instance(n, m, seed=0):
    """
    Generates a maximum independent set instance of graphs described in [1].

    Parameters
    ----------
    n: int
        Number of nodes
    m: int
        Number of edges to attach from a new node to existing nodes
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the instance.

    References
    ----------
    .. [1] A. L. Barabási and R. Albert “Emergence of scaling in random networks”, Science 286, pp 509-512, 1999.
    """
    return independent_set(
        barabasi_albert_params(n, m, seed), name="Barabasi-Albert Independent Set"
    )
