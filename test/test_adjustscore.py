import bwsample as bws
import numpy as np
import random


def test1():
    scores = [random.random() for _ in range(1000)]
    adjusted = bws.adjustscore(scores, method='quantile')
    assert np.argsort(scores).tolist() == np.argsort(adjusted).tolist()


def test2():
    scores = [.1, .3, .5, .7]
    adjusted = bws.adjustscore(scores, method='quantile')
    assert np.argsort(scores).tolist() == np.argsort(adjusted).tolist()


def test3():
    scores = [random.random() for _ in range(1000)]
    adjusted = bws.adjustscore(scores, method='sig3iqr')
    assert np.argsort(scores).tolist() == np.argsort(adjusted).tolist()


def test4():
    scores = [.1, .3, .5, .7]
    adjusted = bws.adjustscore(scores, method='sig3iqr')
    assert np.argsort(scores).tolist() == np.argsort(adjusted).tolist()


def test5():
    scores = [random.random() for _ in range(1000)]
    labels = [s > 0.5 for s in scores]
    adjusted = bws.adjustscore(scores, method='platt', labels=labels)
    assert np.argsort(scores).tolist() == np.argsort(adjusted).tolist()


def test6():
    scores = [.1, .3, .5, .7]
    labels = [s > 0.5 for s in scores]
    adjusted = bws.adjustscore(scores, method='platt', labels=labels)
    assert np.argsort(scores).tolist() == np.argsort(adjusted).tolist()


def test7():
    scores = [random.random() for _ in range(1000)]
    adjusted = bws.adjustscore(scores, method='minmax')
    assert np.argsort(scores).tolist() == np.argsort(adjusted).tolist()


def test8():
    scores = [.1, .3, .5, .7]
    adjusted = bws.adjustscore(scores, method='minmax')
    assert np.argsort(scores).tolist() == np.argsort(adjusted).tolist()
