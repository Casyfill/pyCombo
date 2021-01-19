import pytest


def test_cCombo():
    from pycombo import combo

    assert combo.__doc__ == "combo partition Python binding"


def test_modularity_test_graph(test_graph):
    from pycombo.pyCombo import getComboPartition

    _, modularity_ = getComboPartition(test_graph, weight_prop="weight")
    assert modularity_ == pytest.approx(0.16, 0.0001)
    # assert modularity_ == pytest.approx(modularity(test_graph, partition, key='weight') )


def test_modularity_karate(karate):
    from pycombo.pyCombo import getComboPartition

    _, modularity_ = getComboPartition(karate)
    assert modularity_ == 0.437212
