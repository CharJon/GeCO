import json

import networkx as nx

from geco.graphs import utilities as util


def skip_first_line(path):
    f = open(path, 'r')
    first_line = f.readline()
    return f


if __name__ == "__main__":
    g = nx.read_weighted_edgelist("/path/to/some/edgelist.el")
    # if the first line contains information but no edge
    # might become unnecessary with https://github.com/networkx/networkx/discussions/4596
    g = nx.read_weighted_edgelist(skip_first_line("/path/to/some/edgelist.el"))

    g_props = util.graph_properties(g)
    json.dump(g_props, open("res.json", 'w'))
