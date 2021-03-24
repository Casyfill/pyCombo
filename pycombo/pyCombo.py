#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
from typing import Optional, Tuple, Union

import pycombo._combo as comboCPP
from pycombo.misc import deconstruct_graph, is_graph

__author__ = "Philipp Kats"
__copyright__ = "Philipp Kats"
__license__ = "fmit"
__all__ = ["execute"]

logger = logging.getLogger(__name__)


def execute(
    graph,
    weight: Optional[str] = "weight",
    max_communities: Optional[int] = None,
    modularity_resolution: int = 1,
    num_split_attempts: int = 0,
    fixed_split_step: int = 0,
    start_separate: bool = False,
    treat_as_modularity: bool = False,
    verbose: int = 0,
    intermediate_results_path: Optional[str] = None,
    return_modularity: bool = True,
    random_seed: Optional[int] = None,
) -> Union[Tuple[dict, float], dict]:
    """
    Partition graph into communities using Combo algorithm.
    All details are here: https://github.com/Casyfill/pyCOMBO

    Parameters
    ----------
    graph : NetworkX graph or path to the file (str)
        nx.Graph object, or string treated as path to Pajek .net file.
    weight : str, default 'weight'
        Graph edges property to use as weights. If None, graph assumed to be unweighted.
        Ignored if graph is passed as string (path to the file).
    max_communities : int, default None
        Maximum number of communities. If <= 0 or None, assume to be infinite.
    modularity_resolution : float, default 1.0
        Modularity resolution parameter.
    num_split_attempts : int, default 0
        Number of split attempts. If 0, autoadjust this number automatically.
    fixed_split_step : int, default 0
        Step number to apply predefined split. If 0, use only random splits,
        if >0 sets up the usage of 6 fixed type splits on every fixed_split_step.
    start_separate : bool, default False
        Indicates if Combo should start from assigning each node into its own separate community.
        This could help to achieve higher modularity, but it makes execution much slower.
    treat_as_modularity : bool, default False
        Indicates if edge weights should be treated as modularity scores.
        If True, the algorithm solves clique partitioning problem over the given graph,
        treated as modularity graph (matrix).
        For example, this allows users to provide their own custom 'modularity' matrix.
        `modularity_resolution` is ignored in this case.
    verbose : int, default 0
        Indicates how much progress information Combo should print out.
        For now Combo has only one level starting at verbose >= 1.
    intermediate_results_path : str, default None
        Path to the file where community assignments will be saved on each iteration.
        If None or empty, intermediate results will not be saved.
    return_modularity : bool, default True
        Indicates if function should return achieved modularity score.
    random_seed : int, default None
        Random seed to use.
        None indicates using some internal default value that is based on time
        and is expected to be different for each call.

    Returns
    -------
    partition : dict{int : int}
        Nodes to community labels correspondence.
    modularity : float
        Achieved modularity value. Only returned if return_modularity=True
    """
    if max_communities is not None and max_communities <= 0:
        max_communities = None

    if type(graph) is str:
        community_labels, modularity = comboCPP.execute_from_file(
            graph_path=graph,
            max_communities=max_communities,
            modularity_resolution=modularity_resolution,
            num_split_attempts=num_split_attempts,
            fixed_split_step=fixed_split_step,
            start_separate=start_separate,
            treat_as_modularity=treat_as_modularity,
            verbose=verbose,
            intermediate_results_path=intermediate_results_path,
            random_seed=random_seed,
        )

        partition = {i: community for i, community in enumerate(community_labels)}

    elif type(graph) is list or type(graph).__name__ == 'ndarray':
        community_labels, modularity = comboCPP.execute_from_matrix(
            matrix=graph,
            max_communities=max_communities,
            modularity_resolution=modularity_resolution,
            num_split_attempts=num_split_attempts,
            fixed_split_step=fixed_split_step,
            start_separate=start_separate,
            treat_as_modularity=treat_as_modularity,
            verbose=verbose,
            intermediate_results_path=intermediate_results_path,
            random_seed=random_seed,
        )

        partition = {i: community for i, community in enumerate(community_labels)}

    elif is_graph(graph):
        if len(graph) == 0:
            raise ValueError("Graph is empty")

        nodes, edges = deconstruct_graph(graph, weight=weight)

        community_labels, modularity = comboCPP.execute(
            size=graph.number_of_nodes(),
            edges=edges,
            directed=graph.is_directed(),
            max_communities=max_communities,
            modularity_resolution=modularity_resolution,
            num_split_attempts=num_split_attempts,
            fixed_split_step=fixed_split_step,
            start_separate=start_separate,
            treat_as_modularity=treat_as_modularity,
            verbose=verbose,
            intermediate_results_path=intermediate_results_path,
            random_seed=random_seed,
        )

        partition = {
            nodes[i]: community for i, community in enumerate(community_labels)
        }

    else:
        raise ValueError(f"Wrong graph representation: `{graph}`")

    logger.debug(f"Modularity for {graph.__repr__()}: {modularity:.5f}")

    if return_modularity:
        return partition, modularity

    return partition
