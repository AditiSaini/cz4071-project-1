#ifndef SEQUENTIAL_COMMON_GRAPH_LOADER_H_
#define SEQUENTIAL_COMMON_GRAPH_LOADER_H_

#include <utility>
#include <string>
#include <vector>

namespace sequential {
namespace common {

void LoadGraph(const std::string& graph_file,
		bool weighted,
		std::vector<uint32_t>* index,
		std::vector<uint32_t>* edges,
		std::vector<uint32_t>* weights,
		uint32_t* num_of_vertices,
		uint32_t* num_of_edges,
		uint32_t delta);

void LoadEdgeList(const std::string& graph_file,
		std::vector<std::pair<uint32_t, std::pair<uint32_t, uint32_t> > >* edges,
		uint32_t* num_of_vertices,
		uint32_t* num_of_edges);

}
}

#endif
