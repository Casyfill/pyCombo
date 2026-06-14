from typing import Optional, Tuple, Dict, List
import logging

logger = logging.getLogger(__name__)

nodes_ = Dict[int, int]
edges_ = List[Tuple[int, int, float]]


def is_graph(graph) -> bool:
    graph_names = {"Graph", "DiGraph", "MultiGraph", "MultiDiGraph"}
    return type(graph).__name__ in graph_names


def is_weighted(G, edge: Optional[tuple] = None, weight: str = "weight") -> bool:
    """Returns True if `G` has weighted edges.

    NOTE: ventorized from networkx:
    https://networkx.org/documentation/stable/_modules/networkx/classes/function.html#is_weighted

    Parameters
    ----------
    G : graph
        A NetworkX graph.

    edge : tuple, optional
        A 2-tuple specifying the only edge in `G` that will be tested. If
        None, then every edge in `G` is tested.

    weight: string, optional
        The attribute name used to query for edge weights.

    Returns
    -------
    bool
        A boolean signifying if `G`, or the specified edge, is weighted.

    Raises
    ------
    NetworkXError
        If the specified edge does not exist.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> nx.is_weighted(G)
    False
    >>> nx.is_weighted(G, (2, 3))
    False

    >>> G = nx.DiGraph()
    >>> G.add_edge(1, 2, weight=1)
    >>> nx.is_weighted(G)
    True

    """
    if edge is not None:
        data = G.get_edge_data(*edge)
        if data is None:
            raise ValueError(f"Edge {edge!r} does not exist.")
        return weight in data

    if not any(G.adj.values()):  # nx.is_empty()
        # Special handling required since: all([]) == True
        return False

    return all(weight in data for u, v, data in G.edges(data=True))


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
    weight_key = weight if weight is not None else "weight"
    for edge in graph.edges(data=True):
        if weight is None:
            edge_weight = default_weight
        else:
            edge_weight = edge[2].get(weight_key, default_weight)
        edges.append((nodenum[edge[0]], nodenum[edge[1]], edge_weight))
    return nodes, edges
