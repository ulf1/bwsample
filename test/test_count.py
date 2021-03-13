import bwsample as bws
import uuid


def test1():
    # nn: D>Z, X>F
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'E', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, direct_dok, direct_detail, logical_dok, logical_detail = bws.count(
        [(states1, ids1)], logical_database=[(states2, ids2)])
    target = {('D', 'Z'): 1, ('X', 'F'): 1}
    assert logical_dok == target
    assert logical_detail["nn"] == target
    assert logical_detail["nb"] == {}
    assert logical_detail["nw"] == {}
    assert logical_detail["bn"] == {}
    assert logical_detail["bw"] == {}
    assert logical_detail["wn"] == {}
    assert logical_detail["wb"] == {}
    assert direct_dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1}
    assert direct_detail["bw"] == {('D', 'F'): 1}
    assert direct_detail["bn"] == {('D', 'E'): 1}
    assert direct_detail["nw"] == {('E', 'F'): 1}
    assert dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1, **target}


def test2():
    # nb: D>Y, D>Z
    ids1, ids2 = ('D', 'E', 'F'), ('E', 'Y', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, direct_dok, direct_detail, logical_dok, logical_detail = bws.count(
        [(states1, ids1)], logical_database=[(states2, ids2)])
    target = {('D', 'Y'): 1, ('D', 'Z'): 1}
    assert logical_dok == target
    assert logical_detail["nn"] == {}
    assert logical_detail["nb"] == target
    assert logical_detail["nw"] == {}
    assert logical_detail["bn"] == {}
    assert logical_detail["bw"] == {}
    assert logical_detail["wn"] == {}
    assert logical_detail["wb"] == {}
    assert direct_dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1}
    assert direct_detail["bw"] == {('D', 'F'): 1}
    assert direct_detail["bn"] == {('D', 'E'): 1}
    assert direct_detail["nw"] == {('E', 'F'): 1}
    assert dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1, **target}


def test3():
    # nw: X>F, Y>F
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'Y', 'E')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, direct_dok, direct_detail, logical_dok, logical_detail = bws.count(
        [(states1, ids1)], logical_database=[(states2, ids2)])
    target = {('X', 'F'): 1, ('Y', 'F'): 1}
    assert logical_dok == target
    assert logical_detail["nn"] == {}
    assert logical_detail["nb"] == {}
    assert logical_detail["nw"] == target
    assert logical_detail["bn"] == {}
    assert logical_detail["bw"] == {}
    assert logical_detail["wn"] == {}
    assert logical_detail["wb"] == {}
    assert direct_dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1}
    assert direct_detail["bw"] == {('D', 'F'): 1}
    assert direct_detail["bn"] == {('D', 'E'): 1}
    assert direct_detail["nw"] == {('E', 'F'): 1}
    assert dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1, **target}


def test4():
    # bn: X>E, X>F
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'D', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, direct_dok, direct_detail, logical_dok, logical_detail = bws.count(
        [(states1, ids1)], logical_database=[(states2, ids2)])
    target = {('X', 'E'): 1, ('X', 'F'): 1}
    assert logical_dok == target
    assert logical_detail["nn"] == {}
    assert logical_detail["nb"] == {}
    assert logical_detail["nw"] == {}
    assert logical_detail["bn"] == target
    assert logical_detail["bw"] == {}
    assert logical_detail["wn"] == {}
    assert logical_detail["wb"] == {}
    assert direct_dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1}
    assert direct_detail["bw"] == {('D', 'F'): 1}
    assert direct_detail["bn"] == {('D', 'E'): 1}
    assert direct_detail["nw"] == {('E', 'F'): 1}
    assert dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1, **target}


def test5():
    # bb: n.a.
    ids1, ids2 = ('D', 'E', 'F'), ('D', 'Y', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, direct_dok, direct_detail, logical_dok, logical_detail = bws.count(
        [(states1, ids1)], logical_database=[(states2, ids2)])
    assert logical_dok == {}
    assert logical_detail["nn"] == {}
    assert logical_detail["nb"] == {}
    assert logical_detail["nw"] == {}
    assert logical_detail["bn"] == {}
    assert logical_detail["bw"] == {}
    assert logical_detail["wn"] == {}
    assert logical_detail["wb"] == {}
    assert direct_dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1}
    assert direct_detail["bw"] == {('D', 'F'): 1}
    assert direct_detail["bn"] == {('D', 'E'): 1}
    assert direct_detail["nw"] == {('E', 'F'): 1}
    assert dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1}


def test6():
    # bw: X>E, X>F, Y>E, Y>F
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'Y', 'D')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, direct_dok, direct_detail, logical_dok, logical_detail = bws.count(
        [(states1, ids1)], logical_database=[(states2, ids2)])
    target = {('X', 'E'): 1, ('X', 'F'): 1, ('Y', 'E'): 1, ('Y', 'F'): 1}
    assert logical_dok == target
    assert logical_detail["nn"] == {}
    assert logical_detail["nb"] == {}
    assert logical_detail["nw"] == {}
    assert logical_detail["bn"] == {}
    assert logical_detail["bw"] == target
    assert logical_detail["wn"] == {}
    assert logical_detail["wb"] == {}
    assert direct_dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1}
    assert direct_detail["bw"] == {('D', 'F'): 1}
    assert direct_detail["bn"] == {('D', 'E'): 1}
    assert direct_detail["nw"] == {('E', 'F'): 1}
    assert dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1, **target}


def test7():
    # wn: D>Z, E>Z
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'F', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, direct_dok, direct_detail, logical_dok, logical_detail = bws.count(
        [(states1, ids1)], logical_database=[(states2, ids2)])
    target = {('D', 'Z'): 1, ('E', 'Z'): 1}
    assert logical_dok == target
    assert logical_detail["nn"] == {}
    assert logical_detail["nb"] == {}
    assert logical_detail["nw"] == {}
    assert logical_detail["bn"] == {}
    assert logical_detail["bw"] == {}
    assert logical_detail["wn"] == target
    assert logical_detail["wb"] == {}
    assert direct_dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1}
    assert direct_detail["bw"] == {('D', 'F'): 1}
    assert direct_detail["bn"] == {('D', 'E'): 1}
    assert direct_detail["nw"] == {('E', 'F'): 1}
    assert dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1, **target}


def test8():
    # wb: D>Y, D>Z, E>Y, E>Z
    ids1, ids2 = ('D', 'E', 'F'), ('F', 'Y', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, direct_dok, direct_detail, logical_dok, logical_detail = bws.count(
        [(states1, ids1)], logical_database=[(states2, ids2)])
    target = {('D', 'Y'): 1, ('D', 'Z'): 1, ('E', 'Y'): 1, ('E', 'Z'): 1}
    assert logical_dok == target
    assert logical_detail["nn"] == {}
    assert logical_detail["nb"] == {}
    assert logical_detail["nw"] == {}
    assert logical_detail["bn"] == {}
    assert logical_detail["bw"] == {}
    assert logical_detail["wn"] == {}
    assert logical_detail["wb"] == target
    assert direct_dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1}
    assert direct_detail["bw"] == {('D', 'F'): 1}
    assert direct_detail["bn"] == {('D', 'E'): 1}
    assert direct_detail["nw"] == {('E', 'F'): 1}
    assert dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1, **target}


def test9():
    # ww: n.a.
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'Y', 'F')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, direct_dok, direct_detail, logical_dok, logical_detail = bws.count(
        [(states1, ids1)], logical_database=[(states2, ids2)])
    assert logical_dok == {}
    assert logical_detail["nn"] == {}
    assert logical_detail["nb"] == {}
    assert logical_detail["nw"] == {}
    assert logical_detail["bn"] == {}
    assert logical_detail["bw"] == {}
    assert logical_detail["wn"] == {}
    assert logical_detail["wb"] == {}
    assert direct_dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1}
    assert direct_detail["bw"] == {('D', 'F'): 1}
    assert direct_detail["bn"] == {('D', 'E'): 1}
    assert direct_detail["nw"] == {('E', 'F'): 1}
    assert dok == {('D', 'E'): 1, ('D', 'F'): 1, ('E', 'F'): 1}


def test11():
    stateids = ['abc', 'def', 'ghi', 'jkl']
    combostates = [0, 0, 2, 1]

    _, direct_dok, direct_detail, _, _ = bws.count(
        [(combostates, stateids)], use_logical=False)

    assert direct_dok == {
        ('jkl', 'ghi'): 1, ('jkl', 'abc'): 1, ('abc', 'ghi'): 1,
        ('jkl', 'def'): 1, ('def', 'ghi'): 1}
    assert direct_detail["bw"] == {('jkl', 'ghi'): 1}
    assert direct_detail["bn"] == {('jkl', 'abc'): 1, ('jkl', 'def'): 1}
    assert direct_detail["nw"] == {('abc', 'ghi'): 1, ('def', 'ghi'): 1}
    assert sorted({
        **direct_detail["bw"], **direct_detail["bn"],
        **direct_detail["nw"]}) == sorted(direct_dok)


def test12():
    stateids = ['abc', 'def', 'ghi', 'jkl']
    combostates = [0, 0, 2, 1]

    _, direct_dok, direct_detail, _, _ = bws.count(
        [(combostates, stateids)], use_logical=False)

    _, direct_dok, direct_detail, _, _ = bws.count(
        [(combostates, stateids)], use_logical=False,
        direct_dok=direct_dok, direct_detail=direct_detail)

    assert direct_dok == {
        ('jkl', 'ghi'): 2, ('jkl', 'abc'): 2, ('abc', 'ghi'): 2,
        ('jkl', 'def'): 2, ('def', 'ghi'): 2}
    assert direct_detail["bw"] == {('jkl', 'ghi'): 2}
    assert direct_detail["bn"] == {('jkl', 'abc'): 2, ('jkl', 'def'): 2}
    assert direct_detail["nw"] == {('abc', 'ghi'): 2, ('def', 'ghi'): 2}
    assert sorted({
        **direct_detail["bw"], **direct_detail["bn"],
        **direct_detail["nw"]}) == sorted(direct_dok)


def test13():
    stateids = [str(uuid.uuid4()) for _ in range(10**3 + 2)]
    combostates = [0 for _ in range(10**3)] + [1, 2]

    _, direct_dok, direct_detail, _, _ = bws.count(
        [(combostates, stateids)], use_logical=False)

    assert list(direct_detail["bw"].values())[0] == 1
    assert sorted({
        **direct_detail["bw"], **direct_detail["bn"],
        **direct_detail["nw"]}) == sorted(direct_dok)
