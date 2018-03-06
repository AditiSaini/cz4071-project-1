import sys
from graph import Graph
from analyzer import GraphAnalyzer

if __name__ == "__main__":
    graph = Graph(sys.argv[1])
    analyzer = GraphAnalyzer(graph)
    print("Average degree: " + str(round(analyzer.compute_average_degree(), 5)))
    print("|V|: " + str(graph.get_vertex_count()))
    print("|E|: " + str(graph.get_edge_count()))
    print("Neighbor of vertex 0: " + str(graph.neighbor_of(0)))
    analyzer.compute_sssp_related_properties([])
    print("Betweenness: " + str(len(analyzer.bc_values)))
    print("Avg path length: " + str(round(analyzer.avg_path_length, 5)))
    print("Closeness: " + str(len(analyzer.close_values)))
    analyzer.compute_degree_correlation()
    print("Degree correlation: " + str(analyzer.knn))
    print("1st moment: " + str(round(analyzer.compute_nth_moment(1), 5)))
    print("2nd moment: " + str(round(analyzer.compute_nth_moment(2), 5)))
    print("3rd moment: " + str(round(analyzer.compute_nth_moment(3), 5)))
