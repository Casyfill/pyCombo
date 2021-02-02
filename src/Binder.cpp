#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

using namespace std;
namespace py = pybind11;


std::tuple< vector<int>, double> combo(std::string fileName,
		  int max_communities=-1,
		  double mod_resolution=1.0,
		  bool use_fix_tries=false,
		  int random_seed=42)
{
	// Struct s;
	srand(random_seed);


	if(max_communities== -1)
		// printf("MAX_COMMUNITIES SET TO: INF\n");
		max_communities = INF;

	Graph G;
	std::string ext = fileName.substr(fileName.rfind('.'), fileName.length() - fileName.rfind('.'));
	if(ext == ".edgelist")
		G.ReadFromEdgelist(fileName, mod_resolution);
	else if(ext == ".net")
		G.ReadFromPajeck(fileName, mod_resolution);
	if(G.Size() <= 0)
	{
		cerr << "Error: graph is empty" << std::endl;
		return std::make_tuple(vector<int>(), -1.0);
	}

	RunCombo(G, max_communities);

	return std::make_tuple(G.m_communities, G.Modularity());

}

std::tuple< vector<int>, double> combo_array(
		  std::vector< std::vector<int> > networkarray,
		  std::vector<double> weights,
		  bool directed=false,
		  int max_communities=-1,
		  double mod_resolution=1.0,
		  bool use_fix_tries=false,
		  int random_seed=42)
{
	srand(random_seed);


	if(max_communities== -1)
		max_communities = INF;

	Graph G;
	G.ReadFromArrays(networkarray, weights, mod_resolution, directed);
	RunCombo(G, max_communities);

	return std::make_tuple(G.m_communities, G.Modularity());

}


PYBIND11_MODULE(combo, m) {
    m.doc() = "combo partition Python binding"; // optional module docstring

	m.def("execute", &combo, "execute combo partition on graph",
		py::arg("graph_path"), py::arg("max_communities"), py::arg("mod_resolution"), py::arg("use_fix_tries"), py::arg("random_seed")
		);

	m.def("executearray", &combo_array, "execute combo partition on graph by passing network array",
	  py::arg('narray'), py::arg("weights_array"), py::arg("directed"), py::arg("mod_resolution"), py::arg("use_fix_tries"), py::arg("random_seed")
	);
}
