from __future__ import division
from collections import deque
import math

class GraphAnalyzer:
    def __init__(self, graph):
        self.graph = graph

    def compute_average_degree(self):
        return self.graph.get_edge_count() / self.graph.get_vertex_count()

    def compute_sssp_related_properties(self, sources):
        """
        Computes SSSP based properties including average path length,
        betweenness centrality, and closeness centrality.
        """
        # initialization
        if not hasattr(self, "bc_values"):
            self.bc_values = [0.0 for i in self.graph.get_vertices()]
        if not hasattr(self, "total_path_length"):
            self.total_path_length = 0
        if not hasattr(self, "total_path_count"):
            self.total_path_count = 0
        if not hasattr(self, "close_values"):
            self.close_values = [0.0 for i in self.graph.get_vertices()]
        # set the list of source vertex
        if len(sources) == 0:
            sources = self.graph.get_vertices()
        # run
        for source in sources:
            self.compute_for_single_source(source)
        self.avg_path_length = self.total_path_length / self.total_path_count

    def compute_for_single_source(self, source):
        """
        Compute between-ness centrality
        """
        # initialization
        dependencies = [0.0 for i in self.graph.get_vertices()]
        distances = [1000000000 for i in self.graph.get_vertices()]
        sigma = [0 for i in self.graph.get_vertices()]
        predecessors = [[] for i in self.graph.get_vertices()]
        q = deque()
        s = []
        # run BFS
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
        # compute BC
        while len(s) != 0:
            v = s.pop()
            for predecessor in predecessors[v]:
                dependencies[predecessor] += (sigma[predecessor] / sigma[v]) * (1.0 + dependencies[v])
            if v != source:
                self.bc_values[v] += dependencies[v]
        # compute closeness and average path length
        total_length_from_source = 0
        total_path_count_from_source = 0
        for dist in distances:
            if dist != 1000000000 and dist != 0:
                total_length_from_source += dist
                total_path_count_from_source += 1
                self.total_path_length += dist
                self.total_path_count += 1
        self.close_values[source] = total_length_from_source / total_path_count_from_source

    def compute_degree_distribution(self):
        distribution = {}
        for k in self.graph.get_degrees():
            if k not in distribution:
                distribution[k] = 0
            distribution[k] += 1
        return distribution

    def compute_degree_prob_distribution(self):
        ''' Compute the graph degree probability distribution '''
        distribution = {}
        for k, count in self.compute_degree_distribution().items():
            distribution[k] = float(count) / self.graph.get_vertex_count()
        self.degree_prob_distribution = distribution
        return distribution

    def compute_edge_prob_distribution(self):
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
    
    def compute_degree_connection_prob(self, i, j):
        ''' 
        Compute the conditional prob of a i-degree node connecting with a j-degree node
        (for neutral network)
        '''
        qk = float(i * self.compute_degree_prob_distribution()[i]) / float(self.compute_average_degree())
        edge_pair = (i, j) if i < j else (j, i)
        edge_prob_distribution = self.compute_edge_prob_distribution()
        e = edge_prob_distribution[edge_pair] if edge_pair in edge_prob_distribution else 0
        return float(e) / float(qk)
    
    def compute_degree_correlation(self):
        knn = {} # store the relationship between the degrees of nodes that link to each other.
        possible_degrees = set(self.graph.get_degrees())
        for k in possible_degrees:
            total = 0
            for k_prime in possible_degrees:
                total += k_prime * self.compute_degree_connection_prob(k, k_prime)
            knn[k] = round(total, 5)
        self.knn = knn

    def compute_local_clustering_coef(self, v):
        ''' Compute the local clustering coefficient for v '''
        k = self.graph.get_degrees()[v]
        neighbors = self.graph.neighbor_of(v)
        num_edges_btw_neighbors = 0
        for i in neighbors:
            i_neighbors = self.graph.neighbor_of(i)
            num_edges_btw_neighbors += len(set().union(neighbors, i_neighbors))

        return float(num_edges_btw_neighbors) / float(k*(k-1))

    def compute_avg_clustering_coef(self):
        ''' Compute the overall average clustering coefficient for the network '''
        local_coef_sum = 0
        vertex_count = self.graph.get_vertex_count()
        for i in range(vertex_count):
            local_coef_sum += self.compute_local_clustering_coef(i)
        self.avg_clustering_coef = local_coef_sum / float(vertex_count)

    def comptue_max_degree(self):
        return max(self.graph.get_degrees())

    def compute_nth_moment(self, n):
        if hasattr(self, "degree_prob_distribution"):
            degree_probs = self.degree_prob_distribution
        else:
            degree_probs = self.compute_degree_prob_distribution()

        moment = 0
        for k,prob in degree_probs.items():
            moment += math.pow(k, n) * prob
        return moment

    

