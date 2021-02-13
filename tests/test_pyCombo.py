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
