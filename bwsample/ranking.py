from typing import List
from .utils import to_scipy
import numpy as np
import scipy.sparse
import scipy.linalg
import scipy.stats


def minmax(arr):
    data = np.array(arr)
    xmin = data.min()
    xmax = data.max()
    return (data - xmin) / (xmax - xmin)


def rank(dok, method='pvalue', **kwargs):
    cnt, indices = to_scipy(dok)
    if method in ('ratios'):
        return ranking_maximize_ratios(cnt, indices)
    elif method in ('pvalue'):
        return ranking_minus_pvalues(cnt, indices)
    elif method in ('transition'):
        return ranking_simulate_transition(cnt, indices, **kwargs)
    else:
        raise Exception(f"method='{method}' not availble.")


def ranking_maximize_ratios(cnt: scipy.sparse.csr_matrix,
                            indices: List[str]):
    # compute ratios
    cnt = cnt.tocsr()
    ratios = cnt + cnt.T
    ratios.data = 1.0 / ratios.data
    ratios = ratios.multiply(cnt)
    # ratios = cnt / (cnt + cnt.T)
    # ratios = np.nan_to_num(ratios)

    # sort, larger row sums are better
    rowsum = np.array(ratios.sum(axis=1).flatten())[0]
    ranked = np.argsort(-rowsum)  # maximize
    ordids = np.array(indices)[ranked].tolist()
    scores = minmax(rowsum[ranked]).tolist()
    # ranked, ordids, rowsum = get_rank(-ratios, indices)
    # scores = minmax(-rowsum)

    # done
    return ranked.tolist(), ordids, scores, ratios


def ranking_minus_pvalues(cnt, indices):
    # compute p-values for Nij>Nji or 1
    n, _ = cnt.shape
    P = scipy.sparse.dok_matrix((n, n), dtype=np.float64)
    for i in range(n):
        for j in range(n):
            if i > j:
                f1, f2 = cnt[i, j], cnt[j, i]
                fe = (f1 + f2) / 2  # E: Expected Frequency
                if fe > 0 and f1 != f2:
                    _, pval = scipy.stats.chisquare(
                        f_obs=[f1, f2], f_exp=[fe, fe], ddof=0)
                    if f1 > f2:
                        P[i, j] = 1 - pval
                    else:
                        P[j, i] = 1 - pval

    # sort, larger row sums are better
    rowsum = np.array(P.sum(axis=1).flatten())[0]  # sum rows in DoK matrix
    ranked = np.argsort(-rowsum)  # minimize
    ordids = np.array(indices)[ranked].tolist()
    scores = minmax(rowsum[ranked]).tolist()

    # done
    return ranked.tolist(), ordids, scores, P


def ranking_simulate_transition(cnt, indices, n_rounds=3):
    n = cnt.shape[0]

    # create generator matrix
    genmat = cnt.T.tolil()
    rowsum = genmat.sum(axis=1)
    for i in range(n):
        genmat[i, i] = -rowsum[i]  # set diagonals to -sum(row)
        genmat[i, :] /= rowsum[i]

    # compute transition matrix
    transmat = scipy.linalg.expm(genmat.tocsc())

    # simulation: transition from an item1 to the next item2
    #   that is most likely "item2 > item1"
    x = np.ones(n) / n
    for i in range(n_rounds):
        x = x * transmat

    # sort, larger state probabilities are better
    ranked = np.argsort(-x)  # maximize
    ordids = np.array(indices)[ranked].tolist()
    scores = minmax(x[ranked]).tolist()

    # done
    return ranked.tolist(), ordids, scores, (x, transmat)
