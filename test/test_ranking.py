import bwsample as bws


def test1():
    # demo data
    data = (
        ([1, 0, 0, 2], ['A', 'B', 'C', 'D']),
        ([1, 0, 0, 2], ['A', 'B', 'C', 'D']),
        ([2, 0, 0, 1], ['A', 'B', 'C', 'D']),
        ([0, 1, 2, 0], ['A', 'B', 'C', 'D']),
        ([0, 1, 0, 2], ['A', 'B', 'C', 'D']),
    )
    dok, _, _, _ = bws.extract_pairs_batch2(data)

    # possible settings
    settings = [
        {"method": "ratio", "avg": "all", "calibration": "platt"},
        {"method": "ratio", "avg": "exist", "calibration": "platt"},
        {"method": "ratio", "avg": "all", "calibration": "isotonic"},
        {"method": "ratio", "avg": "exist", "calibration": "isotonic"},
        {"method": "ratio", "avg": "all", "calibration": "minmax"},
        {"method": "ratio", "avg": "exist", "calibration": "minmax"},
        {"method": "pvalue", "avg": "all", "calibration": "platt"},
        {"method": "pvalue", "avg": "exist", "calibration": "platt"},
        {"method": "pvalue", "avg": "all", "calibration": "isotonic"},
        {"method": "pvalue", "avg": "exist", "calibration": "isotonic"},
        {"method": "pvalue", "avg": "all", "calibration": "minmax"},
        {"method": "pvalue", "avg": "exist", "calibration": "minmax"},
        {"method": "eigen", "calibration": "platt"},
        {"method": "eigen", "calibration": "isotonic"},
        {"method": "eigen", "calibration": "minmax"},
        {"method": "transition", "calibration": "platt"},
        {"method": "transition", "calibration": "isotonic"},
        {"method": "transition", "calibration": "minmax"}
    ]

    # loop over each setting
    for setting in settings:
        ranked, ordids, scores, _ = bws.rank(dok, **setting)
        assert len(ranked) == 4
        assert len(ordids) == 4
        assert len(scores) == 4
