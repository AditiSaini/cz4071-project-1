class Graph:
    def __init__(self, input_file):
        self.graph_file = input_file
        self.loaded = False
        self.read()

    def read(self):
        """
        Read the graph from the input file provided.
        Stores the graph internally in a compressed sparse row format.
        """
        if self.loaded:
            return
        self.vertices = []
        self.edges = []
        with open(self.graph_file, "r") as input_graph:
            for line in input_graph:
                self.vertices.append(len(self.edges))
                destinations = line.split(" ")
                for destination in destinations:
                    self.edges.append(int(destination))
        self.vertices.append(len(self.edges))
        # count |V| and |E|
        self.vertex_count = len(self.vertices) - 1
        self.edge_count = len(self.edges)
        self.loaded = True

    def neighbor_of(self, vertex):
        start_index = self.vertices[vertex]
        end_index = self.vertices[vertex + 1]
        return self.edges[start_index:end_index]

    def get_vertices(self):
        return range(self.get_vertex_count())

    def get_vertex_count(self):
        return self.vertex_count

    def get_edge_count(self):
        return self.edge_count
