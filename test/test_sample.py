import bwsample
import itertools
from collections import Counter


def test1(recwarn):
    n_items, shuffle = 4, False
    examples = ['a']
    sample = bwsample.sample(examples, n_items=n_items, shuffle=shuffle)
    assert len(recwarn) == 1
    w = recwarn.pop(UserWarning)
    assert str(w.message) == "Zero BWS sets requested."
    assert sample == []


def test2():
    n_items, shuffle = 4, False
    examples = ['a', 'b']
    sample = bwsample.sample(examples, n_items=n_items, shuffle=shuffle)
    assert sample == []


def test3():
    n_items, shuffle, method = 2, False, 'overlap'
    examples = [chr(x) for x in range(100)]
    sample = bwsample.sample(
        examples, n_items=n_items, shuffle=shuffle, method=method)
    assert len(sample) == len(examples) // (n_items - 1)
    counts = list(Counter(itertools.chain(*sample)).values())
    assert all([c == 2 for c in counts])


def test4():
    n_items, shuffle, method = 3, False, 'overlap'
    examples = [chr(x) for x in range(100)]
    sample = bwsample.sample(
        examples, n_items=n_items, shuffle=shuffle, method=method)
    assert len(sample) == len(examples) // (n_items - 1)
    counts = list(Counter(itertools.chain(*sample)).values())
    assert sum([c == 2 for c in counts]) == 50
    assert sum([c == 1 for c in counts]) == 50


def test5():
    n_items, shuffle, method = 3, False, 'twice'
    examples = [chr(x) for x in range(100)]
    sample = bwsample.sample(
        examples, n_items=n_items, shuffle=shuffle, method=method)
    assert len(sample) == (len(examples) * 2) // n_items
    counts = list(Counter(itertools.chain(*sample)).values())
    # assert sum([c == 2 for c in counts]) == len(sample)
    assert sum(counts) == ((len(examples) * 2) // n_items) * n_items
