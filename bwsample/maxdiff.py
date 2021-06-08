import numpy as np
from typing import List, Tuple
ItemState = int
ItemID = str


def scoring_orme(evaluations: List[Tuple[List[ItemState], List[ItemID]]]):
    """Scoring based on Orme (2009)

    Parameters:
    -----------
    evaluations : List[Tuple[List[ItemState], List[ItemID]]]
        A list of new BWS sets to be evaluated.

    Returns:
    --------
    indices : np.array[any]
        The reordered item IDs

    scores : np.array[float]
        The scaled score for each item ID. Also sorted in descending order.

    Example:
    --------
        import bwsample as bws
        evaluations = (
            ([1, 0, 0, 2], ['A', 'B', 'C', 'D']),
            ([1, 0, 0, 2], ['A', 'B', 'C', 'D']),
            ([2, 0, 0, 1], ['A', 'B', 'C', 'D']),
            ([0, 1, 2, 0], ['A', 'B', 'C', 'D']),
            ([0, 1, 0, 2], ['A', 'B', 'C', 'D']),
        )
        indices, scores = bws.scoring_orme(evaluations)

    References:
    -----------
    Orme, B., 2009. MaxDiff Analysis: Simple Counting, Individual-Level
      Logit, and HB. https://api.semanticscholar.org/CorpusID:202605777
    """
    # count only the best (+1) and worst (-1)
    scorecnt = {}
    for combostates, stateids in evaluations:
        # lookup position
        pos_best = combostates.index(1)
        pos_worst = combostates.index(2)
        # lookup IDs
        id_best = stateids[pos_best]
        id_worst = stateids[pos_worst]
        # increment/decrement
        scorecnt[id_best] = scorecnt.get(id_best, 0) + 1
        scorecnt[id_worst] = scorecnt.get(id_worst, 0) - 1

    # average the scores
    n_evals = len(evaluations)
    indices = []
    scores = []
    for k, v in scorecnt.items():
        indices.append(k)
        scores.append(v / n_evals)

    # sort results
    scores = np.array(scores)
    positions = np.argsort(-scores)
    indices = np.array(indices)[positions]
    scores = scores[positions]

    # done
    return indices, scores
