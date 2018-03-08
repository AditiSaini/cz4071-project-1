import matplotlib.pyplot as plt
import networkx as nx
import graph

if __name__ == "__main__":
    plt.rcParams["figure.figsize"] = (11, 7)
    g = nx.Graph()
    own_graph = graph.Graph("../datasets/tpch-graph.txt")
    degrees = own_graph.get_degrees()
    for v in own_graph.get_vertices():
        if degrees[v] > 1080: # k = 3
            for w in own_graph.neighbor_of(v):
                g.add_edge(v, w)
    options = {
        'node_color': 'black',
        'node_size': 0.1,
        'width': 0.05,
    }
    nx.draw_random(g, **options)
    #nx.draw_spring(g, **options)
    plt.show()
