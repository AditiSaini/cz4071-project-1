#include <fstream>
#include <sstream>
#include <iostream>

#include "graph_loader.h"

using namespace std;

void sequential::common::LoadGraph(const std::string& graph_file,
		bool weighted,
		std::vector<uint32_t>* index,
		std::vector<uint32_t>* edges,
		std::vector<uint32_t>* weights,
		uint32_t* num_of_vertices,
		uint32_t* num_of_edges,
		uint32_t delta)
{
	// open file
	ifstream graph_ifs(graph_file);
	if (!graph_ifs.is_open())
	{
		cerr << "Cannot open graph file, exiting." << endl;
		exit(EXIT_FAILURE);
	}
	else
	{
		cerr << "Start loading graph." << endl;
	}

	// read in |V| and |E|
	string line;
	getline(graph_ifs, line);
	stringstream sstream(line);
	sstream >> *num_of_vertices >> *num_of_edges;
	index->reserve(*num_of_vertices + 1);
	edges->reserve(*num_of_edges);

	// read the adjacency list
	uint32_t dest;
	for (uint32_t src = 0; src < *num_of_vertices; ++src)
	{
		getline(graph_ifs, line);
		stringstream line_stream(line);
		index->push_back(edges->size());
		while (line_stream >> dest)
			edges->push_back(dest);
	}
	index->push_back(edges->size());

	cerr << "Finish loading graph." << endl;
}
