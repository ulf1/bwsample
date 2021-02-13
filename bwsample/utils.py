import itertools
import scipy.sparse
import numpy as np


def to_scipy(dok, dtype=np.float64):
    idx = sorted(list(set(itertools.chain(*dok.keys()))))
    n_dim = len(idx)
    S = scipy.sparse.dok_matrix((n_dim, n_dim), dtype=dtype)
    for (i, j), v in dok.items():
        S[idx.index(i), idx.index(j)] = v
    return S, idx
