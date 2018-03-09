#ifndef SEQUENTIAL_ALGORITHM_BRANDES_H_
#define SEQUENTIAL_ALGORITHM_BRANDES_H_

#include <vector>

namespace sequential {
namespace algorithm {

void RunBrandes(const std::vector<uint32_t>& sources,
		uint32_t num_of_vertices,
		const std::vector<uint32_t>& index,
		const std::vector<uint32_t>& edges,
		const std::vector<uint32_t>& weights,
		bool weighted);

}
}

#endif
