from __future__ import division
from collections import deque

class GraphAnalyzer:
    def __init__(self, graph):
        self.graph = graph

    def compute_average_degree(self):
        return self.graph.get_edge_count() / self.graph.get_vertex_count()

    def compute_betweenness_centrality(self, sources):
        """
        Compute between-ness centrality
        """
        if not hasattr(self, "bc_values"):
            self.bc_values = [0.0 for i in self.graph.get_vertices()]
        # compute BC
        if len(sources) == 0:
            sources = self.graph.get_vertices()
        for source in sources:
            # initialization
            dependencies = [0.0 for i in self.graph.get_vertices()]
            distances = [1000000000 for i in self.graph.get_vertices()]
            sigma = [0 for i in self.graph.get_vertices()]
            predecessors = [[] for i in self.graph.get_vertices()]
            q = deque()
            s = []
            # update source
            distances[source] = 0
            q.append(source)
            while len(q) != 0:
                v = q.popleft()
                s.append(v)
                for w in self.graph.neighbor_of(v):
                    if distances[w] == 1000000000:
                        distances[w] = distances[v] + 1
                        q.append(w)
                    if distances[w] == distances[v] + 1:
                        sigma[w] += 1
                        predecessors[w].append(v)
            while len(s) != 0:
                v = s.pop()
                for predecessor in predecessors[v]:
                    dependencies[predecessor] += (sigma[predecessor] / sigma[v]) * (1.0 + dependencies[v])
                if v != source:
                    self.bc_values[v] += dependencies[v]
