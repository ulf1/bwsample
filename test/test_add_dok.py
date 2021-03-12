import bwsample as bws


def test1():
    a = {"key": 2, "misc": 3, ("id1", "id2"): 7}
    b = {"misc": 1}
    c = bws.add_dok(a, b)
    assert c == {"key": 2, "misc": 4, ("id1", "id2"): 7}

    c = bws.add_dok(b, a)
    assert c == {"key": 2, "misc": 4, ("id1", "id2"): 7}


def test2():
    a = {"key": 2, "misc": 3, ("id1", "id2"): 7}
    b = {"misc": -1, ("id1", "id2"): 2}
    c = bws.add_dok(a, b)
    assert c == {"key": 2, "misc": 2, ("id1", "id2"): 9}

    c = bws.add_dok(b, a)
    assert c == {"key": 2, "misc": 2, ("id1", "id2"): 9}
