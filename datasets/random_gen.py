from networkx.generators.random_graphs import fast_gnp_random_graph

if __name__ == "__main__":
    g = fast_gnp_random_graph(258000, 0.00001)
    with open("random.txt", "w") as random_output:
        for v, neibdict in g.adjacency():
            first = True
            for w, attr in neibdict.items():
                if first:
                    random_output.write(str(w))
                    first = False
                else:
                    random_output.write(" " + str(w))
            random_output.write("\n")
