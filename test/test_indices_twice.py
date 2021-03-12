import bwsample as bws
import itertools
from collections import Counter


def test1(recwarn):
    n_sets, n_items, shuffle = 1, 4, False
    bwsindices, n_examples = bws.sampling.indices_twice(
        n_sets, n_items, shuffle)
    assert len(recwarn) == 1
    w = recwarn.pop(UserWarning)
    assert str(w.message) == "Only one BWS set requested."
    counts = list(Counter(itertools.chain(*bwsindices)).values())
    assert all([c == 1 for c in counts])


def test2():
    n_sets, n_items, shuffle = 2, 4, False
    bwsindices, n_examples = bws.sampling.indices_twice(
        n_sets, n_items, shuffle)
    counts = list(Counter(itertools.chain(*bwsindices)).values())
    assert all([c == 2 for c in counts])


def test3():
    n_sets, n_items, shuffle = 100, 2, False
    bwsindices, n_examples = bws.sampling.indices_twice(
        n_sets, n_items, shuffle)
    counts = list(Counter(itertools.chain(*bwsindices)).values())
    assert all([c == 2 for c in counts])


def test4():
    n_sets, n_items, shuffle = 100, 3, False
    bwsindices, n_examples = bws.sampling.indices_twice(
        n_sets, n_items, shuffle)
    counts = list(Counter(itertools.chain(*bwsindices)).values())
    assert sum([c == 2 for c in counts]) > (100 - 3)


def test5():
    n_sets, n_items, shuffle = 100, 4, False
    bwsindices, n_examples = bws.sampling.indices_twice(
        n_sets, n_items, shuffle)
    counts = list(Counter(itertools.chain(*bwsindices)).values())
    assert all([c == 2 for c in counts])


def test6():
    n_sets, n_items, shuffle = 5, 3, False
    bwsindices, n_examples = bws.sampling.indices_twice(
        n_sets, n_items, shuffle)
    for bwsset in bwsindices:
        assert len(bwsset) == 3
