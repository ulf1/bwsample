import bwsample as bws


def test1():
    # nn: D>Z, X>F
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'E', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, nn, nb, nw, bn, bw, wn, wb = bws.counting.logical_infer(
        ids1, ids2, states1, states2)
    target = {('D', 'Z'): 1, ('X', 'F'): 1}
    assert dok == target
    assert nn == target
    assert nb == {}
    assert nw == {}
    assert bn == {}
    assert bw == {}
    assert wn == {}
    assert wb == {}


def test2():
    # nb: D>Y, D>Z
    ids1, ids2 = ('D', 'E', 'F'), ('E', 'Y', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, nn, nb, nw, bn, bw, wn, wb = bws.counting.logical_infer(
        ids1, ids2, states1, states2)
    target = {('D', 'Y'): 1, ('D', 'Z'): 1}
    assert dok == target
    assert nn == {}
    assert nb == target
    assert nw == {}
    assert bn == {}
    assert bw == {}
    assert wn == {}
    assert wb == {}


def test3():
    # nw: X>F, Y>F
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'Y', 'E')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, nn, nb, nw, bn, bw, wn, wb = bws.counting.logical_infer(
        ids1, ids2, states1, states2)
    target = {('X', 'F'): 1, ('Y', 'F'): 1}
    assert dok == target
    assert nn == {}
    assert nb == {}
    assert nw == target
    assert bn == {}
    assert bw == {}
    assert wn == {}
    assert wb == {}


def test4():
    # bn: X>E, X>F
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'D', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, nn, nb, nw, bn, bw, wn, wb = bws.counting.logical_infer(
        ids1, ids2, states1, states2)
    target = {('X', 'E'): 1, ('X', 'F'): 1}
    assert dok == target
    assert nn == {}
    assert nb == {}
    assert nw == {}
    assert bn == target
    assert bw == {}
    assert wn == {}
    assert wb == {}


def test5():
    # bb: n.a.
    ids1, ids2 = ('D', 'E', 'F'), ('D', 'Y', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, nn, nb, nw, bn, bw, wn, wb = bws.counting.logical_infer(
        ids1, ids2, states1, states2)
    assert dok == {}
    assert nn == {}
    assert nb == {}
    assert nw == {}
    assert bn == {}
    assert bw == {}
    assert wn == {}
    assert wb == {}


def test6():
    # bw: X>E, X>F, Y>E, Y>F
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'Y', 'D')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, nn, nb, nw, bn, bw, wn, wb = bws.counting.logical_infer(
        ids1, ids2, states1, states2)
    target = {('X', 'E'): 1, ('X', 'F'): 1, ('Y', 'E'): 1, ('Y', 'F'): 1}
    assert dok == target
    assert nn == {}
    assert nb == {}
    assert nw == {}
    assert bn == {}
    assert bw == target
    assert wn == {}
    assert wb == {}


def test7():
    # wn: D>Z, E>Z
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'F', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, nn, nb, nw, bn, bw, wn, wb = bws.counting.logical_infer(
        ids1, ids2, states1, states2)
    target = {('D', 'Z'): 1, ('E', 'Z'): 1}
    assert dok == target
    assert nn == {}
    assert nb == {}
    assert nw == {}
    assert bn == {}
    assert bw == {}
    assert wn == target
    assert wb == {}


def test8():
    # wb: D>Y, D>Z, E>Y, E>Z
    ids1, ids2 = ('D', 'E', 'F'), ('F', 'Y', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, nn, nb, nw, bn, bw, wn, wb = bws.counting.logical_infer(
        ids1, ids2, states1, states2)
    target = {('D', 'Y'): 1, ('D', 'Z'): 1, ('E', 'Y'): 1, ('E', 'Z'): 1}
    assert dok == target
    assert nn == {}
    assert nb == {}
    assert nw == {}
    assert bn == {}
    assert bw == {}
    assert wn == {}
    assert wb == target


def test9():
    # ww: n.a.
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'Y', 'F')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok, nn, nb, nw, bn, bw, wn, wb = bws.counting.logical_infer(
        ids1, ids2, states1, states2)
    assert dok == {}
    assert nn == {}
    assert nb == {}
    assert nw == {}
    assert bn == {}
    assert bw == {}
    assert wn == {}
    assert wb == {}
