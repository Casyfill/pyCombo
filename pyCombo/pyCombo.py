#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import division, absolute_import

import os
import logging
import tempfile
from pathlib import Path

__author__ = "Philipp Kats"
__copyright__ = "Philipp Kats"
__license__ = "mit"

logger = logging.getLogger(__name__)


def _check_repr(G):
    if type(G).__name__ != 'Graph':
        raise IOError(f'require networkx graph as first parameter:`{type(G).__name__}`')

def getComboPartition(G, maxcom=None, weight=None):
    '''
    calculates Combo Partition using Combo C++ script
    all details here: https://github.com/Casyfill/pyCOMBO

    G - NetworkX graph
    maxcom - maximum number of partitions, by defeult infinite
    weight - graph esges weight

    # TODO: add functionality for unweighted graph
    # NOTE: code generates temporary partitioning file
    '''
<<<<<<< HEAD
    name = type(G).__name__
    if name != "Graph":
        raise IOError(f'require networkx graph as first parameter, got {name}')
=======
    _check_repr(G)
>>>>>>> refactoring code with tempfile

    nodenum, nodes = {}, {}

    # inventorisation
    for i, n in enumerate(G.nodes()):
        nodenum[n] = i
        nodes[i] = n
    
    f = tempfile.NamedTemporaryFile('w')
    f.write('*Arcs\n')
    for e in G.edges(data=True):
        if weight:
            f.write('{0} {1} {2}\n'.format(nodenum[e[0]],
                                           nodenum[e[1]], e[2][weight]))
        else:
            f.write('{0} {1} {2}\n'.format(nodenum[e[0]],
                                           nodenum[e[1]], 1))
    f.flush()

    # RUN COMBO
    directory = Path(__name__).parent.absolute()
    path_to_binary = str(directory / "pyCombo/comboCPP")
    command = '{path_to_binary} {f.name}'

    if maxcom is not None:
         command = f'{command} {maxcom}'
    logger.info(f'Executing command: `{command}`')
    os.system(command)

    # READ RESULTING PARTITON
    with (directory / 'pyCombo/temp_comm_comboC++.txt').open('r') as f:
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
<<<<<<< HEAD
    name = type(G).__name__
    if  name != "Graph":
        raise IOError(f'require networkx graph as first parameter, got {name}')
=======
    _check_repr(G)
>>>>>>> refactoring code with tempfile

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
