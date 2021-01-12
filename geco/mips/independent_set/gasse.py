import networkx as nx
import pyscipopt as scip

from geco.mips.independent_set.generic import clique_independent_set


def gasse_params(n, p, seed=0):
    """
    Generates a maximum independent set instance as described in [1].

    Parameters
    ----------
    n: int
        Number of nodes.
    p: float
        Edge probability
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    graph: nx.Graph
        An Erdos-Renyi Networkx graph

    References
    ----------
    .. [1] "Exact Combinatorial Optimization with Graph Convolutional Neural Networks" (2019)
      Maxime Gasse, Didier Chételat, Nicola Ferroni, Laurent Charlin and Andrea Lodi
      Advances in Neural Information Processing Systems 32 (2019)
    """
    return nx.generators.erdos_renyi_graph(n, p, seed)


def gasse_instance(n, p, seed=0):
    """
    Generates a maximum independent set instance as described in [1].

    Parameters
    ----------
    n: int
        Number of nodes.
    p: float
        Edge probability
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the instance.

    References
    ----------
    .. [1] "Exact Combinatorial Optimization with Graph Convolutional Neural Networks" (2019)
      Maxime Gasse, Didier Chételat, Nicola Ferroni, Laurent Charlin and Andrea Lodi
      Advances in Neural Information Processing Systems 32 (2019)
    """
    return clique_independent_set(
        gasse_params(n, p, seed), name="Gasse Independent Set"
    )
