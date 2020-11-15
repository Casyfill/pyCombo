#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import division, absolute_import

import os
import logging
# import networkx as nx

__author__ = "Philipp Kats"
__copyright__ = "Philipp Kats"
__license__ = "mit"

_logger = logging.getLogger(__name__)
PWD = os.getenv('PWD')


def getComboPartition(G, maxcom=None, weight=None):
    '''
    calculates Combo Partition using Combo C++ script
    all details here: https://github.com/Casyfill/pyCOMBO

    G - NetworkX graph
    maxcom - maximum number of partitions, by defeult infinite
    weight - graph esges weight

    # TODO: add functionality for unweighted graph
    # TODO: add exception thrower
    # NOTE: code generates temporary partitioning file
    '''
    name = type(G).__name__
    if name != "Graph":
        raise IOError(f'require networkx graph as first parameter, got {name}')

    nodenum = {}
    nodes = {}

    # inventorisation
    for i, n in enumerate(G.nodes()):
        nodenum[n] = i
        nodes[i] = n

    # pass edges
    path = PWD + '/pyCombo/temp.net'

    with open(path, 'w') as f:
        f.write('*Arcs\n')
        for e in G.edges(data=True):
            if weight:
                f.write('{0} {1} {2}\n'.format(nodenum[e[0]],
                                               nodenum[e[1]], e[2][weight]))
            else:
                f.write('{0} {1} {2}\n'.format(nodenum[e[0]],
                                               nodenum[e[1]], 1))

    # RUN COMBO
    command = '{0}/pyCombo/comboCPP '.format(PWD) + path

    if maxcom:
        command += ' {0}'.format(maxcom)  # uses inf or selected max partition

    os.system(command)  # execute bash command

    # READ RESULTING PARTITON
    with open(PWD + '/pyCombo/temp_comm_comboC++.txt', 'r') as f:
        partition = {}

        for i, line in enumerate(f):
            partition[nodes[i]] = int(line)

    return partition


def modularity(G:"nx.classes.graph.Graph", partition, key='weight'):
    '''
    compute network modularity
    for the given partitioning

    G:              networkx graph
    partition:      any partition
    key:            weight attribute

    '''
    name = type(G).__name__
    if  name != "Graph":
        raise IOError(f'require networkx graph as first parameter, got {name}')

    nodes = G.nodes()
    # compute node weights
    if G.is_directed():
        w1 = G.out_degree(weight=key)
        w2 = G.in_degree(weight=key)
    else:
        w1 = w2 = G.degree(weight=key)

    # compute total network weight
    T = 2.0 * sum([e[2][key] for e in G.edges(data=True)])

    M = 0  # start accumulating modularity score
    for a in nodes:
        for b in nodes:

            if partition[a] == partition[b]:  # if belong to the same community
                # get edge weight
                if G.has_edge(a, b):
                    e = G[a][b][key]
                else:
                    e = 0
                # add modularity score for the considered edge
                M += e / T - w1[a] * w2[b] / (T**2)
    return M
