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

    def degree_distribution(self):
        ''' get the graph degree distribution '''
        distribution = {}
        for k in self.graph.get_degrees():
            if k not in distribution:
                distribution[k] = 0
            distribution[k] += 1
        return distribution

    def degree_prob_distribution(self):
        distribution = {}
        for k, count in self.degree_distribution().items():
            distribution[k] = float(count) / self.graph.get_vertex_count()
        return distribution

    def edge_prob_distribution(self):
        distribution = {}
        degrees = self.graph.get_degrees()
        for v in range(self.graph.get_vertex_count()):
            source_degree = degrees[v]
            for n in self.graph.neighbor_of(v):
                target_degree = degrees[n]
                # undirected graph
                edge_pair = (source_degree, target_degree) if source_degree < target_degree else (target_degree, source_degree)
                if edge_pair not in distribution:
                    distribution[edge_pair] = 0

                distribution[edge_pair] += 1

        for edge_pair, count in distribution.items():
            distribution[edge_pair] = float(count) / float(self.graph.get_edge_count())
        return distribution
    
    def degree_connection_prob(self, i, j):
        # the conditional prob of a i-degree node connecting with a j-degree node
        # for neutral network
        qk = float(i * self.degree_prob_distribution()[i]) / float(self.compute_average_degree())
        edge_pair = (i, j) if i < j else (j, i)
        edge_prob_distribution = self.edge_prob_distribution()
        e = edge_prob_distribution[edge_pair] if edge_pair in edge_prob_distribution else 0
        return float(e) / float(qk)
    
    def compute_degree_correlation(self):
        knn = {}
        possible_degrees = set(self.graph.get_degrees())
        for k in possible_degrees:
            total = 0
            for k_prime in possible_degrees:
                total += k_prime * self.degree_connection_prob(k, k_prime)
            knn[k] = total
        self.knn = knn

    def compute_local_clustering_coef(self, v):
        k = self.graph.get_degrees()[v]
        neighbors = self.graph.neighbor_of(v)
        num_edges_btw_neighbors = 0
        for i in neighbors:
            i_neighbors = self.graph.neighbor_of(i)
            num_edges_btw_neighbors += len(set().union(neighbors, i_neighbors))

        return float(num_edges_btw_neighbors) / float(k*(k-1))

    def compute_avg_clustering_coef(self):
        local_coef_sum = 0
        vertex_count = self.graph.get_vertex_count()
        for i in range(vertex_count):
            local_coef_sum += self.compute_local_clustering_coef(i)
        self.avg_clustering_coef = local_coef_sum / float(vertex_count)

    def compute_closeness(self):
        return

    def compute_distance(self):
        # small world property
        return
    

