import bwsample as bws
import itertools


def test1(recwarn):
    n_sets, n_items, shuffle = 0, 0, None
    bwsindices, n_examples = bws.sampling.indices_overlap(
        n_sets, n_items, shuffle)
    assert bwsindices == []
    assert n_examples == 0
    assert len(recwarn) == 1
    w = recwarn.pop(UserWarning)
    assert str(w.message) == "No overlap possible with n_items=0."


def test2(recwarn):
    n_sets, n_items, shuffle = 0, 1, None
    bwsindices, n_examples = bws.sampling.indices_overlap(
        n_sets, n_items, shuffle)
    assert bwsindices == []
    assert n_examples == 0
    assert len(recwarn) == 1
    w = recwarn.pop(UserWarning)
    assert str(w.message) == "No overlap possible with n_items=1."


def test3(recwarn):
    n_sets, n_items, shuffle = 0, 2, None
    bwsindices, n_examples = bws.sampling.indices_overlap(
        n_sets, n_items, shuffle)
    assert bwsindices == []
    assert n_examples == 0
    assert len(recwarn) == 1
    w = recwarn.pop(UserWarning)
    assert str(w.message) == "Zero BWS sets requested."


def test4(recwarn):
    n_sets, n_items, shuffle = 1, 2, None
    bwsindices, n_examples = bws.sampling.indices_overlap(
        n_sets, n_items, shuffle)
    assert bwsindices == [[0, 1]]
    assert n_examples == 2
    assert len(recwarn) == 1
    w = recwarn.pop(UserWarning)
    assert str(w.message) == "Only one BWS set requested."


def test5():
    n_sets, n_items, shuffle = 4, 2, False
    bwsindices, n_examples = bws.sampling.indices_overlap(
        n_sets, n_items, shuffle)
    assert bwsindices == [[0, 1], [1, 2], [2, 3], [3, 0]]
    assert n_examples == 4


def test6():
    n_sets, n_items, shuffle = 4, 3, False
    bwsindices, n_examples = bws.sampling.indices_overlap(
        n_sets, n_items, shuffle)
    assert bwsindices == [[0, 1, 2], [2, 3, 4], [4, 5, 6], [6, 7, 0]]
    assert n_examples == 8


def test7():
    n_sets, n_items, shuffle = 4, 4, False
    bwsindices, n_examples = bws.sampling.indices_overlap(
        n_sets, n_items, shuffle)
    assert bwsindices == [
        [0, 1, 2, 3], [3, 4, 5, 6], [6, 7, 8, 9], [9, 10, 11, 0]]
    assert n_examples == 12


def test8():
    n_sets, n_items, shuffle = 4, 5, False
    bwsindices, n_examples = bws.sampling.indices_overlap(
        n_sets, n_items, shuffle)
    assert bwsindices == [
        [0, 1, 2, 3, 4], [4, 5, 6, 7, 8],
        [8, 9, 10, 11, 12], [12, 13, 14, 15, 0]]
    assert n_examples == 16


def test9():
    n_sets, n_items, shuffle = 1000, 6, False
    bwsindices, n_examples = bws.sampling.indices_overlap(
        n_sets, n_items, shuffle)
    assert len(bwsindices) == 1000
    assert len(bwsindices[0]) == 6
    assert n_examples == n_sets * (n_items - 1)


def test11():
    n_sets, n_items, shuffle = 100, 5, True
    bwsindices, n_examples = bws.sampling.indices_overlap(
        n_sets, n_items, shuffle)
    idx1 = list(itertools.chain(*bwsindices))
    idx2 = list(range(n_examples))
    for i in idx1:
        assert i in idx2
    for i in idx2:
        assert i in idx1
