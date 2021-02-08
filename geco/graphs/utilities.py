import networkx as nx
import math


def edgeweight_properties(graph):
    """
    Returns the maximum, minimum edgeweights and the number of edges with 0 weight (in that order)
    in one swipe from a given networkx graph
    """
    max_weight = - math.inf
    min_weight = math.inf
    num_of_zero_weights = 0
    for u, v, d in graph.edges(data=True):
        weight = d['weight']
        if weight > max_weight:
            max_weight = weight
        if weight < min_weight:
            min_weight = weight
        if weight == 0:
            num_of_zero_weights += 1

    return max_weight, min_weight, num_of_zero_weights


def graph_properties(g):
    avg_degree = sum((deg for node, deg in g.degree)) / g.number_of_nodes()
    density = g.number_of_edges() / ((g.number_of_nodes() * g.number_of_nodes() - g.number_of_nodes()) / 2)
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
        "max_k_core": max_k_core
    }
