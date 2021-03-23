#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for pycombo.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""
from __future__ import print_function, absolute_import, division

import pytest
import networkx as nx
from pathlib import Path

test_dir = Path(__file__).parent


@pytest.fixture(scope="function")
def test_graph():
    """test graph with known partition"""
    G = nx.Graph()
    G.add_nodes_from(range(5))
    G.add_edges_from([(0, 1), (1, 2), (2, 0), (3, 4)])
    nx.set_edge_attributes(G, 1, "weight")
    return G


@pytest.fixture(scope="function")
def test_cp_graph():
    """test graph with known clique partition"""
    G = nx.Graph()
    G.add_nodes_from(range(4))
    G.add_edges_from([(0, 1, {'weight': 1.1}), (0, 2, {'weight': 1}), (0, 3, {'weight': 1}),
                      (1, 2, {'weight': -1.1}), (1, 3, {'weight': -1.1}), (3, 2, {'weight': -1.1})])
    return G


@pytest.fixture(scope="function")
def test_start_sep_graph():
    """test graph with known clique partition that needs start_separate"""
    G = nx.Graph()
    G.add_nodes_from(range(6))
    G.add_edges_from([(0, 1, {'weight': 1.0}), (0, 2, {'weight': -10}), (0, 3, {'weight': 1}), (0, 4, {'weight': -10}), (0, 5, {'weight': -10}),
                      (1, 2, {'weight': 1.2}), (1, 3, {'weight': -10}), (1, 4, {'weight': -10}), (1, 5, {'weight': -10}),
                      (2, 3, {'weight': 1}), (2, 4, {'weight': -1}), (2, 5, {'weight': 0.5}),
                      (3, 4, {'weight': 0.5}), (3, 5, {'weight': -1})])
    return G


@pytest.fixture(scope="function")
def karate() -> nx.Graph:
    import networkx as nx

    return nx.karate_club_graph()


@pytest.fixture(scope="session")
def relaxed_caveman() -> nx.Graph:
    import networkx as nx

    return nx.relaxed_caveman_graph(100, 10, p=0.1, seed=42)


@pytest.fixture(scope="session")
def block_model() -> nx.DiGraph:
    import networkx as nx

    sizes = [5, 8, 10]
    probs = [[0.7 , 0.1, 0.05],
             [0.05, 0.6, 0.05],
             [0.02, 0.2, 0.5]]
    return nx.stochastic_block_model(sizes, probs, seed=42, directed=True, selfloops=True)
