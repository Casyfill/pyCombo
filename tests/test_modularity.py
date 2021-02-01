import pytest


def test_cCombo():
    from pyCombo import combo

    assert combo.__doc__ == "combo partition Python binding"


def test_modularity_karate(karate):
    # import networkx as nx
    # karate = nx.karate_club_graph()

    from pyCombo.pyCombo import getComboPartition

    partition, modularity = getComboPartition(karate, random_seed=42)

    assert isinstance(partition, list)
    assert len(partition) == len(karate.nodes())

    assert modularity == pytest.approx(0.437212, 0.0001), modularity


def test_modularity_test_graph(test_graph):
    from pyCombo.pyCombo import getComboPartition

    partition, modularity = getComboPartition(
        test_graph, weight_prop="weight", random_seed=42
    )
    assert isinstance(partition, list)
    assert len(partition) == len(test_graph.nodes())
    assert modularity == pytest.approx(0.16, 0.0001)
