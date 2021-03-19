#!/usr/bin/env python
# -*- coding: utf-8 -*-
import networkx as nx
import pytest
import os
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


def test_execute_from_file(karate):
    import pycombo

    path = "./karate.net"
    nx.write_pajek(karate, path)
    partition, modularity = pycombo.execute(path)
    assert modularity == pytest.approx(0.41979, 0.000001), modularity
    assert _partitionGroup(partition) == _partitionGroup({0: 2, 1: 2, 2: 2, 3: 2, 4: 0, 5: 0, 6: 0, 7: 2, 8: 1, 9: 1,
                                                          10: 0, 11: 2, 12: 2, 13: 2, 14: 1, 15: 1, 16: 0, 17: 2, 18: 1, 19: 2,
                                                          20: 1, 21: 2, 22: 1, 23: 3, 24: 3, 25: 3, 26: 1, 27: 3, 28: 3, 29: 1,
                                                          30: 1, 31: 3, 32: 1, 33: 1})
    os.remove(path)


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


def test_mod_matrix_as_list(karate):
    from pycombo import execute

    partition_g, modularity_g = execute(karate, random_seed=42)
    mod_matrix = _get_modularity_matrix(karate)
    partition_m, modularity_m = execute(mod_matrix.tolist(), treat_as_modularity=True, random_seed=42)
    assert modularity_m == pytest.approx(modularity_g, 0.000001), (modularity_m, modularity_g)
    assert _partitionGroup(partition_g) == _partitionGroup(partition_m)


def test_mod_matrix_as_numpy(karate):
    from pycombo import execute

    partition_g, modularity_g = execute(karate, random_seed=42)
    mod_matrix = _get_modularity_matrix(karate)
    partition_m, modularity_m = execute(mod_matrix, treat_as_modularity=True, random_seed=42)
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


def test_max_communities(karate):
    import pycombo

    partition_None, modularity_None = pycombo.execute(karate)
    partition_0, modularity_0 = pycombo.execute(karate, max_communities=0)
    assert modularity_None == pytest.approx(modularity_0, 0.000001), (modularity_None, modularity_0)
    assert _partitionGroup(partition_None) == _partitionGroup(partition_0)
    partition_minus1, modularity_minus1 = pycombo.execute(karate, max_communities=-1)
    assert modularity_None == pytest.approx(modularity_minus1, 0.000001), (modularity_None, modularity_minus1)
    assert _partitionGroup(partition_None) == _partitionGroup(partition_minus1)
    partition_minus10, modularity_minus10 = pycombo.execute(karate, max_communities=-10)
    assert modularity_None == pytest.approx(modularity_minus10, 0.000001), (modularity_None, modularity_minus10)
    assert _partitionGroup(partition_None) == _partitionGroup(partition_minus10)
    partition_1, modularity_1 = pycombo.execute(karate, max_communities=1)
    assert modularity_1 == pytest.approx(0, 0.000001), modularity_1
    assert _partitionGroup(partition_1) == [list(range(len(karate)))]
    partition_2, modularity_2 = pycombo.execute(karate, max_communities=2)
    assert modularity_2 == pytest.approx(0.371795, 0.000001), modularity_2
    assert _partitionGroup(partition_2) == [list(range(8)) + list(range(9, 14)) + [16, 17, 19, 21],
                                            [8, 14, 15, 18, 20] + list(range(22, 34))]
    partition_3, modularity_3 = pycombo.execute(karate, max_communities=3)
    assert modularity_3 == pytest.approx(0.402038, 0.000001), modularity_3
    assert _partitionGroup(partition_3) == [list(range(4)) + [7, 9, 11, 12, 13, 17, 19, 21],
                                            [4, 5, 6, 10, 16],
                                            [8, 14, 15, 18, 20] + list(range(22, 34))]
