from networkx.generators.random_graphs import barabasi_albert_graph
from networkx.generators.directed import scale_free_graph

if __name__ == "__main__":
    g = barabasi_albert_graph(300000, 1)
    #g = scale_free_graph(258000)
    with open("scale_free.txt", "w") as random_output:
        for v, neibdict in g.adjacency():
            first = True
            for w, attr in neibdict.items():
                if first:
                    random_output.write(str(w))
                    first = False
                else:
                    random_output.write(" " + str(w))
            random_output.write("\n")
