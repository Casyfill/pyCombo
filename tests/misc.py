#!/usr/bin/env python
#-*- coding: utf-8 -*-
import networkx as nx


def partitionGroup(p):
    '''
    get partition as label-dict
    this way we can check if two partitions are similar, despite
    different labels
    '''

    v = {}
    for key, value in sorted(p.iteritems()):
        v.setdefault(value, []).append(key)
    return sorted(v.values())


def get_test_graph():
    '''test graph with known partition'''
    G = nx.Graph()
    G.add_nodes_from(range(5))
    G.add_edges_from([(0, 1), (1, 2), (1, 3), (2, 4), (3, 4)])
    nx.set_edge_attributes(G, 'weight', [1] * G.number_of_edges())
    return G
