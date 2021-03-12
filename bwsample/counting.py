from typing import List, Optional



def count(evaluations: list, 
          direct_dok: dict = None,
          direct_detail: dict = None,
          use_logical: bool = True,
          logical_dok: dict = None,
          logical_detail: dict = None,
          logical_database: list = None,
          ) -> dict:
    """
    `direct_...` directly extract from 1 BWS set
    `logical_...` logical inference from 2 BWS sets
    """
    # extract from each BWS set
    direct_dok, direct_detail = direct_extract_batch(
        evaluations, dok=direct_dok, details=direct_detail)

    # search for logical inferences
    if use_logical:
        dok_infer = logical_infer_update(
            evaluations, database=logical_database,
            dok=logical_dok, detail=logical_detail)
    
    # add to dok_agg
    for key, val in dok_infer.items():
        dok_all[key] = val + dok_all.get(key, 0)

    # done
    return dok_agg, direct_dok, direct_detail, logical_dok, logical_detail


def logical_infer_update(evaluations, 
                         database=None,   # db_infer
                         dok=None,   # dok_infer
                         detail=None
                        ):
    # Create DoK
    if dok_infer is None:
        dok_infer = {}
    # Create new database
    if db_infer is None:
        db_infer = list(evaluations)

    # start searching for logical inferences
    for states1, ids1 in evaluations:
        for states2, ids2 in db_infer:
            dok_infer = logical_infer(
                ids1, ids2, states1, states2, dok=dok_infer)
    # done
    return dok_infer


def direct_extract(stateids: List[str],
                   combostates: List[int],
                   dok: Optional[dict] = None,
                   dok_bw: Optional[dict] = None,
                   dok_bn: Optional[dict] = None,
                   dok_nw: Optional[dict] = None) -> (
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
            - 0: NOT, unselected (initial state)
            - 1: BEST
            - 2: WORST
        (see TR-225)

    dok: Optional[dict]
        Existing `dok` dictionary that is updated here. see below.

    dok_bw: Optional[dict]
        Existing `dok_bw` dictionary that is updated here. see below.

    dok_bn: Optional[dict]
        Existing `dok_bn` dictionary that is updated here. see below.

    dok_nw: Optional[dict]
        Existing `dok_nw` dictionary that is updated here. see below.

    Returns:
    --------
    dok: dict
        Dictionary with counts for each ">" pair, e.g. an
          entry `{..., ('B', 'C'): 1, ...} means `B>C` was counted `1` times.
        We can extract 3 types of pairs from 1 BWS set:
          - "BEST > WORST" (see dok_bw)
          - "BEST > NOT" (see dok_bn)
          - "NOT > WORST" (see dok_nw)
        The `dok` dictionary contains the aggregate counts of the types
          of pairs. Use `dok_bw`, `dok_bn` and `dok_nw` for
          attribution analysis.

    dok_bw: dict
        Dictionary with counts for explicit "BEST > WORST" pairs.

    dok_bn: dict
        Dictionary with counts for "BEST > NOT" pairs.

    dok_nw: dict
        Dictionary with counts for "NOT > WORST" pairs.

    Examples:
    ---------
        import bwsample as bws

        # First BWS set
        stateids = ['A', 'B', 'C', 'D']
        combostates = [0, 0, 2, 1]  # BEST=1, WORST=2
        dok, dok_bw, dok_bn, dok_nw = bws.counting.direct_extract(
            stateids, combostates)

        # Update dictionary by processing the next BWS set
        stateids = ['D', 'E', 'F', 'A']
        combostates = [0, 1, 0, 2]
        dok, dok_bw, dok_bn, dok_nw = bws.counting.direct_extract(
            stateids, combostates, dok=dok, dok_bw=dok_bw,
            dok_bn=dok_bn, dok_nw=dok_nw)
    """
    if len(stateids) != len(combostates):
        raise Exception("IDs and states lists must have the same length")

    # Dict[Tuple[uuid, uuid], count]]
    # - dictionary of key sparse matrix
    # - Each pair(i,j) refers to ">"
    if dok is None:
        dok = {}
    if dok_bw is None:
        dok_bw = {}
    if dok_bn is None:
        dok_bn = {}
    if dok_nw is None:
        dok_nw = {}

    # find `best` and `worst` py index
    # (this is 2-3x faster than a loop with if-else)
    # If no element has the state `1` and `2`, then skip
    try:
        best_idx = combostates.index(1)
        worst_idx = combostates.index(2)
    except ValueError:
        return dok, dok_bw, dok_bn, dok_nw

    # add the direct "BEST > WORST" observation
    best_uuid = stateids[best_idx]
    worst_uuid = stateids[worst_idx]

    idxpair = (best_uuid, worst_uuid)
    dok[idxpair] = 1 + dok.get(idxpair, 0)
    dok_bw[idxpair] = 1 + dok_bw.get(idxpair, 0)

    # loop over all other elements
    for middle_idx, middle_uuid in enumerate(stateids):
        if middle_idx not in (best_idx, worst_idx):
            # add `BEST > NOT`
            idxpair = (best_uuid, middle_uuid)
            dok[idxpair] = 1 + dok.get(idxpair, 0)
            dok_bn[idxpair] = 1 + dok_bn.get(idxpair, 0)

            # add `NOT > WORST`
            idxpair = (middle_uuid, worst_uuid)
            dok[idxpair] = 1 + dok.get(idxpair, 0)
            dok_nw[idxpair] = 1 + dok_nw.get(idxpair, 0)

    # done
    return dok, dok_bw, dok_bn, dok_nw


def direct_extract_batch(evaluations, 
                         dok=None,   # dok_all
                         detail=None   # {dok_direct, dok_best, dok_worst}
                        ):
    """Loop over an batch of BWS sets

    Example:
    -------
        import bwsample as bws
        evaluations = (
            ([0, 0, 2, 1], ['id1', 'id2', 'id3', 'id4']),
            ([0, 1, 0, 2], ['id4', 'id5', 'id6', 'id1']) )
        dok, detail = bws.counting.direct_extract_batch(evaluations)

        cnts, indicies = bws.to_scipy(dok)
        cnts.todense()
    
    Example 2:
    ----------
        evaluated_combostates = ([0, 0, 2, 1], [0, 1, 0, 2])
        mapped_sent_ids = (['id1', 'id2', 'id3', 'id4'],
                           ['id4', 'id5', 'id6', 'id1'])
        evaluations = zip(*(evaluated_combostates, mapped_sent_ids))
    """
    # intialize empty dict objects
    if dok is None:
        dok = {}
    if detail is None:
        detail, dok_bw, dok_bn, dok_nw = {}, {}, {}, {}

    # query `detail` object
    dok_bw = detail.get("bw", {})
    dok_bn = detail.get("bn", {})
    dok_nw = detail.get("nw", {})

    # loop over all evaluated BWS sets, and post-process each
    for combostates, stateids in evaluations:
        dok, dok_bw, dok_bn, dok_nw = direct_extract(
            stateids, combostates, dok=dok,
            dok_bw=dok_bw, dok_bn=dok_bn, dok_nw=dok_nw)

    # copy details
    detail["bw"] = dok_bw
    detail["bn"] = dok_bn
    detail["nw"] = dok_nw

    # done
    return dok, detail


def find_by_state(ids, states, s_):
    return [i for i, s in zip(*(ids, states)) if s in s_]


def logical_rules(ids1, ids2, states1, states2, s1, s2, dok=None):
    if dok is None:
        dok = {}

    if s1 == 0:  # 0:NOT
        if s2 == 0:  # 0:NOT
            # mm: D>Z
            for i in find_by_state(ids1, states1, [1]):
                for j in find_by_state(ids2, states2, [2]):
                    dok[(i, j)] = 1 + dok.get((i, j), 0)
            # mm: X>F
            for i in find_by_state(ids2, states2, [1]):
                for j in find_by_state(ids1, states1, [2]):
                    dok[(i, j)] = 1 + dok.get((i, j), 0)

        elif s2 == 1:  # 1:BEST
            # mb: D>Y, D>Z
            for i in find_by_state(ids1, states1, [1]):
                for j in find_by_state(ids2, states2, [0, 2]):
                    dok[(i, j)] = 1 + dok.get((i, j), 0)

        elif s2 == 2:  # 2:WORST
            # mw: X>F, Y>F
            for j in find_by_state(ids1, states1, [2]):
                for i in find_by_state(ids2, states2, [0, 1]):
                    dok[(i, j)] = 1 + dok.get((i, j), 0)

    elif s1 == 1:  # 1:BEST
        if s2 == 0:
            # bm: X>E, X>F
            for i in find_by_state(ids2, states2, [1]):
                for j in find_by_state(ids1, states1, [0, 2]):
                    dok[(i, j)] = 1 + dok.get((i, j), 0)

        elif s2 == 2:
            # bw: X>E, X>F, Y>E, Y>F
            for j in find_by_state(ids1, states1, [0, 2]):
                for i in find_by_state(ids2, states2, [0, 1]):
                    dok[(i, j)] = 1 + dok.get((i, j), 0)

    elif s1 == 2:  # 2:WORST
        if s2 == 0:
            # wm: D>Z, E>Z
            for i in find_by_state(ids1, states1, [0, 1]):
                for j in find_by_state(ids2, states2, [2]):
                    dok[(i, j)] = 1 + dok.get((i, j), 0)

        elif s2 == 1:
            # wb: D>Y, D>Z, E>Y, E>Z
            for i in find_by_state(ids1, states1, [0, 1]):
                for j in find_by_state(ids2, states2, [0, 2]):
                    dok[(i, j)] = 1 + dok.get((i, j), 0)
    # done
    return dok


def logical_infer(ids1, ids2, states1, states2, dok=None):
    if dok is None:
        dok = {}
    # find common IDs, and loop over them
    for uid in set(ids1).intersection(ids2):
        try:
            # find positions of the ID
            p1, p2 = ids1.index(uid), ids2.index(uid)
            # lookup states of the ID
            s1, s2 = states1[p1], states2[p2]
            # apply rules
            dok = logical_rules(ids1, ids2, states1, states2, s1, s2, dok=dok)
        except ValueError as err:
            print(err)
            continue
    return dok
