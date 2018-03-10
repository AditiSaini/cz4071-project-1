import sys
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
import graph
import pandas as pd
import numpy as np
import os
import pickle
import math

def plot_curve(x, y, x_label, y_label, title, save_as, log=False, h_line=None, v_line=None):
    if log:
        print(x)
        x = [math.log(i) for i in x]
        y = [math.log(i) for i in y]
    plt.scatter(x, y, s=20*0.1)
    if h_line:
        if log:
            h_line = math.log(h_line)
        plt.axhline(h_line, color='r')
    if v_line:
        if log:
            v_line = math.log(v_line)
        plt.axvline(v_line, color='r')

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(save_as)
    plt.show()

def plot_heatmap(graph, input_file, save_as, title):
    data = pd.read_csv(input_file, names=['value'])
    data.apply(lambda x: ((x - np.mean(x)) / (np.max(x) - np.min(x)))*225)
    data = data.reindex(graph.nodes())
    # Plot it, providing a continuous color scale with cmap:
    pos = nx.random_layout(graph)
    opts = {
        "node_color":data['value'],
        'node_size': 0.2,
        'with_labels': False,
        "pos":pos,
        "cmap":plt.cm.plasma
    }

    nodes = nx.draw_networkx_nodes(graph, **opts)
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1))
    
    # labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(graph, pos, width=0.05)

    plt.title(title)
    plt.colorbar(nodes)
    plt.axis('off')
    plt.savefig(save_as)    
    plt.show()  

def plot_gragh(graph, save_dir):
    options = {
        'node_color': 'black',
        'node_size': 0.1,
        'width': 0.05,
    }
    nx.draw_random(graph, **options)
    plt.savefig(os.path.join(save_dir, 'graph.png'))    
    plt.show()

def draw_properties(graph, save_dir):
    with open(os.path.join(save_dir, "properties.pkl"), "rb") as f:
        property_info_dict = pickle.load(f)

    degree_corr = property_info_dict["degree_correlation"]
    degree_distribution = property_info_dict["degree_distribution"]
    clustering_coef = property_info_dict["clustering_coef"]
    # degrees = property_info_dict['degrees']

    plot_curve(clustering_coef.keys(), clustering_coef.values(), "k", "Ck", "Clustering Coef", 
            save_as=os.path.join(save_dir, "clustering_coef.png"),
            log=True, 
            h_line=property_info_dict["avg_clustering_coef"])
    plot_curve(degree_corr.keys(), degree_corr.values(), "k", "knn", "Degree Correlation", 
            save_as=os.path.join(save_dir, "degree_corr.png"), 
            log=True)
    plot_curve(degree_distribution.keys(), degree_distribution.values(), "k", "prob", "Degree Distribution", 
            save_as=os.path.join(save_dir, "degree_distribution.png"),
            log=True,
            v_line=property_info_dict["avg_degree"])

    plot_heatmap(graph, input_file=os.path.join(save_dir, 'bc_output.txt'), 
                save_as=os.path.join(save_dir, 'betweenness.png'), 
                title='Between-ness Centrality')
    plot_heatmap(graph, input_file=os.path.join(save_dir, 'close_output.txt'), 
                save_as=os.path.join(save_dir,'closeness.png'),
                title='Closeness Centrality')

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python plot.py /path/to/graph /path/to/analysis/result <k>")
        exit()
    k = int(sys.argv[3])
    plt.rcParams["figure.figsize"] = (11, 7)
    nx_graph = nx.Graph()
    own_graph = graph.Graph(sys.argv[1])
    degrees = own_graph.get_degrees()
    for v in own_graph.get_vertices():
        if degrees[v] > k:
            for w in own_graph.neighbor_of(v):
                nx_graph.add_edge(v, w)
    result_dir = sys.argv[2]
    plot_gragh(nx_graph, result_dir)
    draw_properties(nx_graph, result_dir)
