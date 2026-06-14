import pytest


def test_c_import():
    import pycombo

    assert (
        pycombo._combo.__doc__
        == "Python binding for Combo community detection algorithm"
    )


def _comm_groups(partition: dict) -> list:
    """convert partition node->comm into list of sets of nodes, one set per community"""
    result = dict()
    for k, v in partition.items():
        result[v] = result.get(v, list()) + [k]
    return [set(el) for el in result.values()]


def test_modularity_karate(karate, benchmark):
    import networkx.algorithms.community as nx_comm
    from pycombo import execute

    partition, modularity = benchmark(execute, karate, random_seed=42)

    assert isinstance(partition, dict)
    assert len(partition) == len(karate)
    comms = _comm_groups(partition)
    networkx_modularity = nx_comm.modularity(karate, comms)

    assert modularity == pytest.approx(networkx_modularity, 0.0001), (
        modularity,
        networkx_modularity,
    )


def test_relaxed_caveman(relaxed_caveman, benchmark):
    import networkx.algorithms.community as nx_comm
    from pycombo import execute

    partition, modularity = benchmark(execute, relaxed_caveman, random_seed=42)

    assert isinstance(partition, dict)
    assert len(partition) == len(relaxed_caveman)

    comms = _comm_groups(partition)
    networkx_modularity = nx_comm.modularity(relaxed_caveman, comms)

    assert modularity == pytest.approx(networkx_modularity, 0.0001), (
        modularity,
        networkx_modularity,
    )


def test_combo_modularity_vs_leidenalg(karate):
    from cdlib import algorithms
    import networkx.algorithms.community as nx_comm
    from pycombo import execute

    combo_partition, combo_modularity = execute(karate, random_seed=42)
    leiden_clustering = algorithms.leiden(karate)
    leiden_modularity = nx_comm.modularity(karate, leiden_clustering.communities)

    assert combo_modularity == pytest.approx(
        nx_comm.modularity(karate, _comm_groups(combo_partition)), abs=1e-4
    )
    assert combo_modularity >= leiden_modularity - 1e-4
