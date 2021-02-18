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

#ifndef COMBO_H
#define COMBO_H

#include "Graph.h"
#include <optional>
#include <random>
#include <vector>

class ComboAlgorithm {
public:
    ComboAlgorithm();
    explicit ComboAlgorithm(std::optional<unsigned long long> random_seed, int num_split_attempts, int fixed_split_step);
    ComboAlgorithm(int num_split_attempts, int fixed_split_step);
    void Run(Graph& graph, int max_comunities = -1);
    void SetFixedSplitStep(int fixed_split_step) {m_fixed_split_step = fixed_split_step;}
    void SetNumberOfSplitAttempts(int split_tries);
private:
    //settings
    const bool m_debug_verify = false;
    // number of split attempts; 0 - autoadjust this number based on m_current_best_gain
    int m_num_split_attempts;
    // step number to apply predefined split; 0 - use only random splits
    // if >0 sets up the usage of 6 fixed type splits on every m_fixed_split_step
    int m_fixed_split_step;
    double m_autoC1;
    double m_autoC2;
    //implementation
    std::mt19937 m_random_number_generator;
    std::bernoulli_distribution m_bernoulli_distribution;
    double m_current_best_gain;
    void ReCalc(Graph& graph, std::vector< std::vector<double> >& moves,
        std::vector< std::vector<int> >& splits_communities, int origin, int destination);
    double Split(std::vector< std::vector<double> >& Q, const std::vector<double>& correction_vector, std::vector<int>& to_be_moved);
};

#endif //COMBO_H