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

#include "Graph.h"

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <set>
#include <algorithm>
using std::ifstream;
using std::ofstream;
using std::string;
using std::vector;
using std::set;
using std::max;
using std::cout;
using std::endl;
using std::min;

Graph::Graph(void)
{
	m_size = 0;
	m_totalWeight = 0.0;
	m_isOriented = false;
	m_communityNumber = 0;
}


Graph::~Graph(void)
{
}

void Graph::FillMatrix(const vector<int>& src, const vector<int>& dst, const vector<double>& weight)
{
	int m = min(*min_element(src.begin(), src.end()), *min_element(dst.begin(), dst.end()));
	if(m > 0)
		m = 1;
	if(!m_isOriented)
		m_totalWeight *= 2;
	m_size = 1 + max(*max_element(src.begin(), src.end()), *max_element(dst.begin(), dst.end())) - m;
	m_matrix.assign(m_size, vector<double>(m_size, 0));
	for(int i = 0; i < src.size(); ++i)
	{
		m_matrix[src[i]-m][dst[i]-m] += weight[i];
		if(!m_isOriented)
			m_matrix[dst[i]-m][src[i]-m] += weight[i];
	}
}

void Graph::FillModMatrix(const vector<int>& src, const vector<int>& dst, const vector<double>& weight)
{
	int m = min(*min_element(src.begin(), src.end()), *min_element(dst.begin(), dst.end()));
	if(m > 0)
		m = 1;
	m_size = 1 + max(*max_element(src.begin(), src.end()), *max_element(dst.begin(), dst.end())) - m;
	if(!m_isOriented)
		m_totalWeight *= 2;
	m_modMatrix.assign(m_size, vector<double>(m_size, 0));
	vector<double> sumQ2(m_size, 0.0);
	vector<double> sumQ1(m_size, 0.0);
	for(int i = 0; i < src.size(); ++i)
	{
		m_modMatrix[src[i]-m][dst[i]-m] += weight[i] / m_totalWeight;
		if(!m_isOriented)
			m_modMatrix[dst[i]-m][src[i]-m] += weight[i] / m_totalWeight;
	
		sumQ1[src[i]-m] += weight[i] / m_totalWeight;
		sumQ2[dst[i]-m] += weight[i] / m_totalWeight;
		if(!m_isOriented)
		{
			sumQ1[dst[i]-m] += weight[i] / m_totalWeight;
			sumQ2[src[i]-m] += weight[i] / m_totalWeight;
		}
	}
	for(int i = 0; i < m_size; ++i)
		for(int j = 0; j < m_size; ++j)
			m_modMatrix[i][j] -= sumQ1[i]*sumQ2[j];
	for(int i = 0; i < m_size; ++i)
		for(int j = 0; j < m_size; ++j)
			m_modMatrix[i][j] = m_modMatrix[j][i] = (m_modMatrix[i][j] + m_modMatrix[j][i]) / 2;
}

void Graph::ReadFromEdgelist(const std::string& fname)
{
	ifstream file(fname.c_str());
	if(!file.is_open())
		return;
	vector<int> src, dst;
	vector<double> weight;
	while(file.good())
	{
		char buff[256];
		file.getline(buff, 255);
		int s = -1, d = -1;
		double w = 1.0;
		sscanf(buff, "%d %d %lf", &s, &d, &w);
		if(s != -1 && d != -1)
		{
			src.push_back(s);
			dst.push_back(d);
			weight.push_back(w);
			m_totalWeight += w;
		}
	}
	file.close();
	FillModMatrix(src, dst, weight);
}

void Graph::ReadFromPajeck(const std::string& fname)
{
	ifstream file(fname.c_str());
	if(!file.is_open())
		return;
	vector<int> src, dst;
	vector<double> weight;
	bool skip = true;
	while(file.good())
	{
		char buff[256];
		file.getline(buff, 255);
		string line = buff;
		if(line == "*Edges")
		{
			skip = false;
			m_isOriented = false;
		}
		else if(line == "*Arcs")
		{
			skip = false;
			m_isOriented = true;
		}
		else if(!skip)
		{
			int s = -1, d = -1;
			double w = 1.0;
			sscanf(buff, "%d %d %lf", &s, &d, &w);
			if(s != -1 && d != -1)
			{
				src.push_back(s);
				dst.push_back(d);
				weight.push_back(w);
				m_totalWeight += w;
			}
		}
	}
	file.close();
	FillModMatrix(src, dst, weight);
}

double Graph::EdgeWeight(int i, int j) const
{
	return m_matrix[i][j];
}

void Graph::CalcModMtrix()
{
	if(!m_modMatrix.empty())
		return;

	m_modMatrix.assign(m_size, vector<double>(m_size, 0.0));
	for(int i = 0; i < m_size; ++i)
		for(int j = 0; j < m_size; ++j)
			m_modMatrix[i][j] = EdgeWeight(i, j) / m_totalWeight;
	
	vector<double> sumQ2(m_size, 0.0);
	vector<double> sumQ1(m_size, 0.0);
	for(int i = 0; i < m_size; ++i)
		for(int j = 0; j < m_size; ++j)
		{
			sumQ1[i] += m_modMatrix[i][j];
			sumQ2[j] += m_modMatrix[i][j];
		}
	for(int i = 0; i < m_size; ++i)
		for(int j = 0; j < m_size; ++j)
			m_modMatrix[i][j] -= sumQ1[i]*sumQ2[j];
	for(int i = 0; i < m_size; ++i)
		for(int j = 0; j < m_size; ++j)
			m_modMatrix[i][j] = m_modMatrix[j][i] = (m_modMatrix[i][j] + m_modMatrix[j][i]) / 2;
}

void Graph::Print() const
{
	cout << "Matrix:" << endl;
	for(int i = 0; i < m_size; ++i)
	{
		for(int j = 0; j < m_size; ++j)
		{
			cout << m_matrix[i][j] << '\t';
		}
		cout << endl;
	}
	cout << "Modularity matrix:" << endl;
	for(int i = 0; i < m_size; ++i)
	{
		for(int j = 0; j < m_size; ++j)
		{
			cout << m_modMatrix[i][j] << '\t';
		}
		cout << endl;
	}
}

void Graph::PrintCommunity(const string& fileName) const
{
	ofstream file(fileName.c_str());
	if(!file.is_open())
		return;
	for(int i = 0; i < m_size; ++i)
		file << m_communities[i] << endl;
	file.close();
}

void Graph::SetCommunities(const vector<int>& new_communities, int number)
{
	if(m_size != new_communities.size())
		return;
	m_communities = new_communities;
	if(number == -1)
		m_communityNumber = *max_element(m_communities.begin(), m_communities.end()) + 1;
	else
		m_communityNumber = number;
}

double Graph::Modularity() const
{
	double mod = 0;
	for(int i = 0; i < m_modMatrix.size(); ++i)
		for(int j = 0; j < m_modMatrix.size(); ++j)
			if(m_communities[i] == m_communities[j])
				mod += m_modMatrix[i][j];
	return mod;
}

void Graph::PerformSplit(int origin, int dest, const vector<int>& split_communities)
{
	if(dest > m_communityNumber)
		dest = m_communityNumber;
	if(dest == m_communityNumber)
		++m_communityNumber;
	for(int i = 0; i < m_size; ++i)
		if(m_communities[i] == origin && split_communities[i])
			m_communities[i] = dest;
}

bool Graph::IsCommunityEmpty(int comm) const
{
	for(int i = 0; i < m_size; ++i)
		if(m_communities[i] == comm)
			return false;
	return true;
}

bool Graph::DeleteCommunityIfEmpty(int comm)
{
	if(IsCommunityEmpty(comm))
	{
		set<int> comms;
        for(int i = 0; i < m_size; ++i)
		{
			if(m_communities[i] > comm)
				--m_communities[i];
			comms.insert(m_communities[i]);
		}
		m_communityNumber = comms.size();
        return true;
	}
	return false;
}

vector<int> Graph::CommunityIndices(int comm) const
{
	vector<int> res;
	for(int i = 0; i < m_size; ++i)
	{
		if(m_communities[i] == comm)
			res.push_back(i);
	}
	return res;
}

vector< vector<double> > Graph::GetModularitySubmatrix(const vector<int>& indices) const
{
	vector< vector<double> > res(indices.size(), vector<double>(indices.size()));
	for(int i = 0; i < indices.size(); ++i)
		for(int j = 0; j < indices.size(); ++j)
			res[i][j] = m_modMatrix[indices[i]][indices[j]];
	return res;
}

vector<double> Graph::GetCorrectionVector(const vector<int>& origCommInd, const vector<int>& destCommInd) const
{
	vector<double> res(origCommInd.size(), 0.0);
	for(int i = 0; i < origCommInd.size(); ++i)
		for(int j = 0; j < destCommInd.size(); ++j)
			res[i] += m_modMatrix[destCommInd[j]][origCommInd[i]];
	return res;
}
