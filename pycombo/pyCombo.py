#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
from typing import Optional, Union, Tuple
import pycombo._combo as comboCPP

__author__ = "Philipp Kats"
__copyright__ = "Philipp Kats"
__license__ = "fmit"
__all__ = ["get_combo_partition"]

logger = logging.getLogger(__name__)


def _check_repr(graph):
    if type(graph).__name__ not in {"Graph", "DiGraph", "MultiGraph", "MultiDiGraph"}:
        raise ValueError(
            f"require networkx graph as first parameter, got `{type(graph).__name__}`"
        )

    if len(graph) == 0:
        raise ValueError("Graph is empty")


def get_combo_partition(
    graph,
    weight_prop: Optional[str] = 'weight',
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
    weight_prop : str, default 'weight'
        Graph edges property to use as weights. If None, graph assumed to be unweighted.
        Unused if graph is string.
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
        partition = {}
        for i, community in enumerate(community_labels):
            partition[i] = community
    else:
        _check_repr(graph)
        nodenum, nodes = {}, {}
        for i, n in enumerate(graph.nodes()):
            nodenum[n] = i
            nodes[i] = n
        edges = []
        for edge in graph.edges(data=True):
            if weight_prop is not None:
                edges.append(
                    (nodenum[edge[0]], nodenum[edge[1]], edge[2].get(weight_prop, 1))
                )
            else:
                edges.append((nodenum[edge[0]], nodenum[edge[1]], 1.0))
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
        partition = {}
        for i, community in enumerate(community_labels):
            partition[nodes[i]] = community
    logger.debug(f"Result: {partition}, {modularity}")
    # TODO: setup c++ to throw stderr

    return partition, modularity
