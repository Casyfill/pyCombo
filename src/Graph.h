/*                                                                            
    Copyright 2021
    Alexander Belyi <alexander.belyi@gmail.com>,
    Stanislav Sobolevsky <stanly@mit.edu>                                               
                                                                            
    This file is part of Combo algorithm.

    Combo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Combo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Combo.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef GRAPH_H
#define GRAPH_H

#include <string>
#include <tuple>
#include <vector>

class Graph;

Graph ReadGraphFromFile(const std::string& file_name, double mod_resolution = 1, bool treat_as_modularity = false);

class Graph
{
public:
	explicit Graph(bool is_directed = false, double modularity_resolution = 1);
	Graph(int size, const std::vector<int>& sources, const std::vector<int>& destinations, const std::vector<double>& weights,
		bool is_directed, double modularity_resolution = 1, bool treat_as_modularity = false);
	Graph(int size, const std::vector<std::tuple<int, int, double>>& edges, bool is_directed,
		double modularity_resolution = 1, bool treat_as_modularity = false);
	explicit Graph(const std::vector<std::vector<double>>& matrix,
		double modularity_resolution = 1, bool treat_as_modularity = false);
	explicit Graph(std::vector<std::vector<double>>&& matrix,
		double modularity_resolution = 1, bool treat_as_modularity = false);
	Graph(const Graph& graph);
	Graph(Graph&& graph) noexcept;
	Graph& operator=(Graph graph);

	int Size() const {return int(m_modularity_matrix.size());}
	int IsDirected() const {return m_is_directed;}
	int ModularityResolution() const {return m_modularity_resolution;}
	int NumberOfCommunities() const {return m_number_of_communities;};

	double Modularity() const;
	std::vector< std::vector<double> > GetModularitySubmatrix(const std::vector<int>& indices) const;
	std::vector<double> GetCorrectionVector(const std::vector<int>& orig_comm_ind, const std::vector<int>& dest_comm_ind) const;
	
	void SetCommunities(const std::vector<int>& new_communities, int number = -1);
	std::vector<int> Communities() const {return m_communities;};
	std::vector<int> CommunityIndices(int comm) const;
	bool IsCommunityEmpty(int community) const;

	void PerformSplit(int origin, int destination, const std::vector<int>& split_communities);
	bool DeleteCommunityIfEmpty(int community);
	void Print() const;
	void PrintCommunity(const std::string& file_name) const;

	friend void swap(Graph& left, Graph& right);

private:
	void CalcModMatrix(int size, const std::vector<int>& sources, const std::vector<int>& destinations, const std::vector<double>& weights);
	void FillModMatrix(int size, const std::vector<int>& sources, const std::vector<int>& destinations, const std::vector<double>& weights);
	void CalcModMatrix(int size, const std::vector<std::tuple<int, int, double>>& edges);
	void FillModMatrix(int size, const std::vector<std::tuple<int, int, double>>& edges);
	void CalcModMatrix(const std::vector<std::vector<double>>& matrix);
	void FillModMatrix(const std::vector<std::vector<double>>& matrix);
	void FillModMatrix(std::vector<std::vector<double>>&& matrix);

private:
	int m_number_of_communities;
	bool m_is_directed;
	// Modularity Resolution Parameter
	// as per Newman 2016 (https://journals.aps.org/pre/abstract/10.1103/PhysRevE.94.052315)
	double m_modularity_resolution;
	std::vector<std::vector<double> > m_modularity_matrix;
	std::vector<int> m_communities;
};

#endif //GRAPH_H
