import sys
from graph import Graph
from analyzer import GraphAnalyzer

if __name__ == "__main__":
    graph = Graph(sys.argv[1])
    analyzer = GraphAnalyzer(graph)
    print("Average degree: " + str(analyzer.compute_average_degree()))
    print("|V|: " + str(graph.get_vertex_count()))
    print("|E|: " + str(graph.get_edge_count()))
    print("Neighbor of vertex 0: " + str(graph.neighbor_of(0)))
    analyzer.compute_betweenness_centrality([])
    print("Betweenness: " + str(len(analyzer.bc_values)))
    analyzer.compute_degree_correlation()
    print("Degree correlation: " + str(analyzer.knn))
