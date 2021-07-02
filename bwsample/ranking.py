from typing import List, Dict, Tuple, Optional
from .utils import to_scipy
from .utils import adjustscore
from .utils import minmax
import numpy as np
import scipy.sparse
import scipy.sparse.linalg
import scipy.linalg
import scipy.stats
import warnings


def rank(dok: Dict[Tuple[str, str], int],
         method: Optional[str] = 'ratio',
         adjust: Optional[str] = None,
         **kwargs) -> (np.array, np.array, np.array, dict):
    """Rank items based on pairwise comparison frequencies

    Parameters:
    -----------
    dok : Dict[Tuple[str, str], int]
        Count/Frequency data as Dictionary of Keys (DoK)

    method : Optional[str]
        The procedure to compute ranks and scores.
        - 'ratio'
        - 'pvalue'
        - 'approx'
        - 'btl'
        - 'eigen'
        - 'trans'

    Returns:
    --------
    positions : np.array[uint64]
        The array positions to order/sort the original data by indexing.

    sortedids : np.array[any]
        The reordered item IDs

    metrics : np.array[float]
        The metric for each item ID. Also sorted in descending order.

    scores : np.array[float]
        Scaled or calibrated metrics (Default: The `metrics` if `adjust=None`)

    info : dict
        Further information depending on the selected `method`

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
        agg_dok, _, _, _, _ = bws.count(evaluations)
        positions, sortedids, metrics, info = bws.rank(
            agg_dok, method='ratio', avg='exist', adjust='ordinal')
    """
    # convert to sparse matrix
    cnt, indices = to_scipy(dok)

    # compute the rankings
    if method in ('ratio'):
        positions, sortedids, metrics, info = maximize_ratio(
            cnt, indices, **kwargs)
    elif method in ('pvalue'):
        warnings.warn("Use 'approx' because it's faster.", UserWarning)
        positions, sortedids, metrics, info = maximize_minuspvalue(
            cnt, indices, **kwargs)
    elif method in ('approx', 'hoaglin'):
        positions, sortedids, metrics, info = maximize_hoaglinapprox(
            cnt, indices, **kwargs)
    elif method in ('btl', 'hunter'):
        positions, sortedids, metrics, info = bradley_terry_probability(
            cnt, indices, **kwargs)
    elif method in ('eigen', 'saaty'):
        positions, sortedids, metrics, info = eigenvector_estimation(
            cnt, indices)
    elif method in ('trans'):
        positions, sortedids, metrics, info = transition_simulation(
            cnt, indices, **kwargs)
    else:
        raise Exception(f"method='{method}' not available.")

    # adjust scores
    if adjust is not None:
        cut = np.median(metrics)
        labels = [x >= cut for x in metrics]
        scores = adjustscore(metrics, method=adjust, labels=labels)
    else:
        scores = metrics.copy()

    # done
    return positions, sortedids, metrics, scores, info


def maximize_ratio(cnt: scipy.sparse.csr_matrix,
                   indices: List[str],
                   avg: Optional[str] = 'exist'):
    """Rank items based simple ratios, and calibrate row sums as scores

    Parameters:
    -----------
    cnt : scipy.sparse.dok.dok_matrix
        Quadratic sparse matrix with frequency data

    indices : List[str]
        Identifiers, e.g. UUID4, of each row/column of the `cnt` matrix.

    avg : Optional[str] = 'exists'
        How to compute denominator for averaging.
        - 'all': divide the sum of ratios by the row length
        - 'exist': divide the sum of ratios by the number of ratios in the row

    Returns:
    --------
    positions : np.array[uint64]
        The array positions to order/sort the original data by indexing.

    sortedids : np.array[any]
        The reordered item IDs

    metrics : np.array[float]
        The metric for each item ID. Also sorted in descending order.

    info : dict
        Further information depending on the selected `method`

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
        agg_dok, _, _, _, _ = bws.count(evaluations)
        positions, sortedids, metrics, info = bws.rank(
            agg_dok, method='ratio', avg='exist')
    """
    # compute ratios
    cnt = cnt.tocsr()
    ratios = cnt + cnt.T
    ratios.data = 1.0 / ratios.data
    ratios = ratios.multiply(cnt)

    # sum rows in DoK matrix
    metrics = np.array(ratios.sum(axis=1).flatten())[0]
    # averaging
    if avg == 'all':
        metrics /= len(metrics)
    elif avg == 'exist':
        ridx, _ = (ratios + ratios.T).nonzero()  # ensure actual 0s are counted
        for i, c in zip(*np.unique(ridx, return_counts=True)):
            metrics[i] /= c

    # sort, larger row sums are better
    positions = np.argsort(-metrics)  # maximize
    sortedids = np.array(indices)[positions]
    metrics = metrics[positions]

    # informations
    info = {}

    # done
    return positions, sortedids, metrics, info


def maximize_minuspvalue(cnt: scipy.sparse.csr_matrix,
                         indices: List[str],
                         avg: Optional[str] = 'exist'):
    """Rank based on p-values of a Chi-Squard tests between reciprocal pairs,
        and calibrate row sums as scores

    Parameters:
    -----------
    cnt : scipy.sparse.dok.dok_matrix
        Quadratic sparse matrix with frequency data

    indices : List[str]
        Identifiers, e.g. UUID4, of each row/column of the `cnt` matrix.

    avg : Optional[str]
        How to compute denominator for averaging.
        - 'all': divide the sum of ratios by the row length
        - 'exist': divide the sum of ratios by the number of ratios in the row

    Returns:
    --------
    positions : np.array[uint64]
        The array positions to order/sort the original data by indexing.

    sortedids : np.array[any]
        The reordered item IDs

    metrics : np.array[float]
        The metric for each item ID. Also sorted in descending order.

    info : dict
        Further information depending on the selected `method`, e.g.
        - "P": The matrix with the `1-p`-values

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
        agg_dok, _, _, _, _ = bws.count(evaluations)
        positions, sortedids, metrics, info = bws.rank(
            agg_dok, method='pvalue', avg='exist')
    """
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

    # sum rows in DoK matrix
    metrics = np.array(P.sum(axis=1).flatten())[0]
    # averaging
    if avg == 'all':
        metrics /= len(metrics)
    elif avg == 'exist':
        ridx, _ = (P + P.T).nonzero()  # ensure actual 0s are counted
        for i, c in zip(*np.unique(ridx, return_counts=True)):
            metrics[i] /= c

    # sort, larger row sums are better
    positions = np.argsort(-metrics)  # minimize P, maximize 1-P
    sortedids = np.array(indices)[positions]
    metrics = metrics[positions]

    # informations
    info = {}
    info["P"] = P

    # done
    return positions, sortedids, metrics, info


def maximize_hoaglinapprox(cnt: scipy.sparse.csr_matrix,
                           indices: List[str],
                           avg: Optional[str] = 'exist'):
    """Rank based on p-values computed with the Hoaglin Approximation of DoF=0

    Parameters:
    -----------
    cnt : scipy.sparse.dok.dok_matrix
        Quadratic sparse matrix with frequency data

    indices : List[str]
        Identifiers, e.g. UUID4, of each row/column of the `cnt` matrix.

    avg : Optional[str]
        How to compute denominator for averaging.
        - 'all': divide the sum of ratios by the row length
        - 'exist': divide the sum of ratios by the number of ratios in the row

    Returns:
    --------
    positions : np.array[uint64]
        The array positions to order/sort the original data by indexing.

    sortedids : np.array[any]
        The reordered item IDs

    metrics : np.array[float]
        The metric for each item ID. Also sorted in descending order.

    info : dict
        Further information depending on the selected `method`, e.g.
        - "P": The matrix with the `1-p`-values

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
        agg_dok, _, _, _, _ = bws.count(evaluations)
        positions, sortedids, metrics, info = bws.rank(
            agg_dok, method='approx', avg='exist')
    """
    # compute Expected E
    cnt = cnt.tocsr()
    E = cnt + cnt.T
    E.data = E.data / 2.0
    # compute X^2
    X2 = cnt - E
    X2.data = (X2.data)**2
    E.data = 1.0 / E.data
    X2 = X2.multiply(E)
    # compute Hoaglin's Approximation for DoF=0
    P = np.sqrt(X2)
    P.data = np.power(0.1, (P.data + 1.37266) / 2.13161)
    # P.data = P.data * 4.405087805849058
    P.data = np.maximum(0.0, np.minimum(1.0, P.data))
    # only if Nij>Nji
    P = P.multiply(cnt > cnt.T)
    # Q = 1-P
    P.data = 1. - P.data

    # sum rows in DoK matrix
    metrics = np.array(P.sum(axis=1).flatten())[0]
    # averaging
    if avg == 'all':
        metrics /= len(metrics)
    elif avg == 'exist':
        ridx, _ = (P + P.T).nonzero()  # ensure actual 0s are counted
        for i, c in zip(*np.unique(ridx, return_counts=True)):
            metrics[i] /= c

    # sort, larger row sums are better
    positions = np.argsort(-metrics)  # minimize P, maximize 1-P
    sortedids = np.array(indices)[positions]
    metrics = metrics[positions]

    # informations
    info = {}
    info["P"] = P

    # done
    return positions, sortedids, metrics, info


def eigenvector_estimation(cnt: scipy.sparse.csr_matrix,
                           indices: List[str]):
    """Compute the eigenvectors of the pairwise comparison matrix, and
        calibrate eigenvectors as scores.

    Parameters:
    -----------
    cnt : scipy.sparse.dok.dok_matrix
        Quadratic sparse matrix with frequency data

    indices : List[str]
        Identifiers, e.g. UUID4, of each row/column of the `cnt` matrix.

    Returns:
    --------
    positions : np.array[uint64]
        The array positions to order/sort the original data by indexing.

    sortedids : np.array[any]
        The reordered item IDs

    metrics : np.array[float]
        The metric for each item ID. Also sorted in descending order.

    info : dict
        Further information depending on the selected `method`, e.g.
        - "eigval": Estimated eigenvalue
        - "eigenvec": Estimated eigenvector

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
        agg_dok, _, _, _, _ = bws.count(evaluations)
        positions, sortedids, metrics, info = bws.rank(
            agg_dok, method='eigen')

    References:
    -----------
    Saaty, T.L., 2003. Decision-making with the AHP: Why is the principal
        eigenvector necessary. European Journal of Operational Research 145,
        85–91. https://doi.org/10.1016/S0377-2217(02)00227-8
    """
    # set diagonals to 1
    n = cnt.shape[0]
    cnt = cnt.tolil()
    for i in range(n):
        cnt[i, i] = 1

    # Compute a sparse "positive reciprocal near consistent pairwise
    #   comparison matrix". Avoid accidental conversion into dense matrix
    #   by manipulating the value/data vector of the transposed sp matrix.
    cnt = cnt.tocsr()
    cntT = cnt.T
    cntT.data = 1.0 / cntT.data
    ratios = cnt.multiply(cntT)

    # compute eigenvectors as scores
    eigval, eigenvec = scipy.sparse.linalg.eigs(ratios, k=1)
    metrics = np.abs(np.real(eigenvec[:, 0]))

    # sort, larger row sums are better
    positions = np.argsort(-metrics)  # maximize
    sortedids = np.array(indices)[positions]
    metrics = metrics[positions]

    # informations
    info = {}
    info["eigval"] = eigval
    info["eigenvec"] = eigenvec

    # done
    return positions, sortedids, metrics, info


def transition_simulation(cnt: scipy.sparse.dok.dok_matrix,
                          indices: List[str],
                          n_rounds: Optional[int] = 2):
    """Estimate transition matrix of item_i>item_j, simulate the item
        probabilities that are calibrated to scores.

    Parameters:
    -----------
    cnt : scipy.sparse.dok.dok_matrix
        Quadratic sparse matrix with frequency data

    indices : List[str]
        Identifiers, e.g. UUID4, of each row/column of the `cnt` matrix.

    n_rounds: Optional[int] = 2
        Number of steps/rounds to simulate

    Returns:
    --------
    positions : np.array[uint64]
        The array positions to order/sort the original data by indexing.

    sortedids : np.array[any]
        The reordered item IDs

    metrics : np.array[float]
        The metric for each item ID. Also sorted in descending order.

    info : dict
        Further information depending on the selected `method`, e.g.
        - "sim": The predicted/simulated item probability
        - "transmat: The estimated transition probability matrix.

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
        agg_dok, _, _, _, _ = bws.count(evaluations)
        positions, sortedids, metrics, info = bws.rank(
            agg_dok, method='trans', n_rounds=3)
    """
    n = cnt.shape[0]

    # create generator matrix
    genmat = cnt.T.tolil()
    rowsum = genmat.sum(axis=1)
    for i in range(n):
        genmat[i, i] = -rowsum[i]  # set diagonals to -sum(row)
        genmat[i, :] /= max(1, rowsum[i])

    # compute transition matrix
    transmat = scipy.sparse.linalg.expm(genmat.tocsc())

    # simulation: transition from an item1 to the next item2
    #   that is most likely "item2 > item1"
    x = np.ones(n) / n
    for i in range(n_rounds):
        x = x * transmat

    # sort, larger state probabilities are better
    positions = np.argsort(-x)  # maximize
    sortedids = np.array(indices)[positions]
    metrics = x[positions]

    # informations
    info = {}
    info["sim"] = x
    info["transmat"] = transmat

    # done
    return positions, sortedids, metrics, info


def mle_btl_sparse(cnt: scipy.sparse.csr_matrix,
                   x0: Optional[np.array] = None,
                   max_iter: Optional[int] = 50,
                   tol: Optional[float] = 1e-5) -> (np.array, bool):
    """MLE by Hunter (2004, p.386-387)

    Parameters:
    -----------
    cnt : scipy.sparse.dok.dok_matrix
        Quadratic sparse matrix with frequency data

    x0 : np.array
        Initial values.

    max_iter : int
        maximum number of iterations

    tol : float
        termination criteria

    Returns:
    --------
    gamma : np.array
        Estimated gamma parameters. SUM[gammas]=1. The estimated
          parameters can be used as scores

    flag : bool
        True if solution was found within `max_iter` optimization steps.
        False if not.

    References:
    -----------
    Hunter, D.R., 2004. MM algorithms for generalized Bradley-Terry models. The
      Annals of Statistics 32, 384–406. https://doi.org/10.1214/aos/1079120141
    """
    # ensure CSR format
    cnt = cnt.tocsr()
    m = cnt.shape[0]

    # set initial values
    if x0 is None:
        x = np.ones(m) / m
    else:
        x = np.array(x0)
        x = x / x.sum()

    # rowsum, i.e. the number of wins `W_i`
    rowsum = cnt.sum(axis=1)

    # count zero rows
    zrow = m - (cnt > 0).sum(axis=1)

    # add `Nij + Nji`
    cntij = (cnt + cnt.T)
    # pseudo inverse `[(Nij + Nji) / (yi + yj)]^{-1}`
    cntij.data = 1 / cntij.data

    # copy sparse structure for `yi + yj`
    gamij = cntij.copy()
    ridx, cidx = gamij.nonzero()

    for k in range(max_iter):
        # assign new weights
        gamij[(ridx, cidx)] = x[ridx] + x[cidx]

        # don't forget to use the inverse:
        tmp = gamij.multiply(cntij)

        # sum up rows, and elementwise multiply
        gamk = np.multiply(rowsum, zrow + tmp.sum(axis=1))

        # normalize to `gam_i^(k)`
        x1 = gamk / gamk.sum(axis=0)

        # abort
        if np.linalg.norm(x1 - x, ord=np.inf) < tol:
            return np.array(x1.flatten())[0], True

        # update
        x = x1

    # last result
    return np.array(x1.flatten())[0], False


def bradley_terry_probability(cnt: scipy.sparse.csr_matrix,
                              indices: List[str],
                              prefit: Optional[bool] = True,
                              max_iter: Optional[int] = 50,
                              tol: Optional[float] = 1e-5):
    """Bradley-Terry-Luce (BTL) probability model for pairwise comparisons

    Parameters:
    -----------
    cnt : scipy.sparse.dok.dok_matrix
        Quadratic sparse matrix with frequency data

    indices : List[str]
        Identifiers, e.g. UUID4, of each row/column of the `cnt` matrix.

    prefit : bool
        flag to prefit parameters with 'ratio' method
        (see `ranking_maximize_ratios`)

    max_iter : int  (see `mle_btl_sparse`)
        maximum number of iterations

    tol : float  (see `mle_btl_sparse`)
        termination criteria

    Returns:
    --------
    positions : np.array[uint64]
        The array positions to order/sort the original data by indexing.

    sortedids : np.array[any]
        The reordered item IDs

    metrics : np.array[float]
        The metric for each item ID. Also sorted in descending order.

    info : dict
        Further information depending on the selected `method`, e.g.
        - "weights": The estimated MLE parameters that can be used for scoring

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
        agg_dok, _, _, _, _ = bws.count(evaluations)
        positions, sortedids, metrics, info = bws.rank(
            agg_dok, method='btl', prefit=True, max_iter=100, tol=1e-5)
    """
    cnt = cnt.tocsr()
    x0 = None
    if prefit:
        ratios = cnt + cnt.T
        ratios.data = 1.0 / ratios.data
        ratios = ratios.multiply(cnt)
        x0 = np.array(ratios.sum(axis=1).flatten())[0]
        x0 = minmax(x0)

    # estimate Bradley-Terry-Luce model parameters as metric
    x, flag = mle_btl_sparse(cnt, x0=x0, max_iter=max_iter, tol=tol)

    # sort, larger state probabilities are better
    positions = np.argsort(-x)  # maximize
    sortedids = np.array(indices)[positions]
    metrics = x[positions]

    # informations
    info = {}
    info["weights"] = x

    # done
    return positions, sortedids, metrics, info
