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


def num_of_simple_cycles(graph):
    """
    Finds number of simple cycles

    Parameters
    ----------
    graph: nx.Graph
        Graph to find number of simple cycles in

    Returns
    -------
    num_of_simple_cycles: int
        Number of simple cycles in graph
    """
    if graph.is_directed():
        return len(list(nx.simple_cycles(graph)))
    else:
        graph = nx.DiGraph(graph)
        all_simple_cycles = list(nx.simple_cycles(graph))
        all_simple_cycles = filter(lambda x: len(x) > 2, all_simple_cycles)
        all_simple_cycles = set(map(lambda x: tuple(sorted(x)), all_simple_cycles))
        return len(list(all_simple_cycles))


def find_parallel_edges(graph):
    """
    Finds parallel edges (not total edges) between nodes and their amount.

    Parameters
    ----------
    graph: nx.Graph
        Graph to find parallel edges in

    Returns
    -------
    parallel_edges: list
        Edge as tuple, followed by number of parallel edges
    """
    all_parallel_edges = []
    for node in graph:
        for neighbor in graph.neighbors(node):
            num_of_edges = graph.number_of_edges(node, neighbor)
            if num_of_edges > 1:
                all_parallel_edges.append([(node, neighbor), num_of_edges - 1])

    if not graph.is_directed():
        filtered_edges, seen = [], set()
        for parallel_edge_data in all_parallel_edges:
            edge = tuple(parallel_edge_data[0])
            if edge not in seen and tuple(reversed(parallel_edge_data[0])) not in seen:
                seen.add(edge)
                filtered_edges.append(parallel_edge_data)
        return filtered_edges

    return all_parallel_edges


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
    num_of_simple_cycles: int
        Number of simple cycles in the graph

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
    assortativity_coeff = (
        None  # TODO (JC): bug - nx.degree_assortativity_coefficient(g)
    )
    average_clustering_coeff = nx.average_clustering(g)
    max_k_core = max(nx.core_number(g).values())
    number_of_simple_cycles = num_of_simple_cycles(g)

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
        "number_of_simple_cycles": number_of_simple_cycles,
    }
