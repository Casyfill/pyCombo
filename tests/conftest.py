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
def karate() -> nx.Graph:
    import networkx as nx

    return nx.karate_club_graph()


@pytest.fixture(scope="session")
def relaxed_caveman() -> nx.Graph:
    import networkx as nx

    return nx.relaxed_caveman_graph(100, 10, p=0.1, seed=42)
