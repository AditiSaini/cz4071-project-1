#include <sys/time.h>
#include <sys/resource.h>
#include <chrono>
#include <fstream>
#include <iostream>
#include <string>

#include "graph_loader.h"
#include "brandes.h"

using namespace std;
using namespace sequential;

int main(int argc, char* argv[])
{
	/*
	 * Check input arguments
	 */
	if (argc != 4)
	{
		cout << "Usage: ./sssp <graph-file> <sources-file> <weighted>" << endl;
		exit(EXIT_FAILURE);
	}

	/*
	 * Get input arguments
	 */
	string graph_file(argv[1]);
	string sources_file(argv[2]);
	bool weighted = static_cast<bool>(atoi(argv[3]));

	/*
	 * Read graph from file
	 */
	vector<uint32_t> index, edges, weights;
	uint32_t num_of_vertices, num_of_edges;

	common::LoadGraph(graph_file, weighted, &index, &edges, &weights, &num_of_vertices, &num_of_edges, 0);

	/*
	 * Read source vertices from file
	 */
	//ifstream source_ifs(sources_file);
	//if (!source_ifs.is_open())
	//{
	//	cout << "Cannot open source list file." << endl;
	//	exit(EXIT_FAILURE);
	//}
	//uint32_t source;
	vector<uint32_t> source_list;
	//while (source_ifs >> source)
	//	source_list.push_back(source);
	source_list.reserve(num_of_vertices);
	for (uint32_t i = 0; i < num_of_vertices; ++i)
		source_list.push_back(i);

	/*
	 * Run the algorithm on source vertices
	 */
#ifdef NDEBUG
	auto t1 = chrono::steady_clock::now();
#endif
	algorithm::RunBrandes(source_list, num_of_vertices, index, edges, weights, weighted);
#ifdef NDEBUG
	auto t2 = chrono::steady_clock::now();
	auto diff = t2 - t1;
	cerr << "Elapsed time " << chrono::duration_cast<chrono::milliseconds>(diff).count() << "ms" << endl;
#endif
}
