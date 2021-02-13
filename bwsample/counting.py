from typing import List, Optional


def extract_pairs(stateids: List[str],
                  combostates: List[int],
                  dok_all: Optional[dict] = None,
                  dok_direct: Optional[dict] = None,
                  dok_best: Optional[dict] = None,
                  dok_worst: Optional[dict] = None) -> (
                      dict, dict, dict, dict):
    """Extract ">" Pairs from one evaluated BWS set

    Parameters:
    -----------
    stateids: List[str]
        A list of IDs (e.g. uuid) corresponding to the `combostates` list.

    combostates: List[int]
        Combinatorial state variable. Each element of the list
          - corresponds to an ID in the `stateids` list,
          - represents an item state variable (or the i-th FSM), and
          - can habe one of the three states:
            - 0: MIDDLE, unselected (initial state)
            - 1: BEST
            - 2: WORST
        (see TR-225)

    dok_all: Optional[dict]
        Existing `dok_all` dictionary that is updated here. see below.

    dok_direct: Optional[dict]
        Existing `dok_direct` dictionary that is updated here. see below.

    dok_best: Optional[dict]
        Existing `dok_best` dictionary that is updated here. see below.

    dok_worst: Optional[dict]
        Existing `dok_worst` dictionary that is updated here. see below.

    Returns:
    --------
    dok_all: dict
        Dictionary with counts for each ">" pair, e.g. an
          entry `{..., ('B', 'C'): 1, ...} means `B>C` was counted `1` times.
        We can extract 3 types of pairs from 1 BWS set:
          - "BEST > WORST" (see dok_direct)
          - "BEST > MIDDLE" (see dok_best)
          - "MIDDLE > WORST" (see dok_worst)
        The `dok_all` dictionary contains the aggregate counts of the types
          of pairs. Use `dok_direct`, `dok_best` and `dok_worst` for
          attribution analysis.

    dok_direct: dict
        Dictionary with counts for explicit "BEST > WORST" pairs.

    dok_best: dict
        Dictionary with counts for "BEST > MIDDLE" pairs.

    dok_worst: dict
        Dictionary with counts for "MIDDLE > WORST" pairs.

    Examples:
    ---------
        from bwsample import extract_pairs

        # First BWS set
        stateids = ['A', 'B', 'C', 'D']
        combostates = [0, 0, 2, 1]  # BEST=1, WORST=2
        dok_all, dok_direct, dok_best, dok_worst = extract_pairs(
            stateids, combostates)

        # Update dictionary by processing the next BWS set
        stateids = ['D', 'E', 'F', 'A']
        combostates = [0, 1, 0, 2]
        dok_all, dok_direct, dok_best, dok_worst = extract_pairs(
            stateids, combostates, dok_all=dok_all, dok_direct=dok_direct,
            dok_best=dok_best, dok_worst=dok_worst)
    """
    if len(stateids) != len(combostates):
        raise Exception("IDs and states lists must have the same length")

    # Dict[Tuple[uuid, uuid], count]]
    # - dictionary of key sparse matrix
    # - Each pair(i,j) refers to ">"
    if dok_all is None:
        dok_all = {}
    if dok_direct is None:
        dok_direct = {}
    if dok_best is None:
        dok_best = {}
    if dok_worst is None:
        dok_worst = {}

    # find `best` and `worst` py index
    # (this is 2-3x faster than a loop with if-else)
    # If no element has the state `1` and `2`, then skip
    try:
        best_idx = combostates.index(1)
        worst_idx = combostates.index(2)
    except ValueError:
        return dok_all, dok_direct, dok_best, dok_worst

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


def extract_pairs_batch(evaluated_combostates, mapped_sent_ids):
    """Loop over an batch of BWS sets

    Example:
    -------
        from bwsample import extract_pairs, to_scipy
        mapped_sent_ids = (['id1', 'id2', 'id3', 'id4'],
                           ['id4', 'id5', 'id6', 'id1'])
        evaluated_combostates = ([0, 0, 2, 1], [0, 1, 0, 2])
        dok_all, dok_direct, dok_best, dok_worst = extract_pairs_batch(
            mapped_sent_ids, evaluated_combostates)
        cnts_all, indicies = to_scipy(dok_all)
        cnts_all.todense()
    """
    dok_all, dok_direct, dok_best, dok_worst = {}, {}, {}, {}
    for combostates, stateids in zip(*(evaluated_combostates,
                                       mapped_sent_ids)):
        dok_all, dok_direct, dok_best, dok_worst = extract_pairs(
            stateids, combostates, dok_all=dok_all, dok_direct=dok_direct,
            dok_best=dok_best, dok_worst=dok_worst)
    return dok_all, dok_direct, dok_best, dok_worst


def extract_pairs_batch2(data):
    """Loop over an batch of BWS sets

    Example:
    -------
        from bwsample import extract_pairs_batch, to_scipy
        data = (
            ([0, 0, 2, 1], ['id1', 'id2', 'id3', 'id4']),
            ([0, 1, 0, 2], ['id4', 'id5', 'id6', 'id1']) )
        dok_all, dok_direct, dok_best, dok_worst = extract_pairs_batch2(data)

        cnts_all, indicies = to_scipy(dok_all)
        cnts_all.todense()
    """
    dok_all, dok_direct, dok_best, dok_worst = {}, {}, {}, {}
    for combostates, stateids in data:
        dok_all, dok_direct, dok_best, dok_worst = extract_pairs(
            stateids, combostates, dok_all=dok_all, dok_direct=dok_direct,
            dok_best=dok_best, dok_worst=dok_worst)
    return dok_all, dok_direct, dok_best, dok_worst
