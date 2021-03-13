import bwsample as bws


def test1():
    dok = {('A', 'D'): 3, ('A', 'B'): 2}
    cnt, indices = bws.to_scipy(dok, dtype=int)
    assert cnt.shape == (3, 3)
    assert len(indices) == 3
    assert cnt[0, 1] == 2  # A,B
    assert cnt[0, 2] == 3  # A,D
