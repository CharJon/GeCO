import itertools

import networkx as nx
import pyscipopt as scip


def independent_set(graph: nx.Graph, name: str = "Independent Set") -> scip.Model:
    """
    Generates an independent set according to [1].

    Parameters
    ----------
    graph: nx.Graph
        Networkx undirected graph
    name: str
        name of the generated model

    Returns
    -------
    model: scip.Model
        pyscipopt model of the generated instance

    References
    ----------
    .. [1] https://www.princeton.edu/~aaa/Public/Teaching/ORF523/S16/ORF523_S16_Lec11_gh.pdf
    """
    model = scip.Model(name)

    vars = {
        str(node): model.addVar(lb=0, ub=1, obj=1, name=str(node), vtype="B")
        for node in graph.nodes
    }

    for u, v in itertools.combinations(graph.nodes, 2):
        model.addCons(vars[str(u)] + vars[str(v)] <= 1)

    model.setMaximize()

    return model
