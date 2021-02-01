import pytest


def test_cCombo():
    from pyCombo import combo

    assert combo.__doc__ == "combo partition Python binding"


def test_modularity_karate(karate, benchmark):
    # import networkx as nx
    # karate = nx.karate_club_graph()

    from pyCombo.pyCombo import getComboPartition

    partition, modularity = benchmark(getComboPartition, karate, random_seed=42)

    assert isinstance(partition, list)
    assert len(partition) == len(karate)

    assert modularity == pytest.approx(0.437212, 0.0001), modularity


def test_relaxed_caveman(relaxed_caveman, benchmark):

    from pyCombo.pyCombo import getComboPartition

    partition, modularity = benchmark(
        getComboPartition, relaxed_caveman, weight_prop="weight", random_seed=42
    )
    print(modularity)
    assert isinstance(partition, list)
    assert len(partition) == len(relaxed_caveman)


def test_modularity_test_graph(test_graph, benchmark):
    from pyCombo.pyCombo import getComboPartition

    partition, modularity = benchmark(
        getComboPartition, test_graph, weight_prop="weight", random_seed=42
    )

    assert isinstance(partition, list)
    assert len(partition) == len(test_graph)
    assert modularity == pytest.approx(0.16, 0.0001)
