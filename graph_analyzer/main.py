import sys
import pickle
import os
from graph import Graph
from analyzer import GraphAnalyzer
import matplotlib.pyplot as plt
import math

def compute_properties(graph, analyzer, save_dir):
    analyzer.compute_average_degree()
    print("Average degree: " + str(round(analyzer.avg_degree, 5)))
    print("largest k: " + str(analyzer.comptue_max_degree()))
    print("|V|: " + str(graph.get_vertex_count()))
    print("|E|: " + str(graph.get_edge_count()))
    print("Neighbor of vertex 0: " + str(graph.neighbor_of(0)))

    analyzer.compute_sssp_related_properties([0]) 
    print("Betweenness: " + str(len(analyzer.bc_values)))
    print("Avg path length: " + str(round(analyzer.avg_path_length, 5)))
    print("Closeness: " + str(len(analyzer.close_values)))

    analyzer.compute_degree_correlation()   
    print("Degree correlation: " + str(list(analyzer.knn.values())[:10]))
    analyzer.compute_degree_based_clustering_coef()
    analyzer.compute_avg_clustering_coef()    
    print("Avg clustering coef: " + str(analyzer.avg_clustering_coef))
    analyzer.compute_degree_prob_distribution() 

    property_info_dict = {"avg_degree" : analyzer.avg_degree,
                        "degree_distribution" : analyzer.degree_prob_distribution,
                        "degrees" : graph.get_degrees(),
                        "bc_values" : analyzer.bc_values,
                        "avg_path_len" : analyzer.avg_path_length,
                        "closeness" : analyzer.close_values,
                        "degree_correlation" : analyzer.knn,
                        "avg_clustering_coef" : analyzer.avg_clustering_coef,
                        "clustering_coef" : analyzer.degree_based_clustering_coef,
                        "1st_moment" : analyzer.compute_nth_moment(1),
                        "2nd_moment" : analyzer.compute_nth_moment(2),
                        "3rd_moment" : analyzer.compute_nth_moment(3)}

    # store the calculated properties for the graph
    with open(os.path.join(save_dir,"properties.pkl"), "wb") as f:
        pickle.dump(property_info_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py /path/to/graph/file /path/to/result/dir")
        exit()
    save_dir = sys.argv[2]  # the folder for storing the pkl file
    graph = Graph(sys.argv[1])
    analyzer = GraphAnalyzer(graph)
    compute_properties(graph, analyzer, save_dir)
