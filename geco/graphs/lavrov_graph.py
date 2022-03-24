import networkx as nx


def lavrov_graph(
        k
):
    """
    Generate Lavrov graph as described in [1] using networkx.

    Parameters
    ----------
    k: int
       Number k for Lavrov graph, number of nodes is 2 * k

    Returns
    -------
    graph: nx.Graph
        The generated Lavrov graph

    References
    ----------
    ..[1] https://math.stackexchange.com/questions/2811736/an-upper-bound-on-the-number-of-chordless-cycles-in-an-undirected-graph/2811761#2811761
    """

    g = nx.Graph()
    g.add_nodes_from([0,2 * k - 1])

    for i in range(0, k):
        g.add_edge(i, (i + 1) % k)
        g.add_edge(i + k, (i + 1) % k + k)
        g.add_edge(i, (i + 1) % k + k)
        g.add_edge(i + k, (i + 1) % k)

    return g
