import numpy as np
import random
import warnings
from typing import List, Optional


def shuffle_subarrs(arrs, n_sets, n_items):
    rj = np.random.randint(1, n_items, n_sets)
    rk = np.random.randint(0, n_items - 1, n_sets)
    for i, (j, k) in enumerate(np.c_[rj, rk]):
        arrs[i][j], arrs[i][0] = arrs[i][0], arrs[i][j]
        if j != k:
            arrs[i][k], arrs[i][-1] = arrs[i][-1], arrs[i][k]
    return arrs


def indices_overlap(n_sets: int, n_items: int,
                    shuffle: Optional[bool] = True) -> (List[List[int]], int):
    """Generate BWS set indices so that each example occur at least once,
        and exactly `1/(n_items - 1) * 100%` of examples occur twice across
        all generate BWS sets.

    Parameters:
    -----------
    n_sets: int
        Requested number of BWS sets

    n_items: int
        Number items per BWS set

    shuffle: bool=True
        Flag to permute/shuffle indices

    Return:
    -------
    bwsindices: List[List[int]]
        A list of `n_sets` BWS sets. Each BWS set is a list
          of `n_items` indices.

    n_examples: int
        The number of indices spread across the BWS sets. The indices can
          be generated as follows: `indices=range(0, n_examples)`

    Examples:
    ---------
        from bwsample import indices_overlap
        bwsindices, n_examples = indices_overlap(1000, 4, False)

    Notes:
    ------
    Using `@numba.jit(nopython=True)` doesn't seem to yield any performance
      benefits.
    """
    # abort
    if n_items < 2:
        warnings.warn(f"No overlap possible with n_items={n_items}.")
        return [], 0
    if n_sets < 1:
        warnings.warn("Zero BWS sets requested.")
        return [], 0
    if n_sets == 1:
        warnings.warn("Only one BWS set requested.")
        if shuffle:
            return [list(np.random.permutation(n_items))], n_items
        else:
            return [list(range(0, n_items))], n_items

    # compute required number of examples
    n_examples = n_sets * (n_items - 1)

    # generate a `pool` of indices
    pool = list(range(0, n_examples))

    # copy from indices `pool`
    bwsindices = [pool[k:(k + n_items)]
                  for k in range(0, n_examples, n_items - 1)]
    bwsindices[-1].append(bwsindices[0][0])

    # shuffle each BWS set
    if shuffle:
        bwsindices = shuffle_subarrs(bwsindices, n_sets, n_items)

    # done
    return bwsindices, n_examples


def indices_twice(n_sets: int, n_items: int,
                  shuffle: Optional[bool] = True) -> (List[List[int]], int):
    """Sample each example at least twice across all generated BWS sets

    Parameters:
    -----------
    n_sets: int
        Requested number of BWS sets

    n_items: int
        Number items per BWS set

    shuffle: bool=True
        Flag to permute/shuffle indices

    Return:
    -------
    bwsindices: List[List[int]]
        A list of `n_sets` BWS sets. Each BWS set is a list
          of `n_items` indices.

    n_examples: int
        The number of indices spread across the BWS sets. The indices can
          be generated as follows: `indices=range(0, n_examples)`

    Examples:
    ---------
        from bwsample import indices_twice
        bwsindices, n_examples = indices_twice(1000, 4, False)
    """
    # (A) Call `indices_overlap` without randomness!
    bwsindices, n_examples = indices_overlap(n_sets, n_items, False)

    if n_items <= 2 or n_sets <= 1:
        return bwsindices, n_examples

    # (B) Add BWS sets so that every index is used twice --
    # number of BWS sets to connect examples
    n_btw = (n_examples * (n_items - 2)) // (n_items * (n_items - 1))

    # which examples from the `pool` have not been used twice?
    avail = [q for q in range(n_examples) if (q % (n_items - 1)) != 0]
    n_avail = n_btw * (len(avail) // n_btw)

    # generate BWS sets
    grid = range(0, n_avail, n_btw)
    grid = grid[:n_items]
    for r in range(n_btw):
        bwsindices.extend([[avail[k + r] for k in grid]])

    # (C) Shuffle here
    if shuffle:
        bwsindices = shuffle_subarrs(bwsindices, n_sets, n_items)

    # done
    return bwsindices, n_examples
