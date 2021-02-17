#!/usr/bin/env python
# -*- coding: utf-8 -*-
import networkx as nx
import pytest
from typing import Iterable


def _partitionGroup(p: dict) -> Iterable[list]:
    """
    get partition as label-dict

    returns dict of partition -> set of nodes
    this way we can check if two partitions are similar, despite
    different labels
    """

    v = dict()
    for key, value in sorted(p.items()):
        v.setdefault(value, []).append(key)
    return sorted(v.values())


def test_basic_combo(test_graph):
    import pycombo

    partition, modularity_ = pycombo.execute(test_graph)
    assert isinstance(partition, dict)
    assert _partitionGroup(partition) == _partitionGroup({0: 0, 1: 0, 2: 0, 3: 1, 4: 1})


@pytest.mark.parametrize("graph", [nx.Graph(), 42])
def test_errors(graph):
    from pycombo import execute

    with pytest.raises(ValueError):
        execute(graph)


def test_deconstruct_graph(karate):
    from pycombo.misc import deconstruct_graph

    nodes, edges = deconstruct_graph(karate)
    assert len(nodes) == len(karate)
    assert len(edges) == karate.size()


def test_weighted_graph():
    import networkx as nx
    lesmis = nx.les_miserables_graph()
    from pycombo import execute

    _, modularity = execute(lesmis, random_seed=42)
    assert modularity == pytest.approx(0.566688, 0.000001), modularity


def test_weighted_digraph(block_model):
    from pycombo import execute

    partition, modularity = execute(block_model, random_seed=42)
    assert modularity == pytest.approx(0.421296, 0.000001), modularity
    assert _partitionGroup(partition) == [list(range(5)), list(range(5, 5 + 8)), list(range(5 + 8, 5 + 18))]


def _get_modularity_matrix(graph, symmetrize=False):
    '''
    build modularity matrix and return as numpy array
    '''
    import numpy as np

    A = nx.to_numpy_array(graph)
    if not graph.is_directed():
        A += np.diag(np.diag(A))
    wout = A.sum(axis=1)
    win = A.sum(axis=0)
    T = wout.sum()
    Q = A / T - np.matmul(wout.reshape(-1, 1), win.reshape(1, -1)) / (T ** 2)
    if symmetrize:
        Q = (Q + Q.transpose()) / 2
    return Q


def test_mod_matrix(karate):
    from pycombo import execute

    partition_g, modularity_g = execute(karate, random_seed=42)
    mod_matrix = _get_modularity_matrix(karate)
    partition_m, modularity_m = execute(mod_matrix.tolist(), treat_as_modularity=True, random_seed=42)
    assert modularity_m == pytest.approx(modularity_g, 0.000001), (modularity_m, modularity_g)
    assert _partitionGroup(partition_g) == _partitionGroup(partition_m)


def test_mod_graph(karate):
    from pycombo import execute

    partition_g, modularity_g = execute(karate, random_seed=42)
    mod_graph = nx.from_numpy_array(_get_modularity_matrix(karate), create_using=nx.DiGraph)
    partition_m, modularity_m = execute(mod_graph, treat_as_modularity=True, random_seed=42)
    assert modularity_m == pytest.approx(modularity_g, 0.000001), (modularity_m, modularity_g)
    assert _partitionGroup(partition_g) == _partitionGroup(partition_m)


def test_clique_partitioning(test_cp_graph):
    import pycombo

    partition, modularity = pycombo.execute(test_cp_graph, treat_as_modularity=True)
    assert modularity == 1.1, modularity
    assert _partitionGroup(partition) == _partitionGroup({0: 0, 1: 0, 2: 1, 3: 2})
