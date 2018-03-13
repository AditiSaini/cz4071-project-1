import sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
import graph
import pandas as pd
import numpy as np
import os
import pickle
import math

def plot_curve(data, x_label, y_label, title, save_as, log=False, h_line=None, v_line=None):
    x = list(data.keys())
    y = list(data.values())
    if log:
        # Remove zeros for log-log plots
        for k in x:
            if k == 0 or data[k] == 0:
                del data[k]
        x = [math.log(i) for i in data.keys()]
        y = [math.log(i) for i in data.values()]
    plt.scatter(x, y, s=10)
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

def plot_heatmap(graph, pos, hubs, data, save_as):
    dataframe = pd.DataFrame(data, columns=['value'])
    dataframe.apply(lambda x: ((x - np.mean(x)) / (np.max(x) - np.min(x)))*225)
    dataframe = dataframe.reindex(graph.nodes())
    # Providing a continuous color scale with cmap
    node_size = []
    for i in (graph.nodes()):
        if i not in hubs:
            node_size.append(0.6)
        else:
            # enlarge hub size
            node_size.append(5)
    opts = {
        "node_color":dataframe['value'],
        'node_size': node_size, #0.6, 
        'with_labels': False,
        "pos":pos,
        "cmap":plt.cm.plasma
    }

    nodes = nx.draw_networkx_nodes(graph, **opts)
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1))
    edges = nx.draw_networkx_edges(graph, pos, width=0.05)

    plt.colorbar(nodes)
    plt.axis('off')
    plt.savefig(save_as)    
    plt.show()  

def plot_gragh(graph, save_dir):
    pos = nx.random_layout(graph)
    options = {
        'pos': pos,
        'node_color': 'black',
        'node_size': 0.7,
        'width': 0.05,
    }
    nx.draw(graph, **options)
    plt.savefig(os.path.join(save_dir, 'graph.png')) 
    plt.show()
    return pos

def draw_properties(graph, pos, hubs, degrees, save_dir):
    with open(os.path.join(save_dir, "properties.pkl"), "rb") as f:
        property_info_dict = pickle.load(f)

    degree_corr = property_info_dict["degree_correlation"]
    degree_distribution = property_info_dict["degree_distribution"]
    clustering_coef = property_info_dict["clustering_coef"]

    plot_curve(clustering_coef, "log(k)", "log(C(k))", "Clustering Coefficient",
            save_as=os.path.join(save_dir, "clustering_coef.png"),
            log=True, 
            h_line=property_info_dict["avg_clustering_coef"])
    plot_curve(degree_corr, "log(k)", "log(knn)", "Degree Correlation", 
            save_as=os.path.join(save_dir, "degree_corr.png"), 
            log=True)
    plot_curve(degree_distribution, "log(k)", "log(P(k))", "Degree Distribution",
            save_as=os.path.join(save_dir, "degree_distribution.png"),
            log=True,
            v_line=property_info_dict["avg_degree"])

    bc_values = property_info_dict["bc_values"]
    cc_values = property_info_dict["closeness"]
    bc_degree = {}
    cc_degree = {}
    for i in range(len(degrees)):
        k = degrees[i]
        if cc_values[i] > 5000:
            continue
        if k not in bc_degree:
            bc_degree[k] = [bc_values[i]]
        else:
            bc_degree[k].append(bc_values[i])
        if k not in cc_degree:
            cc_degree[k] = [cc_values[i]]
        else:
            cc_degree[k].append(cc_values[i])
    for k in bc_degree.keys():
        bc_degree[k] = sum(bc_degree[k])/float(len(bc_degree[k]))
        cc_degree[k] = sum(cc_degree[k])/float(len(cc_degree[k]))

    plot_curve(bc_degree, "log(k)", "log(bc)", "Betweenness v.s. Degree",
            log=True,
            save_as=os.path.join(save_dir, "bc_degree.png"))
    plot_curve(cc_degree, "log(k)", "log(cc)", "Closeness v.s. Degree",
            log=True,
            save_as=os.path.join(save_dir, "cc_degree.png"))

    bc_cc = {}
    for i in range(len(degrees)):
        if cc_values[i] > 5000:
            continue
        bc_cc[bc_values[i]] = cc_values[i]
    plot_curve(bc_cc, "log(bc)", "log(cc)", "Betweenness v.s. Closeness",
            log=True,
            save_as=(os.path.join(save_dir, "bc_cc.png")))

    plot_heatmap(graph, pos, hubs, bc_values, 
                save_as=os.path.join(save_dir, 'betweenness.png'))
    plot_heatmap(graph, pos, hubs, cc_values, 
                save_as=os.path.join(save_dir,'closeness.png'))


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python plot.py /path/to/graph /path/to/analysis/result <k>")
        exit()
    k = int(sys.argv[3])
    plt.rcParams["figure.figsize"] = (11, 7)
    nx_graph = nx.Graph()
    own_graph = graph.Graph(sys.argv[1])
    degrees = own_graph.get_degrees()
    hubs = []
    matplotlib.rcParams.update({'font.size': 20})
    for v in own_graph.get_vertices():
        if degrees[v] > k:
            hubs.append(v)
            for w in own_graph.neighbor_of(v):
                nx_graph.add_edge(v, w)
    result_dir = sys.argv[2]
    if nx_graph.nodes():
        pos = plot_gragh(nx_graph, result_dir)
        draw_properties(nx_graph, pos, hubs, degrees, result_dir)
    else:
        print("There is no node satisfying your degree threshold.")
