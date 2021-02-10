#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest


def _partitionGroup(p):
    """
    get partition as label-dict
    this way we can check if two partitions are similar, despite
    different labels
    """

    v = {}
    for key, value in sorted(p.items()):
        v.setdefault(value, []).append(key)
    return sorted(v.values())


# @pytest.mark.parametrize("n", [3, 4, 5, 10])
# def test_fileojb_write_graph(n):
#     import tempfile
#     from pycombo.pyCombo import _fileojb_write_graph
#     import networkx as nx

#     test_graph = nx.complete_graph(n)
#     n_edges = (n * (n - 1)) / 2
#     n_lines = 2 + n + n_edges

#     with tempfile.NamedTemporaryFile("w") as tmp:
#         _ = _fileojb_write_graph(tmp, test_graph, weight=None)

#         with open(tmp.name, "r") as rtmp:
#             lines_list = list(rtmp.readlines())
#             assert len(lines_list) == n_lines, "".join(lines_list)


# def test_basic_combo(test_graph):
#     from pyCombo import combo

#     partition, modularity_ = combo(test_graph, weight_prop='weight')
#     assert isinstance(partition, dict)
#     assert _partitionGroup(partition) == _partitionGroup({0: 0, 1: 0, 2: 1, 3: 0, 4: 1})


def test_errors():
    from pycombo.pyCombo import get_combo_partition
    import networkx as nx

    graph = nx.Graph()  # empty
    with pytest.raises(ValueError):
        get_combo_partition(graph)

    # wrong value, number
    with pytest.raises(ValueError):
        get_combo_partition(42, weight_prop="weight")


# @pytest.mark.parametrize('full_graph_size', [2,3, 10, 100])
# def test_modularity_complete_graph(full_graph_size):
#     from pyCombo import combo
#     import networkx as nx

#     graph = nx.complete_graph(full_graph_size)
#     partition, modularity_ = combo(graph)

#     parts = {}
#     for node, part in partition.items():
#         if part not in parts:
#             parts[part] = {node, }
#         else:
#             parts[part].add(node)


#     assert len(parts.keys()) == 1, parts
#     # assert modularity_ == 1
