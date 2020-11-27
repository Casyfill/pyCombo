import pytest

def test_modularity_test_graph(test_graph):
    from pyCombo import combo #, modularity
	
    _, modularity_ = combo(test_graph, weight_prop='weight')
    assert modularity_ == pytest.approx(0.16, 0.0001)
    # assert modularity_ == pytest.approx(modularity(test_graph, partition, key='weight') )



def test_modularity_karate(karate):
    from pyCombo import combo

    _, modularity_ = combo(karate)
    assert modularity_ == 0.41979