import json

import networkx as nx

from geco.graphs import utilities as util

if __name__ == "__main__":
    g = nx.read_weighted_edgelist("path/to/some/weighted_edgelist_file.el")
    g_props = util.graph_properties(g)
    json.dump(g_props, open("res.json", 'w'))
