import numpy as np
import warnings
from typing import List, Optional


def indices_overlap(n_sets: int, n_items: int,
                    permute: Optional[bool] = True) -> (List[List[int]], int):
    """Generate BWS set indices so that each example occur at least once,
        and exactly `1/(n_items - 1) * 100%` of examples occur twice across
        all generate BWS sets.

    Parameters:
    -----------
    n_sets: int
        Requested number of BWS sets

    n_items: int
        Number items per BWS set

    permute: bool=True
        Flag to permute indicies

    Return:
    -------
    bwsindices: List[List[int]]
        A list of `n_sets` BWS sets. Each BWS set is a list
          of `n_items` indicies.

    n_examples: int
        The number of indicies spread across the BWS sets. The indicies can
          be generated as follows: `indicies=range(0, n_examples)`

    Examples:
    ---------
        from bwsample import bws_sets_overlap
        bwsindices, n_examples = bws_sets_overlap(1000, 4, False)

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
        if permute:
            return [list(np.random.permutation(n_items))], n_items
        else:
            return [list(range(0, n_items))], n_items

    # compute required number of examples
    n_examples = n_sets * (n_items - 1)

    # generate a `pool` of indicies
    if permute:
        pool = list(np.random.permutation(n_examples))
    else:
        pool = list(range(0, n_examples))

    # copy from indicies `pool`
    bwsindices = [pool[k:(k + n_items)]
                  for k in range(0, n_examples, n_items - 1)]
    bwsindices[-1].append(bwsindices[0][0])

    # done
    return bwsindices, n_examples
