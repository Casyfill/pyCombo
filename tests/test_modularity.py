import pytest


def test_cCombo():
    from pyCombo import combo

    assert combo.__doc__ == "combo partition Python binding"


def test_modularity_karate(karate):
    # import networkx as nx
    # karate = nx.karate_club_graph()

    from pyCombo.pyCombo import getComboPartition

    result = getComboPartition(karate, random_seed=42)
    assert result == pytest.approx(0.437212, 0.0001), result


def test_modularity_test_graph(test_graph):
    from pyCombo.pyCombo import getComboPartition

    result = getComboPartition(test_graph, weight_prop="weight", random_seed=42)
    # assert isinstance(result, tuple)
    modularity_ = result
    assert modularity_ == pytest.approx(0.16, 0.0001)
