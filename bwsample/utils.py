import itertools
import scipy.sparse
import numpy as np
from typing import Dict, Tuple, List
ItemID = str


def to_scipy(dok: Dict[Tuple[str, str], int], dtype=np.float64) -> (
        scipy.sparse.dok.dok_matrix, List[str]):
    """Convert dictionary with pairwise comparison frequencies
        in a scipy sparse matrix

    Parameters:
    -----------
    dok : Dict[Tuple[str, str], int]
        Count/Frequency data as Dictionary of Keys (DoK)

    dtype (Default: np.float64)
        Data type of the sparse matrix

    Returns:
    --------
    cnt : scipy.sparse.dok.dok_matrix
        Quadratic sparse matrix with frequency data

    indices : List[str]
        Identifiers, e.g. UUID4, of each row/column of the `cnt` matrix.

    Example:
    --------
        import bwsample as bws
        dok = {('A', 'D'): 3, ('A', 'B'): 2}
        cnt, indices = bws.to_scipy(dok)
    """
    idx = sorted(list(set(itertools.chain(*dok.keys()))))
    n_dim = len(idx)
    cnt = scipy.sparse.dok_matrix((n_dim, n_dim), dtype=dtype)
    for (i, j), v in dok.items():
        cnt[idx.index(i), idx.index(j)] = v
    return cnt, idx


def add_dok(a: Dict[Tuple[ItemID, ItemID], int],
            b: Dict[Tuple[ItemID, ItemID], int]
            ) -> Dict[Tuple[ItemID, ItemID], int]:
    """Add counts of two Dictionary of Keys (DOK) objects

    Parameters:
    -----------
    a, b : Dict[Tuple[ItemID, ItemID], int]
        Two Dictionary of Keys (DOK) objects which values
          are to be added.

    Returns:
    --------
    out : Dict[Tuple[ItemID, ItemID], int]
        A Dictionary of Keys (DOK) objects with the added values
          for each key.

    Example:
    --------
        import bwsample as bws
        a = {"key": 2, "misc": 3, ("id1", "id2"): 7}
        b = {"misc": 1}
        c = bws.add_dok(a, b)

    """
    if len(a) > len(b):
        # copy a to output
        out = a.copy()
        # add b to output
        for key, val in b.items():
            out[key] = val + out.get(key, 0)
    else:
        # copy b to output
        out = b.copy()
        # add a to output
        for key, val in a.items():
            out[key] = val + out.get(key, 0)
    # done
    return out
