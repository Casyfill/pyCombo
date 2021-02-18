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


#include "Combo.h"
#include "Graph.h"

#include <algorithm>
#include <chrono>
#include <cmath>
#include <iostream>
#include <optional>
#include <random>
using namespace std;

#define THRESHOLD 1e-6


vector<double> Sum(const vector< vector<double> >& matrix)
{
	int n = matrix.size();
	vector<double> res(n, 0.0);
	for (int i = 0; i < n; ++i)
		for (int j = 0; j < n; ++j)
			res[i] += matrix[i][j];
	return res;
}

template<typename T> bool Positive(T x) {return x > 0.0;}
template<typename T> bool Negative(T x) {return x < 0.0;}
template<typename T> bool NotNegative(T x) {return x >= 0.0;}
template<typename T> bool NotPositive(T x) {return x <= 0.0;}
vector<double> SumPos(const vector< vector<double> >& matrix, bool (*Pred)(double) = NULL)
{
	int n = matrix.size();
	vector<double> res(n, 0.0);
	for (int i = 0; i < n; ++i)
		for (int j = 0; j < n; ++j)
			if (Pred && Pred(matrix[i][j]))
				res[i] += matrix[i][j];
	return res;
}

template<typename T>
bool TestAll(const vector<T>& vec, bool (*Pred)(T))
{
	int n = vec.size();
	for (int i = 0; i < n; ++i)
		if (!Pred(vec[i]))
			return false;
	return true;
}

double ModularityGain(const vector< vector<double> >& Q, const vector<double>& correction_vector, const vector<int>& community)
{
	int n = community.size();
	double mod_gain = 0.0;
	for (int i = 0; i < n; ++i) {
		for (int j = 0; j < n; ++j)
			if (community[i] == community[j])
				mod_gain += Q[i][j];
			else
				mod_gain -= Q[i][j];
	}
	mod_gain *= 0.5;
	for (int i = 0; i < n; ++i) {
		if (community[i])
			mod_gain += correction_vector[i];
		else
			mod_gain -= correction_vector[i];
	}
	return mod_gain;
}

//perform a split improvement using a Kernighan-Lin-style iterative shifts series
double PerformKernighansShift(const vector< vector<double> >& Q, const vector<double>& correction_vector,
	const vector<int>& communities_old, vector<int>& communities_new)
{
 	int n = Q.size();
	vector<double> gains(n, 0.0);
	for (int i = 0; i < n; ++i) {
		for (int j = 0; j < n; ++j)
			if (i != j) {
				if (communities_old[i] == communities_old[j])
					gains[i] -= Q[i][j];
				else
					gains[i] += Q[i][j];
			}
		if (communities_old[i])
			gains[i] -= correction_vector[i];
		else
			gains[i] += correction_vector[i];
		gains[i] *= 2;
	}
	vector<double> gains_got(n, 0.0);
	vector<int> gains_indexes(n, 0);
	communities_new = communities_old;
	for (int i = 0; i < n; ++i) {
		vector<double>::iterator it = max_element(gains.begin(), gains.end());
		gains_got[i] = *it;
		int gains_ind = it - gains.begin();
		gains_indexes[i] = gains_ind;
		if (i > 0)
			gains_got[i] = gains_got[i] + gains_got[i-1];
		for (int j = 0; j < n; ++j)
			if (communities_new[gains_ind] == communities_new[j])
				gains[j] += 4 * Q[gains_ind][j];
			else
				gains[j] -= 4 * Q[gains_ind][j];
		communities_new[gains_ind] = !communities_new[gains_ind];
		gains[gains_ind] = gains[gains_ind] - 2*n;
	}
	vector<double>::iterator it = max_element(gains_got.begin(), gains_got.end());
	double mod_gain = *it;
	int steps_to_get_max_gain = it - gains_got.begin() + 1;
	if (mod_gain > 0) {
		communities_new = communities_old;
		for (int i = 0; i < steps_to_get_max_gain; ++i)
			communities_new[gains_indexes[i]] = !communities_new[gains_indexes[i]];
	} else {
		communities_new = communities_old;
		mod_gain = 0;
	}
	return mod_gain;
}

//try to split the subnetwork with respect to the correction vector
double ComboAlgorithm::Split(vector< vector<double> >& Q,
	const vector<double>& correction_vector, vector<int>& to_be_moved)
{
	double mod_gain = 0.0;
	vector<double> sumQ = Sum(Q);
	int n = Q.size();
	for (int i = 0; i < n; ++i)
		Q[i][i] += 2 * correction_vector[i] - sumQ[i]; //adjust the submatrix
	int tries;
	if (m_num_split_attempts > 0)
		tries = m_num_split_attempts;
	else
		tries = pow(abs(log(m_current_best_gain)), m_autoC2) / m_autoC1 + 3;
	for (int tryI = 1; tryI <= tries; ++tryI)
	{
		vector<int> communities(n); // 0 - stay in origin, 1 - move to destination
		//perform an initial simple split
		if (m_fixed_split_step > 0 && tryI <= 6 * m_fixed_split_step && tryI % m_fixed_split_step == 0) {
			//perform one of predifined split types
			int fixed_split_type = tryI / m_fixed_split_step;
			if (fixed_split_type == 1 || fixed_split_type == 2)
				communities.assign(n, 2 - fixed_split_type);
			else {
				vector<double> sum_pos = SumPos(Q, Positive);
				int node_ind;
				if (fixed_split_type == 3 || fixed_split_type == 4)
					node_ind = max_element(sum_pos.begin(), sum_pos.end()) - sum_pos.begin();
				else
					node_ind = min_element(sum_pos.begin(), sum_pos.end()) - sum_pos.begin();  
				communities.assign(n, -1);
				int community = 1;
				communities[node_ind] = community;
				while (true) {
					int next_node_ind = -1;
					double cur_min = 1e300;
					double cur_max = -1e300;
					for (int i = 0; i < n; ++i) {
						if (communities[i] == -1) {
							if ((fixed_split_type == 3 || fixed_split_type == 5) && Q[node_ind][i] < cur_min) {
								next_node_ind = i;
								cur_min = Q[node_ind][i];
							} else if ((fixed_split_type == 4 || fixed_split_type == 6) && Q[node_ind][i] > cur_max) {
								next_node_ind = i;
								cur_max = Q[node_ind][i];
							}
						}
					}
					if (next_node_ind == -1)
						break;
					node_ind = next_node_ind;
					community ^= 1;
					communities[node_ind] = community;
				}
			}
		} else {
			for (int i = 0; i < n; ++i)
				communities[i] = int(m_bernoulli_distribution(m_random_number_generator));
		}

		double mod_gain_total = ModularityGain(Q, correction_vector, communities);
		double mod_gain_from_shift = 1;
		while (mod_gain_from_shift > THRESHOLD) {
			vector<int> communities_shifted(n);
			mod_gain_from_shift = PerformKernighansShift(Q, correction_vector, communities, communities_shifted);
			if (mod_gain_from_shift > THRESHOLD) {
				mod_gain_total += mod_gain_from_shift;
				communities = communities_shifted;
				if (m_debug_verify) {
					double mod_gain_verify = ModularityGain(Q, correction_vector, communities);
					if (fabs(mod_gain_verify - mod_gain_total) > THRESHOLD)
						cerr << "ERROR" << endl;
				}

			}
		}
		if (mod_gain < mod_gain_total) {
			to_be_moved = communities;
			mod_gain = mod_gain_total;
		}
		if (mod_gain <= 1e-6)
			tries = int(tries / 2);
	}

	if (fabs(mod_gain) < THRESHOLD)
		to_be_moved.assign(n, 1);

	return mod_gain;
}

void ComboAlgorithm::ReCalc(Graph& graph, vector< vector<double> >& moves, vector< vector<int> >& splits_communities, int origin, int destination)
{
	moves[origin][destination] = 0;
	if (origin != destination) {
		vector<int> orig_comm_ind = graph.CommunityIndices(origin);
		if (!orig_comm_ind.empty()) {
			vector<double> correction_vector = graph.GetCorrectionVector(orig_comm_ind, graph.CommunityIndices(destination));
			vector<int> to_be_moved(orig_comm_ind.size());
			vector< vector<double> > Q = graph.GetModularitySubmatrix(orig_comm_ind);
			moves[origin][destination] = Split(Q, correction_vector, to_be_moved);
			for (size_t i = 0; i < to_be_moved.size(); ++i)
				splits_communities[destination][orig_comm_ind[i]] = to_be_moved[i];
		}
	}
}

double BestGain(const vector< vector<double> >& moves, int& origin, int& destination)
{
	double best_gain = -1;
	for (size_t i = 0; i < moves.size(); ++i)
		for (size_t j = 0; j < moves.size(); ++ j)
			if (best_gain < moves[i][j]) {
				best_gain = moves[i][j];
				origin = i;
				destination = j;
			}
	return best_gain;
}

void DeleteEmptyCommunities(Graph& graph, vector< vector<double> >& moves, vector< vector<int> >& splits_communities, int origin)
{
	if (graph.DeleteCommunityIfEmpty(origin)) {
		int comm_number = graph.NumberOfCommunities();
		for (int i = origin; i < comm_number; ++i)
			moves[i] = moves[i+1];
		moves[comm_number].assign(comm_number+2, 0);
		for (size_t i = 0; i < moves.size(); ++i) {
			for (int j = origin; j < comm_number+1; ++j)
				moves[i][j] = moves[i][j+1];
			moves[i][comm_number+1] = 0;
		}
		for (int i = origin; i < comm_number+1; ++i)
			splits_communities[i] = splits_communities[i+1];
	}
}

void ComboAlgorithm::Run(Graph& graph, int max_comunities)
{
	if (max_comunities <= 0)
		max_comunities = graph.Size();
	graph.SetCommunities(vector<int>(graph.Size(), 0));
	double currentMod = graph.Modularity();
	vector< vector<double> > moves(2, vector<double>(2, 0)); //results of splitting communities
	//vectors of boolean meaning that corresponding vertex should be moved to dest
	vector< vector<int> > splits_communities(2, vector<int>(graph.Size(), 0)); //best split vectors
	m_current_best_gain = 1;
	int origin = 0, destination = 0;
	for (origin = 0; origin < graph.NumberOfCommunities(); ++ origin)
		for (destination = 0; destination < graph.NumberOfCommunities() + (graph.NumberOfCommunities() < max_comunities); ++destination)
			ReCalc(graph, moves, splits_communities, origin, destination);
	m_current_best_gain = BestGain(moves, origin, destination);
	while (m_current_best_gain > THRESHOLD) {
		bool comunity_added = destination >= graph.NumberOfCommunities();
		graph.PerformSplit(origin, destination, splits_communities[destination]);
		if (m_debug_verify) {
			double oldMod = currentMod;
			currentMod = graph.Modularity();
			if (fabs(currentMod - oldMod - m_current_best_gain) > THRESHOLD)
				cerr << "ERROR" << endl;
		}
		if (comunity_added && destination < max_comunities - 1) {
			if (destination + 1 >= int(moves.size())) {
				for (size_t i = 0; i < moves.size(); ++i)
					moves[i].push_back(0);
				moves.push_back(vector<double>(moves.size() + 1, 0));
				splits_communities.push_back(vector<int>(graph.Size(), 0));
			}
			for (int i = 0; i < destination; ++i) {
				moves[i][destination+1] = moves[i][destination];
				splits_communities[destination+1] = splits_communities[destination];
			}
		}
		for (int i = 0; i < graph.NumberOfCommunities() + (graph.NumberOfCommunities() < max_comunities); ++i) {
			ReCalc(graph, moves, splits_communities, origin, i);
			ReCalc(graph, moves, splits_communities, destination, i);
			if (i != destination && i < graph.NumberOfCommunities())
				ReCalc(graph, moves, splits_communities, i, origin);
			if (i != origin && i < graph.NumberOfCommunities())
				ReCalc(graph, moves, splits_communities, i, destination);
		}
		DeleteEmptyCommunities(graph, moves, splits_communities, origin); //remove origin community if empty
		m_current_best_gain = BestGain(moves, origin, destination);
	}
}

void ComboAlgorithm::SetNumberOfSplitAttempts(int split_tries)
{
	if (split_tries <= 0) {
		if (split_tries == -1) {
			m_autoC1 = 1.5*log(10);
			m_autoC2 = 1;
		} else if (split_tries == -2) {
			m_autoC1 = log(10);
			m_autoC2 = 1;
		} else {
            m_autoC1 = 2;
            m_autoC2 = 1.5;
		}  
	}
	m_num_split_attempts = split_tries;
}

ComboAlgorithm::ComboAlgorithm(optional<unsigned long long> random_seed, int num_split_attempts, int fixed_split_step) :
	m_fixed_split_step(fixed_split_step),
	m_random_number_generator(random_seed.has_value() ? random_seed.value() :
		std::chrono::duration_cast<std::chrono::milliseconds>(
			std::chrono::steady_clock::now().time_since_epoch()).count()),
	m_bernoulli_distribution(0.5)
{
	SetNumberOfSplitAttempts(num_split_attempts);
}

ComboAlgorithm::ComboAlgorithm(): 
	ComboAlgorithm(std::chrono::duration_cast<std::chrono::milliseconds>(
		std::chrono::steady_clock::now().time_since_epoch()).count(), 0, 0)
{}

ComboAlgorithm::ComboAlgorithm(int num_split_attempts, int fixed_split_step) :
	ComboAlgorithm(std::chrono::duration_cast<std::chrono::milliseconds>(
		std::chrono::steady_clock::now().time_since_epoch()).count(), num_split_attempts, fixed_split_step)
{}
