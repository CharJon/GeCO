import networkx as nx
import pyscipopt as scip

from geco.mips.independent_set.generic import independent_set


def barabasi_albert_params(n, m, seed=0):
    return nx.generators.barabasi_albert_graph(n, m, seed)


def barabasi_albert_instance(n, m, seed=0):
    """
    Generates a maximum independent set instance of graphs described in [1].

    Parameters
    ----------
    n: int
        number of nodes.
    m: int
        edge probability
    seed: int, random state or None
        randomization seed

    Returns
    -------
    model: scip.Model
        pyscipopt model of the instance.

    References
    ----------
    .. [1] A. L. Barabási and R. Albert “Emergence of scaling in random networks”, Science 286, pp 509-512, 1999.
    """
    return independent_set(
        barabasi_albert_params(n, m, seed), name="Barabasi-Albert Independent Set"
    )
