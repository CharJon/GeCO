import networkx as nx
from networkx.utils import py_random_state

from geco.mips.max_cut.generic import naive


@py_random_state(-1)
def tang_instance(n, m, seed=0):
    """
    Generates a max-cut instance as described in A.2 in [1].

    Parameters
    ----------
    n: int
        Number of nodes
    m: int
        Number of edges
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    model: scip.Model
        A pyscipopt model of the generated instance

    References
    ----------
    .. [1] Tang, Y., Agrawal, S., & Faenza, Y. (2019). Reinforcement learning for integer
    programming: Learning to cut. arXiv preprint arXiv:1906.04859.
    """
    graph = nx.generators.gnm_random_graph(n, m, seed=seed)
    weights = tang_params(graph, seed=0)
    for (_, _, data), weight in zip(graph.edges(data=True), weights):
        data["weight"] = weight
    _, model = naive(graph)
    return model


@py_random_state(-1)
def tang_params(graph, seed=0):
    """
    Generates max-cut instance params as described in A.2 in [1].

    Parameters
    ----------
    graph: nx.Graph
        Networkx graph
    seed: integer, random_state, or None
        Indicator of random number generation state

    Returns
    -------
    weights: list[int]
        Weight for each edge

    References
    ----------
    .. [1] Tang, Y., Agrawal, S., & Faenza, Y. (2019). Reinforcement learning for integer
    programming: Learning to cut. arXiv preprint arXiv:1906.04859.
    """
    weights = []
    for _ in graph.edges:
        weights.append(seed.randint(0, 10))
    return weights
