#include <chrono>
#include <iostream>
#include <fstream>
#include <queue>
#include <stack>

#include "brandes.h"

using namespace std;

const uint32_t INF = 1000000000;

void sequential::algorithm::RunBrandes(const vector<uint32_t>& sources,
		uint32_t num_of_vertices,
		const vector<uint32_t>& index,
		const vector<uint32_t>& edges,
		const vector<uint32_t>& weights,
		bool weighted)
{
	vector<float> bc(num_of_vertices, 0.0f);
	vector<float> closeness(num_of_vertices, 0.0f);
	uint64_t total_path_length = 0;
	uint64_t total_path_count = 0;
	float avg_path_length;
	float bc_base = static_cast<float>((num_of_vertices - 1) * (num_of_vertices - 2));

	for (auto&& source : sources)
	{
		if (source % 100 == 0)
			cerr << "Computed for " << source << " sources." << endl;
		//cerr << "Computing BC for source " << source << endl;
		//auto t1 = chrono::steady_clock::now();
		/*
		 * First phase: SSSP with path counting
		 */
		vector<uint32_t> distances(num_of_vertices, INF);
		vector<uint32_t> sigma(num_of_vertices, 0);
		vector<vector<uint32_t> > predecessors(num_of_vertices);
		stack<uint32_t> s;

		sigma.at(source) = 1;
		distances.at(source) = 0;
		queue<uint32_t> q;
		q.push(source);

		while (!q.empty())
		{
			uint32_t v = q.front();
			q.pop();
			s.push(v);
			uint32_t e_end = index.at(v + 1);
			for (uint32_t i = index.at(v); i < e_end; ++i)
			{
				uint32_t dst = edges.at(i);
				if (distances.at(dst) == INF)
				{
					q.push(dst);
					distances.at(dst) = distances.at(v) + 1;
				}
				if (distances.at(dst) == distances.at(v) + 1)
				{
					sigma.at(dst) += sigma.at(v);
					predecessors.at(dst).push_back(v);
				}
			}
		}

		/*
		 * Second phase: dependency accumulation
		 */
		vector<float> dependencies(num_of_vertices, 0.0f);
		while (!s.empty())
		{
			uint32_t v = s.top();
			s.pop();
			for (auto&& pre : predecessors.at(v))
				dependencies.at(pre) += (static_cast<float>(sigma.at(pre)) / static_cast<float>(sigma.at(v))) *
					(1.0f + dependencies.at(v));
			if (v != source)
				bc.at(v) += dependencies.at(v);
		}
		
		/*
		 * Third phase: closeness centrality & avg path length
		 */
		uint32_t total_length_from_source = 0;
		for (auto&& dist : distances)
		{
			if (dist != INF && dist != 0)
			{
				++total_path_count;
				total_length_from_source += dist;
				total_path_length += dist;
			}
		}
		closeness.at(source) = static_cast<float>(total_length_from_source);

		//auto t2 = chrono::steady_clock::now();
		//auto diff = t2 - t1;
		//cout << "Elapsed time " << chrono::duration_cast<chrono::milliseconds>(diff).count() << "ms" << endl;
	}
	avg_path_length = static_cast<double>(total_path_length) / static_cast<double>(total_path_count);

	// final output
	cout << avg_path_length << endl;
	ofstream bc_output("bc_output.txt");
	for (auto&& val : bc)
		bc_output << val / bc_base << endl;
	ofstream c_output("close_output.txt");
	for (auto&& val : closeness)
		c_output << static_cast<float>(num_of_vertices - 1) / val << endl;
}
