#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
from typing import Optional, Union, Tuple
import pycombo._combo as comboCPP
from pycombo.misc import _check_repr, deconstruct_graph

__author__ = "Philipp Kats"
__copyright__ = "Philipp Kats"
__license__ = "fmit"
__all__ = ["execute"]

logger = logging.getLogger(__name__)


def execute(
    graph,
    weight: Optional[str] = None,
    max_communities: int = -1,
    modularity_resolution: int = 1,
    num_split_attempts: int = 0,
    fixed_split_step: int = 0,
    return_modularity: bool = True,
    random_seed: int = -1,
) -> Union[Tuple[dict, float], dict]:
    """
    Partition graph into communities using Combo algorithm.
    All details are here: https://github.com/Casyfill/pyCOMBO

    Parameters
    ----------
    graph : NetworkX graph or str
        String treated as path to Pajek .net file with graph.
    weight : str, default None
        Graph edges property to use as weights. If None, graph assumed to be unweighted.
        Unused if graph is string (path to the file).
    max_communities : int, default -1
        Maximum number of communities. If -1, assume to be infinite.
    modularity_resolution : float, default 1.0
        Modularity resolution parameter.
    num_split_attempts : int, default 0
        Number of split attempts. If 0, autoadjust this number automatically.
    fixed_split_step : int, default 0
        Step number to apply predifined split. If 0, use only random splits,
        if >0 sets up the usage of 6 fixed type splits on every fixed_split_step.
    random_seedd : int, default 0
        Random seed to use.

    Returns
    -------
    partition : dict{int : int}
        Nodes to community labels correspondance.
    modularity : float
        Achieved modularity value.
    """
    if type(graph) is str:
        community_labels, modularity = comboCPP.execute_from_file(
            graph_path=graph,
            max_communities=max_communities,
            modularity_resolution=modularity_resolution,
            num_split_attempts=num_split_attempts,
            fixed_split_step=fixed_split_step,
            random_seed=random_seed,
        )

        partition = dict()
        for i, community in enumerate(community_labels):
            partition[i] = community
    else:
        _check_repr(graph)
        nodes, edges = deconstruct_graph(graph, weight=weight)
        logger.debug(edges)
        community_labels, modularity = comboCPP.execute(
            size=graph.number_of_nodes(),
            edges=edges,
            directed=graph.is_directed(),
            max_communities=max_communities,
            modularity_resolution=modularity_resolution,
            num_split_attempts=num_split_attempts,
            fixed_split_step=fixed_split_step,
            random_seed=random_seed,
        )

        partition = dict()
        for i, community in enumerate(community_labels):
            partition[nodes[i]] = community

    logger.debug(f"Modularity for {graph.__repr__()}: {modularity:.5f}")

    if return_modularity:
        return partition, modularity

    return partition
