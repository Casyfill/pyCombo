#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Set, Tuple, Union, overload

import pycombo._combo as comboCPP
from pycombo.misc import deconstruct_graph, is_graph

__author__ = "Philipp Kats"
__copyright__ = "Philipp Kats"
__license__ = "GPL-3.0-or-later"
__all__ = ["execute"]

logger = logging.getLogger(__name__)

Partition = Dict[Any, int]
ExecuteResult = Union[Partition, Tuple[Partition, float], Any]


def _is_ndarray(graph: Any) -> bool:
    return type(graph).__module__ == "numpy" and type(graph).__name__ == "ndarray"


def _partition_to_communities(partition: Partition) -> List[Set[Any]]:
    communities: Dict[int, Set[Any]] = {}
    for node, community in partition.items():
        communities.setdefault(community, set()).add(node)
    return list(communities.values())


def _write_partition_to_graph(
    graph: Any, partition: Partition, attribute: str
) -> None:
    for node, community in partition.items():
        graph.nodes[node][attribute] = community


def _to_node_clustering(graph: Any, partition: Partition) -> Any:
    from cdlib.classes import NodeClustering

    return NodeClustering(
        communities=_partition_to_communities(partition),
        graph=graph,
        method_name="combo",
    )


@overload
def execute(
    graph: Any,
    weight: Optional[str] = "weight",
    max_communities: Optional[int] = None,
    modularity_resolution: float = 1.0,
    num_split_attempts: int = 0,
    fixed_split_step: int = 0,
    start_separate: bool = False,
    treat_as_modularity: bool = False,
    verbose: int = 0,
    intermediate_results_path: Optional[str] = None,
    *,
    return_modularity: bool = True,
    random_seed: Optional[int] = None,
    community_attribute: Optional[str] = None,
    as_clustering: bool = False,
) -> Tuple[Partition, float]: ...


@overload
def execute(
    graph: Any,
    weight: Optional[str] = "weight",
    max_communities: Optional[int] = None,
    modularity_resolution: float = 1.0,
    num_split_attempts: int = 0,
    fixed_split_step: int = 0,
    start_separate: bool = False,
    treat_as_modularity: bool = False,
    verbose: int = 0,
    intermediate_results_path: Optional[str] = None,
    *,
    return_modularity: bool = False,
    random_seed: Optional[int] = None,
    community_attribute: Optional[str] = None,
    as_clustering: bool = False,
) -> Partition: ...


def execute(
    graph,
    weight: Optional[str] = "weight",
    max_communities: Optional[int] = None,
    modularity_resolution: float = 1.0,
    num_split_attempts: int = 0,
    fixed_split_step: int = 0,
    start_separate: bool = False,
    treat_as_modularity: bool = False,
    verbose: int = 0,
    intermediate_results_path: Optional[str] = None,
    return_modularity: bool = True,
    random_seed: Optional[int] = None,
    community_attribute: Optional[str] = None,
    as_clustering: bool = False,
) -> ExecuteResult:
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
        For now, Combo has only one level starting at verbose >= 1.
    intermediate_results_path : str, default None
        Path to the file where community assignments will be saved on each iteration.
        If None or empty, intermediate results will not be saved.
    return_modularity : bool, default True
        Indicates if function should return achieved modularity score.
    random_seed : int, default None
        Random seed to use.
        None indicates using some internal default value that is based on time
        and is expected to be different for each call.
    community_attribute : str, optional
        When partitioning a NetworkX graph, write community labels to
        ``graph.nodes[node][community_attribute]``.
    as_clustering : bool, default False
        When True, return a ``cdlib.classes.NodeClustering`` instead of a dict.
        Requires cdlib to be installed.

    Returns
    -------
    partition : dict{int : int}
        Nodes to community labels correspondence.
    modularity : float
        Achieved modularity value. Only returned if return_modularity=True
    """
    if max_communities is not None and max_communities <= 0:
        max_communities = None

    params = {
        "max_communities": max_communities,
        "modularity_resolution": modularity_resolution,
        "num_split_attempts": num_split_attempts,
        "fixed_split_step": fixed_split_step,
        "start_separate": start_separate,
        "treat_as_modularity": treat_as_modularity,
        "verbose": verbose,
        "intermediate_results_path": intermediate_results_path,
        "random_seed": random_seed,
    }

    nx_graph = graph if is_graph(graph) else None

    if isinstance(graph, str):
        community_labels, modularity = comboCPP.execute_from_file(
            graph_path=graph,
            **params,
        )
        partition = {i: community for i, community in enumerate(community_labels)}

    elif isinstance(graph, list) or _is_ndarray(graph):
        community_labels, modularity = comboCPP.execute_from_matrix(
            matrix=graph,
            **params,
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
            **params,
        )

        partition = {
            nodes[i]: community for i, community in enumerate(community_labels)
        }

    else:
        raise ValueError(f"Wrong graph representation: `{graph}`")

    logger.debug(f"Modularity for {graph!r}: {modularity:.5f}")

    if community_attribute is not None:
        if nx_graph is None:
            raise ValueError(
                "community_attribute is only supported for NetworkX graph inputs"
            )
        _write_partition_to_graph(nx_graph, partition, community_attribute)

    if as_clustering:
        if nx_graph is None:
            raise ValueError("as_clustering is only supported for NetworkX graph inputs")
        clustering = _to_node_clustering(nx_graph, partition)
        if return_modularity:
            return clustering, modularity
        return clustering

    if return_modularity:
        return partition, modularity

    return partition
