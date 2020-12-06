/*                                                                            
    Copyright 2014
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

#pragma once

#include <string>
#include <vector>
#include <set>

class Graph
{
public:
	Graph(void);
	virtual ~Graph(void);

	void ReadFromEdgelist(const std::string& fname, double mod_resolution);
	void ReadFromPajeck(const std::string& fname, double mod_resolution);
	void CalcModMtrix();

	int Size() const {return m_size;}
	int CommunityNumber() const {return m_communityNumber;};
	double EdgeWeight(int i, int j) const;
	bool IsCommunityEmpty(int comm) const;

	double Modularity() const;
	std::vector< std::vector<double> > GetModularitySubmatrix(const std::vector<int>& indices) const;
	std::vector<double> GetCorrectionVector(const std::vector<int>& origCommInd, const std::vector<int>& destCommInd) const;
	
	void SetCommunities(const std::vector<int>& new_communities, int number = -1);
	std::vector<int> Communities() const {return m_communities;};
	std::vector<int> CommunityIndices(int comm) const;

	void PerformSplit(int origin, int dest, const std::vector<int>& split_communities);
	bool DeleteCommunityIfEmpty(int comm);
	void Print() const;
	void PrintCommunity(const std::string& fileName) const;

private:
	void FillMatrix(const std::vector<int>& src, const std::vector<int>& dst, const std::vector<double>& weight);
	void FillModMatrix(const std::vector<int>& src, const std::vector<int>& dst, const std::vector<double>& weight, double mod_resolution);

private:
	int m_size;
	double m_totalWeight;
	int m_communityNumber;
	bool m_isOriented;
	std::vector<std::vector<double> > m_matrix;
	std::vector<std::vector<double> > m_modMatrix;
	std::vector<int> m_communities;
};

