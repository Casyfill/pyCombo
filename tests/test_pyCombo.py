#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

def _partitionGroup(p):
    '''
    get partition as label-dict
    this way we can check if two partitions are similar, despite
    different labels
    '''

    v = {}
    for key, value in sorted(p.items()):
        v.setdefault(value, []).append(key)
    return sorted(v.values())

def test_combo(test_graph):
    from pyCombo import combo

    partition = combo(test_graph, weight='weight')
    assert isinstance(partition, dict)
    assert _partitionGroup(partition) == _partitionGroup({0: 0, 1: 0, 2: 1, 3: 0, 4: 1})

    with pytest.raises(IOError):
        combo(42, weight='weight')



def test_modularity(test_graph):
    from pyCombo import combo, modularity
	
    partition = combo(test_graph, weight='weight')
    assert modularity(test_graph, partition, key='weight') == pytest.approx(0.08000000000000004, 0.00000001)

