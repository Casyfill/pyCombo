import networkx as nx
from pathlib import Path
import pytest

current_path = Path(__file__).parent


@pytest.fixture(scope="class")
def karate():
    path = current_path / "data" / "karate.net"
    return nx.read_pajek(str(path))


class Test_Graph:
    def test_graph_nx(self, karate):
        from pyCombo import Graph

        g = Graph(karate)
        assert g.m_isOriented == True

        l = len(karate.nodes())
        assert g.m_size == l
        assert g.m_matrix.shape == (l, l)

    def test_graph_matrix(self, karate):
        from copy import deepcopy
        from pyCombo import Graph

        k = nx.relabel.convert_node_labels_to_integers(karate)

        # there is one more edge like this, hense total weight=100
        attr = {(1, 0, 0): 99}
        nx.set_edge_attributes(k, attr, name="weight")

        g = Graph(k)

        assert g.m_matrix[1, 0] == 100

