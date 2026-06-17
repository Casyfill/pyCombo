# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Optional, Tuple, Dict, List
import logging

logger = logging.getLogger(__name__)

nodes_ = Dict[int, int]
edges_ = List[Tuple[int, int, float]]


def is_graph(graph) -> bool:
    """Tests if the input is a NetworkX graph.
    Avoids having to import NetworkX just to check the type.
    """
    return hasattr(graph, "nodes") and hasattr(graph, "edges") and hasattr(graph, "adj")


def _has_weight_attribute(graph, weight: str) -> bool:
    return any(weight in data for u, v, data in graph.edges(data=True))


def _default_edge_weight(graph, weight: Optional[str]) -> float:
    """Return the fallback edge weight for edges missing the weight attribute.

    Unweighted graphs use 1.0 (standard modularity convention).
    Weighted graphs use 0.0 for edges that lack the weight attribute.
    """
    if weight is None:
        return 1.0
    if _has_weight_attribute(graph, weight):
        return 0.0
    logger.info(f"No property found: `{weight}`. Using as unweighted graph")
    return 1.0


def deconstruct_graph(graph, weight: Optional[str] = None) -> Tuple[nodes_, edges_]:
    """deconstructs networkx.Graph

    deconstructs networkx.Graph into
    dictionary of nodes (index, name)
    and na array of edge tuples (from, to, weight)
    """
    default_weight = _default_edge_weight(graph, weight)

    nodenum, nodes = dict(), dict()
    for i, n in enumerate(graph.nodes()):
        nodenum[n] = i
        nodes[i] = n

    edges = []
    for edge in graph.edges(data=True):
        if weight is None:
            edge_weight = default_weight
        else:
            edge_weight = edge[2].get(weight, default_weight)
        edges.append((nodenum[edge[0]], nodenum[edge[1]], edge_weight))
    return nodes, edges
