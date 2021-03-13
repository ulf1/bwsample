import bwsample as bws


def test1():
    # demo data
    evaluations = (
        ([1, 0, 0, 2], ['A', 'B', 'C', 'D']),
        ([1, 0, 0, 2], ['A', 'B', 'C', 'D']),
        ([2, 0, 0, 1], ['A', 'B', 'C', 'D']),
        ([0, 1, 2, 0], ['A', 'B', 'C', 'D']),
        ([0, 1, 0, 2], ['A', 'B', 'C', 'D']),
    )
    dok, _, _, _, _ = bws.count(evaluations)

    # possible settings
    settings = [
        {"method": "ratio", "avg": "all", "adjust": "platt"},
        {"method": "ratio", "avg": "exist", "adjust": "platt"},
        {"method": "ratio", "avg": "all", "adjust": "quantile"},
        {"method": "ratio", "avg": "exist", "adjust": "quantile"},
        {"method": "ratio", "avg": "all", "adjust": "sig3iqr"},
        {"method": "ratio", "avg": "exist", "adjust": "sig3iqr"},
        {"method": "pvalue", "avg": "all", "adjust": "platt"},
        {"method": "pvalue", "avg": "exist", "adjust": "platt"},
        {"method": "pvalue", "avg": "all", "adjust": "quantile"},
        {"method": "pvalue", "avg": "exist", "adjust": "quantile"},
        {"method": "pvalue", "avg": "all", "adjust": "sig3iqr"},
        {"method": "pvalue", "avg": "exist", "adjust": "sig3iqr"},
        {"method": "btl", "adjust": "platt"},
        {"method": "btl", "adjust": "quantile"},
        {"method": "btl", "adjust": "sig3iqr"},
        {"method": "eigen", "adjust": "platt"},
        {"method": "eigen", "adjust": "quantile"},
        {"method": "eigen", "adjust": "sig3iqr"},
        {"method": "trans", "adjust": "platt"},
        {"method": "trans", "adjust": "quantile"},
        {"method": "trans", "adjust": "sig3iqr"}
    ]

    # loop over each setting
    for setting in settings:
        positions, sortedids, metrics, scores, info = bws.rank(dok, **setting)
        assert len(positions) == 4
        assert len(sortedids) == 4
        assert len(metrics) == 4
        assert len(scores) == 4
