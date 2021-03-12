import bwsample as bws


def test1():
    arrs = [[1, 2, 3], [4, 5, 6]]
    out = bws.sampling.shuffle_subarrs(arrs)
    for i in range(len(out)):
        for v in out[i]:
            assert v in arrs[i]


def test2():
    arrs = [[1, 2, 3], [4, 5, 6]]
    n_items = 3
    n_sets = 2
    out = bws.sampling.shuffle_subarrs(arrs, n_sets, n_items)
    for i in range(len(out)):
        for v in out[i]:
            assert v in arrs[i]
