#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, absolute_import

# import subprocess
# import os
import logging
import tempfile
from pathlib import Path
from typing import Optional
import math
import pyCombo.combo as ccombo

__author__ = "Philipp Kats"
__copyright__ = "Philipp Kats"
__license__ = "fmit"

__all__ = ["getComboPartition", "modularity"]
logger = logging.getLogger(__name__)


def _check_repr(G):
    if type(G).__name__ not in {"Graph", "MultiDiGraph"}:
        raise ValueError(
            f"require networkx graph as first parameter, got `{type(G).__name__}`"
        )

    if len(G) == 0:
        raise ValueError("Graph is empty")


def _fileojb_write_graph(f, G, weight=None) -> dict:

    nodenum, nodes = {}, {}

    f.write(f"*Vertices {len(G.nodes())}\n")
    for i, n in enumerate(G.nodes()):
        f.write(f'{i} "{n}"\n')
        nodenum[n] = i
        nodes[i] = n

    f.write("*Arcs\n")

    for e in G.edges(data=True):
        if weight is not None:
            f.write(f"{nodenum[e[0]]} {nodenum[e[1]]} {nodenum[e[2][weight]]}\n")
        else:
            f.write(f"{nodenum[e[0]]} {nodenum[e[1]]} 1\n")
    f.flush()

    cnt = 1 + len(G.edges())
    logger.debug(f"Wrote Graph to `{f.name}` ({cnt} lines)")
    return nodes


def getComboPartition(
    G, max_communities:int=-1,
    mod_resolution: int = 1,
    weight_prop: Optional[str] = None,
    use_fix_tries:bool = False,
    random_seed:int = 42
):
    """
    calculates Combo Partition using Combo C++ script
    all details here: https://github.com/Casyfill/pyCOMBO

    G - NetworkX graph
    max_communities - maximum number of partitions. If none, assume to be infinite
    mod_resolution
    weight_prop - graph edges property to use as weights. If None, graph assumed to be unweighted
    use_fix_tries: bool
    random_seedd:int Random seed to use

    #### NOTE: code generates temporary partitioning file
    """

    _check_repr(G)
    directory = Path(__name__).parent.absolute()

    with tempfile.TemporaryDirectory(dir=directory) as tmpdir:
        with open(f"{tmpdir}/temp_graph.net", "w") as f:
            nodes = _fileojb_write_graph(f, G, weight=weight_prop)

        # RUN COMBO
        # commands = [
        #     str(directory / "combo" / "comboCPP"),
        #     f.name,
        #     max_number_of_communities,
        #     str(mod_resolution),
        #     "temp_partition",  # file_suffix
        # ]

        # logger.info(f'Executing command: `{" ".join(commands)}`')
        # out = subprocess.Popen(
        #     commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        # )
        result = ccombo.execute(
            graph_path=f.name,
            max_communities=max_communities,
            mod_resolution=mod_resolution,
            use_fix_tries=use_fix_tries,
            random_seed=random_seed
        )

        logger.info(f"Result: {result}")
        stdout, stderr = result
        # stdout, stderr = out.communicate()
        logger.debug(f"STDOUT: {stdout}")
        if stderr is not None:
            raise Exception(f"STDERR: {stderr}")  # TODO: setup c++ to throw stderr

        try:
            modularity_ = float(stdout)
        except Exception as e:
            raise Exception(stdout, e)

        # READ RESULTING PARTITON
        with open(f"{tmpdir}/temp_graph_temp_partition.txt", "r") as f:
            partition = {nodes[i]: int(line) for i, line in enumerate(f)}
            return partition, modularity_


def modularity(G, partition, key: Optional[str] = None):
    """
    compute network modularity
    for the given partitioning

    G:              networkx graph
    partition:      any partition
    key:            weight attribute

    """
    _check_repr(G)
    assert len(G.nodes()) == len(
        partition.keys()
    ), f"Graph got {len(G.nodes())} nodes, partition got {len(partition.keys())}"
    weighted = key is not None
    nodes = G.nodes()
    # compute node weights
    if G.is_directed():
        w1 = G.out_degree(weight=key)
        w2 = G.in_degree(weight=key)
    else:
        w1 = w2 = G.degree(weight=key)

    # compute total network weight
    if weighted:
        T = 2.0 * sum([edge[2][key] for edge in G.edges(data=True)])
    else:
        T = 2.0 * len(G.edges())

    M = 0  # start accumulating modularity score
    for a in nodes:
        for b in nodes:

            try:
                if partition[a] == partition[b]:  # if belong to the same community
                    # get edge weight
                    if G.has_edge(a, b):
                        if weighted:
                            e = G[a][b][key]
                        else:
                            e = 1
                    else:
                        e = 0
                    # add modularity score for the considered edge
                    M += e / T - w1[a] * w2[b] / (T ** 2)
            except KeyError:
                raise KeyError(a, b, partition, nodes)
    return M
