import pytest


def test_cCombo():
    from pycombo.pyCombo import comboCPP

    assert comboCPP.__doc__ == "Python binding for Combo community detection algorithm"


def _comm_groups(partition: dict) -> list:
    """convert partition node->comm
    into list of sets of nodes, one set per community
    """
    result = dict()
    for k, v in partition.items():
        result[v] = result.get(v, list()) + [k]
    return [set(el) for el in result.values()]


def test_modularity_karate(karate, benchmark):
    # import networkx as nx
    # karate = nx.karate_club_graph()
    import networkx.algorithms.community as nx_comm

    from pycombo.pyCombo import get_combo_partition

    partition, modularity = benchmark(get_combo_partition, karate, random_seed=42)

    assert isinstance(partition, dict)
    assert len(partition) == len(karate)
    comms = _comm_groups(partition)
    networkx_modularity = nx_comm.modularity(karate, comms)

    assert modularity == pytest.approx(networkx_modularity, 0.0001), (
        modularity,
        networkx_modularity,
    )


def test_relaxed_caveman(relaxed_caveman, benchmark):

    from pycombo.pyCombo import get_combo_partition

    partition, modularity = benchmark(
        get_combo_partition, relaxed_caveman, weight_prop="weight", random_seed=42
    )

    assert isinstance(partition, dict)
    assert len(partition) == len(relaxed_caveman)


# def test_modularity_test_graph(test_graph, benchmark):
#     from pyCombo.pyCombo import get_combo_partition

#     partition, modularity = benchmark(
#         get_combo_partition, test_graph, weight_prop="weight", random_seed=42
#     )

#     assert isinstance(partition, list)
#     assert len(partition) == len(test_graph)
#     assert modularity == pytest.approx(0.16, 0.0001)
