from bwsample import extract_pairs
import uuid


def test1():
    stateids = ['abc', 'def', 'ghi', 'jkl']
    combostates = [0, 0, 2, 1]

    dok_all, dok_direct, dok_best, dok_worst = extract_pairs(
        stateids, combostates)

    assert dok_all == {
        ('jkl', 'ghi'): 1, ('jkl', 'abc'): 1, ('abc', 'ghi'): 1,
        ('jkl', 'def'): 1, ('def', 'ghi'): 1}
    assert dok_direct == {('jkl', 'ghi'): 1}
    assert dok_best == {('jkl', 'abc'): 1, ('jkl', 'def'): 1}
    assert dok_worst == {('abc', 'ghi'): 1, ('def', 'ghi'): 1}
    assert sorted({**dok_direct, **dok_best, **dok_worst}) == sorted(dok_all)


def test2():
    stateids = ['abc', 'def', 'ghi', 'jkl']
    combostates = [0, 0, 2, 1]

    dok_all, dok_direct, dok_best, dok_worst = extract_pairs(
        stateids, combostates)

    dok_all, dok_direct, dok_best, dok_worst = extract_pairs(
        stateids, combostates, dok_all=dok_all, dok_direct=dok_direct,
        dok_best=dok_best, dok_worst=dok_worst)

    assert dok_all == {
        ('jkl', 'ghi'): 2, ('jkl', 'abc'): 2, ('abc', 'ghi'): 2,
        ('jkl', 'def'): 2, ('def', 'ghi'): 2}
    assert dok_direct == {('jkl', 'ghi'): 2}
    assert dok_best == {('jkl', 'abc'): 2, ('jkl', 'def'): 2}
    assert dok_worst == {('abc', 'ghi'): 2, ('def', 'ghi'): 2}
    assert sorted({**dok_direct, **dok_best, **dok_worst}) == sorted(dok_all)


def test3():
    stateids = [str(uuid.uuid4()) for _ in range(10**3 + 2)]
    combostates = [0 for _ in range(10**3)] + [1, 2]

    dok_all, dok_direct, dok_best, dok_worst = extract_pairs(
        stateids, combostates)

    assert list(dok_direct.values())[0] == 1
    assert sorted({**dok_direct, **dok_best, **dok_worst}) == sorted(dok_all)
