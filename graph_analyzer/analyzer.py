class GraphAnalyzer:
    def __init__(self, graph):
        self.graph = graph

    def compute_average_degree(self):
        return self.graph.get_edge_count() / self.graph.get_vertex_count()
