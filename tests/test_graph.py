import networkx as nx
import numpy as np
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

        assert g.m_matrix[1, 0] == 99

    def test_graph_Modularity(self, karate):
        from pyCombo import Graph

        g = Graph(karate)

        g.SetCommunities(new_communities=np.zeros(g.m_size, dtype=np.int))
        assert g.m_communityNumber == 1

        v = g.Modularity()
        assert v == -3.469446951953614e-18

    def test_check_modularity(self):
        bbl = nx.barbell_graph(10, 0)
        import community
        from pyCombo import Graph

        g = Graph(bbl)
        l = community.best_partition(bbl)
        zz = np.array(list(l.values()))

        g.SetCommunities(new_communities=zz)

        lw_modularity = community.modularity(l, bbl)
        assert g.Modularity() == lw_modularity, g.m_modMatrix

    def test_isCommunityEmpty(self, karate):
        from pyCombo import Graph

        g = Graph(karate)
        g.SetCommunities(new_communities=np.zeros(g.m_size, dtype=np.int))

        assert g.IsCommunityEmpty(1)

    def PerformSplit(self, karate):
        from pyCombo import Graph

        g = Graph(karate)
        g.SetCommunities(new_communities=np.zeros(g.m_size, dtype=np.int))

        mask = np.zeros(g.m_size)
        mask[:10] = 1

        g.PerformSplit(0, 1, mask)

        assert g.m_communityNumber == 2
        assert g.m_communities.sum() == 10

