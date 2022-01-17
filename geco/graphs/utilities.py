import math

import networkx as nx


def edgeweight_properties(graph, weight_label="weight"):
    """
    Calculates properties of edge weights.

    Parameters
    ----------
    graph: nx.Graph
        Graph to calculate the properties from
    weight_label:


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
        weight = d[weight_label]
        if weight > max_weight:
            max_weight = weight
        if weight < min_weight:
            min_weight = weight
        if weight == 0:
            num_of_zero_weights += 1

    return max_weight, min_weight, num_of_zero_weights


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

    Notes
    -----
    Accepts both undirected and directed graphs.
    If the graph is undirected, this implementation finds all parallel
    edges twice (once from both vertices), then filters out the duplicate.
    """
    all_parallel_edges = []
    for node in graph:
        for neighbor in graph.neighbors(node):
            num_of_edges = graph.number_of_edges(node, neighbor)
            if num_of_edges > 1:
                all_parallel_edges.append(((node, neighbor), num_of_edges - 1))

    if not graph.is_directed():
        filtered_parallel_edges = __remove_duplicate_parallel_edges(all_parallel_edges)
        return filtered_parallel_edges

    return all_parallel_edges


def __remove_duplicate_parallel_edges(all_parallel_edges):
    filtered_edges, seen = [], set()
    for parallel_edge_data in all_parallel_edges:
        edge = tuple(parallel_edge_data[0])
        if edge not in seen and tuple(reversed(parallel_edge_data[0])) not in seen:
            seen.add(edge)
            filtered_edges.append(parallel_edge_data)
    return filtered_edges


def graph_properties(graph, weight_label="weight"):
    """
    Calculates properties of edge weights.

    Parameters
    ----------
    graph: nx.Graph
        Graph to calculate the properties from
    weight_label: str
        Optional, which label to use as edge-weight
        If None no edge weight related statistics get collected

    Returns
    -------
    properties: dict
    A dict with the following calculated properties:
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
        number_of_selfloop_nodes: int
            Number of nodes that have a self-loop
        number_of_selfloops: int
            Total number of selfloops in the graph

    References
    ----------
    ..[1] https://networkx.org/documentation/stable//reference/algorithms/generated/networkx.algorithms.assortativity.degree_assortativity_coefficient.html
    ..[2] https://networkx.org/documentation/networkx-2.4/reference/algorithms/generated/networkx.algorithms.cluster.average_clustering.html
    ..[3] https://networkx.org/documentation/networkx-1.9/reference/generated/networkx.algorithms.core.core_number.html
    """

    avg_degree = sum((deg for node, deg in graph.degree)) / graph.number_of_nodes()
    density = graph.number_of_edges() / (
            (graph.number_of_nodes() * graph.number_of_nodes() - graph.number_of_nodes())
            / 2
    )
    planar, _ = nx.algorithms.check_planarity(graph)

    num_of_connected_components = nx.number_connected_components(graph)
    number_of_triangles = sum(nx.triangles(graph).values()) // 3
    max_degree = max(degree for _, degree in graph.degree())
    assortativity_coeff = (
        None  # TODO (JC): bug - nx.degree_assortativity_coefficient(g)
    )

    average_clustering_coeff = nx.average_clustering(g)
    max_k_core = max(nx.core_number(g).values())
    number_of_selfloop_nodes = len(list(nx.nodes_with_selfloops(g)))
    number_of_selfloops = len(list(nx.selfloop_edges(g)))


    d = {
        "num_nodes": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "avg_degree": avg_degree,
        "density": density,
        "planar": planar,
        "num_of_connected_components": num_of_connected_components,
        "max_degree": max_degree,
        "assortativity_coeff": assortativity_coeff,
        "number_of_triangles": number_of_triangles,
        "average_clustering_coeff": average_clustering_coeff,
        "max_k_core": max_k_core,
        "number_of_selfloop_nodes": number_of_selfloop_nodes,
        "number_of_selfloops": number_of_selfloops,
    }

    if weight_label:
        max_edgeweight, min_edgeweight, num_of_zero_edgeweights = edgeweight_properties(
            graph, weight_label
        )

        d = {**d,
             "max_edgeweight": max_edgeweight,
             "min_edgeweight": min_edgeweight,
             "num_of_zero_edgeweights": num_of_zero_edgeweights
             }

    return d
