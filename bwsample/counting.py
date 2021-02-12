from typing import List, Optional


def extract_pairs(stateids: List[str], combostates: List[int],
                  dok_all: Optional[dict] = None,
                  dok_direct: Optional[dict] = None,
                  dok_best: Optional[dict] = None,
                  dok_worst: Optional[dict] = None) -> (
                      dict, dict, dict, dict):
    """
    """
    # find `best` and `worst` py index
    # (this is 2-3x faster than a loop with if-else)
    best_idx = combostates.index(1)
    worst_idx = combostates.index(2)

    # Dict[Tuple[uuid, uuid], count]]
    # - dictionary of key sparse matrix
    # - Each pair(i,j) refers to ">"
    if dok_all is None:
        dok_all, dok_direct, dok_best, dok_worst = {}, {}, {}, {}

    # add the direct best-worst observation
    best_uuid = stateids[best_idx]
    worst_uuid = stateids[worst_idx]

    idxpair = (best_uuid, worst_uuid)
    dok_all[idxpair] = 1 + dok_all.get(idxpair, 0)
    dok_direct[idxpair] = 1 + dok_direct.get(idxpair, 0)

    # loop over all other elements
    for middle_idx, middle_uuid in enumerate(stateids):
        if middle_idx not in (best_idx, worst_idx):
            # add `best > middle`
            idxpair = (best_uuid, middle_uuid)
            dok_all[idxpair] = 1 + dok_all.get(idxpair, 0)
            dok_best[idxpair] = 1 + dok_best.get(idxpair, 0)

            # add `middle > worst`
            idxpair = (middle_uuid, worst_uuid)
            dok_all[idxpair] = 1 + dok_all.get(idxpair, 0)
            dok_worst[idxpair] = 1 + dok_worst.get(idxpair, 0)

    # done
    return dok_all, dok_direct, dok_best, dok_worst
