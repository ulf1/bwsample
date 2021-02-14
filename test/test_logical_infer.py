from bwsample import logical_infer


def test1():
    # mm: D>Z, X>F
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'E', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok = logical_infer(ids1, ids2, states1, states2)
    assert dok == {('D', 'Z'): 1, ('X', 'F'): 1}


def test2():
    # mb: D>Y, D>Z
    ids1, ids2 = ('D', 'E', 'F'), ('E', 'Y', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok = logical_infer(ids1, ids2, states1, states2)
    assert dok == {('D', 'Y'): 1, ('D', 'Z'): 1}


def test3():
    # mw: X>F, Y>F
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'Y', 'E')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok = logical_infer(ids1, ids2, states1, states2)
    assert dok == {('X', 'F'): 1, ('Y', 'F'): 1}


def test4():
    # bm: X>E, X>F
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'D', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok = logical_infer(ids1, ids2, states1, states2)
    assert dok == {('X', 'E'): 1, ('X', 'F'): 1}


def test5():
    # bb: n.a.
    ids1, ids2 = ('D', 'E', 'F'), ('D', 'Y', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok = logical_infer(ids1, ids2, states1, states2)
    assert dok == {}


def test6():
    # bw: X>E, X>F, Y>E, Y>F
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'Y', 'D')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok = logical_infer(ids1, ids2, states1, states2)
    assert dok == {('X', 'E'): 1, ('X', 'F'): 1, ('Y', 'E'): 1, ('Y', 'F'): 1}


def test7():
    # wm: D>Z, E>Z
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'F', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok = logical_infer(ids1, ids2, states1, states2)
    assert dok == {('D', 'Z'): 1, ('E', 'Z'): 1}


def test8():
    # wb: D>Y, D>Z, E>Y, E>Z
    ids1, ids2 = ('D', 'E', 'F'), ('F', 'Y', 'Z')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok = logical_infer(ids1, ids2, states1, states2)
    assert dok == {('D', 'Y'): 1, ('D', 'Z'): 1, ('E', 'Y'): 1, ('E', 'Z'): 1}


def test9():
    # ww: n.a.
    ids1, ids2 = ('D', 'E', 'F'), ('X', 'Y', 'F')
    states1, states2 = (1, 0, 2), (1, 0, 2)
    dok = logical_infer(ids1, ids2, states1, states2)
    assert dok == {}
