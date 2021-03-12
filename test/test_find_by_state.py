import bwsample as bws


def test1():
    ids = ['a', 'b', 'c', 'd']
    states = [0, 1, 0, 2]
    ids2 = bws.counting.find_by_state(ids, states, [0])
    assert ids2 == ['a', 'c']
