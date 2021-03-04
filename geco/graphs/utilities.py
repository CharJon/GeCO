import networkx as nx
import math


def edgeweight_properties(graph):
    """
    Calculates properties of edge weights.

    Parameters
    ----------
    graph: nx.Graph
        Graph to calculate the properties from

    Returns
    -------
    max_weight: number
        Maximum weights of an edge
    min_weight: number
        Minimum weight of an edge
    num_of_zero_weights: int
        Number of edges with zero weight
    """
    max_weight = -math.inf
    min_weight = math.inf
    num_of_zero_weights = 0
    for u, v, d in graph.edges(data=True):
        weight = d["weight"]
        if weight > max_weight:
            max_weight = weight
        if weight < min_weight:
            min_weight = weight
        if weight == 0:
            num_of_zero_weights += 1

    return max_weight, min_weight, num_of_zero_weights


def graph_properties(g):
    """
    Calculates properties of edge weights.

    Parameters
    ----------
    graph: nx.Graph
        Graph to calculate the properties from

    Returns
    -------
    num_nodes: int
        Number of nodes of the graph
    num_edges: int
        Number of edges of the graph
    avg_degree: float
        Average degree of node
    density: float
        Number of edges divided by the number of possible edges
    planar: bool
        Whether the graph is planar or not
    max_edgeweight: float
        Maximum weights of an edge
    min_edgeweight: float
        Minimum weight of an edge
    num_of_zero_weights: int
        Number of edges with zero weight
    num_of_connected_components: int
        Number of connected components in the graph
    max_degree: int
        Maximum degree of a node in the graph
    assortativity_coeff: float
        The degree assortativity coefficient as defined in [1]
    number_of_triangles: int
        Number of traingles in the graph
    average_clustering_coeff: float
        Average clustering coefficient as defined in [2]
    max_k_core: int
        Maximum k-core as defined in [3]

    References
    ----------
    ..[1] https://networkx.org/documentation/stable//reference/algorithms/generated/networkx.algorithms.assortativity.degree_assortativity_coefficient.html
    ..[2] https://networkx.org/documentation/networkx-2.4/reference/algorithms/generated/networkx.algorithms.cluster.average_clustering.html
    ..[3] https://networkx.org/documentation/networkx-1.9/reference/generated/networkx.algorithms.core.core_number.html
    """

    avg_degree = sum((deg for node, deg in g.degree)) / g.number_of_nodes()
    density = g.number_of_edges() / (
        (g.number_of_nodes() * g.number_of_nodes() - g.number_of_nodes()) / 2
    )
    planar, _ = nx.algorithms.check_planarity(g)
    max_edgeweight, min_edgeweight, num_of_zero_edgeweights = edgeweight_properties(g)
    num_of_connected_components = nx.number_connected_components(g)
    number_of_triangles = sum(nx.triangles(g).values()) // 3
    max_degree = max(degree for _, degree in g.degree())
    assortativity_coeff = nx.degree_assortativity_coefficient(g)
    average_clustering_coeff = nx.average_clustering(g)
    max_k_core = max(nx.core_number(g).values())

    return {
        "num_nodes": g.number_of_nodes(),
        "num_edges": g.number_of_edges(),
        "avg_degree": avg_degree,
        "density": density,
        "planar": planar,
        "max_edgeweight": max_edgeweight,
        "min_edgeweight": min_edgeweight,
        "num_of_zero_edgeweights": num_of_zero_edgeweights,
        "num_of_connected_components": num_of_connected_components,
        "max_degree": max_degree,
        "assortativity_coeff": assortativity_coeff,
        "number_of_triangles": number_of_triangles,
        "average_clustering_coeff": average_clustering_coeff,
        "max_k_core": max_k_core,
    }
