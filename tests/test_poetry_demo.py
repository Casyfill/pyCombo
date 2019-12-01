from pathlib import Path

current_folder = Path(__file__).parent


def test_version():
    from pyCombo import __version__

    assert __version__ == "0.1.0"


# def test__run_combo():
#     from pyCombo import _run_combo

#     _run_combo(str(current_folder / "karate.net"))


# def test_toy_network():
#     from pyCombo import combo
#     import networkx as nx

#     n = nx.read_pajek(str(current_folder / "karate.net"))
#     result = combo(n)

