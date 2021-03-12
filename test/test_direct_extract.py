import bwsample as bws
import uuid


def test1():
    stateids = ['abc', 'def', 'ghi', 'jkl']
    combostates = [0, 0, 2, 1]

    dok, dok_bw, dok_bn, dok_nw = bws.counting.direct_extract(
        stateids, combostates)

    assert dok == {
        ('jkl', 'ghi'): 1, ('jkl', 'abc'): 1, ('abc', 'ghi'): 1,
        ('jkl', 'def'): 1, ('def', 'ghi'): 1}
    assert dok_bw == {('jkl', 'ghi'): 1}
    assert dok_bn == {('jkl', 'abc'): 1, ('jkl', 'def'): 1}
    assert dok_nw == {('abc', 'ghi'): 1, ('def', 'ghi'): 1}
    assert sorted({**dok_bw, **dok_bn, **dok_nw}) == sorted(dok)


def test2():
    stateids = ['abc', 'def', 'ghi', 'jkl']
    combostates = [0, 0, 2, 1]

    dok, dok_bw, dok_bn, dok_nw = bws.counting.direct_extract(
        stateids, combostates)

    dok, dok_bw, dok_bn, dok_nw = bws.counting.direct_extract(
        stateids, combostates, dok=dok, dok_bw=dok_bw,
        dok_bn=dok_bn, dok_nw=dok_nw)

    assert dok == {
        ('jkl', 'ghi'): 2, ('jkl', 'abc'): 2, ('abc', 'ghi'): 2,
        ('jkl', 'def'): 2, ('def', 'ghi'): 2}
    assert dok_bw == {('jkl', 'ghi'): 2}
    assert dok_bn == {('jkl', 'abc'): 2, ('jkl', 'def'): 2}
    assert dok_nw == {('abc', 'ghi'): 2, ('def', 'ghi'): 2}
    assert sorted({**dok_bw, **dok_bn, **dok_nw}) == sorted(dok)


def test3():
    stateids = [str(uuid.uuid4()) for _ in range(10**3 + 2)]
    combostates = [0 for _ in range(10**3)] + [1, 2]

    dok, dok_bw, dok_bn, dok_nw = bws.counting.direct_extract(
        stateids, combostates)

    assert list(dok_bw.values())[0] == 1
    assert sorted({**dok_bw, **dok_bn, **dok_nw}) == sorted(dok)
