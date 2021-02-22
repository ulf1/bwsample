from typing import List
from .utils import to_scipy
import numpy as np
import scipy.sparse
import scipy.sparse.linalg
import scipy.linalg
import scipy.stats
import sklearn.linear_model
import sklearn.isotonic


def minmax(arr: np.array) -> np.array:
    data = np.array(arr)
    xmin = data.min()
    xmax = data.max()
    return (data - xmin) / (xmax - xmin)


def calibrate(scores: np.array, labels: np.array,
              method: str = None) -> np.array:
    """Wrapper function to calibrate scores with its binary labels

    Parameters:
    -----------
    scores: np.array
        The scores generated by a model. It's assumed that these scores
          are probabilities with values between [0,1]. For example, apply
          min-max-scaling for ratio-scale data types (i.e. score>0.0).

    labels: np.array
        The binary labels that are supposed to be classified by the scores.

    method: str (Default: None)
        The calibration algorithm:
            - 'platt' for Platt-Scaling (Platt, 1999)
            - 'isotonic' for Isotonic Regression (Zadrozny and Elkan, 2002)

    Return:
    -------
    calibrated_scores : np.array
        The predicted probabilities

    References:
    -----------
    Platt, J., 1999. Probabilistic outputs for support vector machines and
        comparisons to regularized likelihood methods.
    Zadrozny, B., Elkan, C., 2002. Transforming classifier scores into
        accurate multiclass probability estimates, in: Proceedings of the
        Eighth ACM SIGKDD International Conference on Knowledge Discovery
        and Data Mining, KDD ’02. Association for Computing Machinery,
        New York, NY, USA, pp. 694–699. https://doi.org/10.1145/775047.775151
    """
    scores = np.array(scores)
    labels = np.array(labels)
    if method == 'platt':
        cls = sklearn.linear_model.LogisticRegression()
        cls.fit(X=scores.reshape(-1, 1), y=labels)
        return cls.predict_proba( scores.reshape(-1, 1))[:, 1]
    elif method == 'isotonic':
        cls = sklearn.isotonic.IsotonicRegression(out_of_bounds='raise')
        cls.fit(X=scores, y=labels)
        return cls.transform(scores)
    else:
        return x


def rank(dok, method='pvalue', **kwargs):
    """
    Parameters:
    -----------

    Returns:
    --------

    Example:
    --------

    """
    cnt, indices = to_scipy(dok)
    if method in ('ratios'):
        return ranking_maximize_ratios(cnt, indices, **kwargs)
    elif method in ('pvalue'):
        return ranking_minus_pvalues(cnt, indices, **kwargs)
    elif method in ('eigen'):
        return scoring_eigenvector(cnt, indices, **kwargs)
    elif method in ('transition'):
        return transition_simulation(cnt, indices, **kwargs)
    else:
        raise Exception(f"method='{method}' not available.")


def ranking_maximize_ratios(cnt: scipy.sparse.csr_matrix,
                            indices: List[str],
                            avg: str='exist',
                            calibration: str='platt'):
    """
    Parameters:
    -----------

    Returns:
    --------

    Example:
    --------

    """
    # compute ratios
    cnt = cnt.tocsr()
    ratios = cnt + cnt.T
    ratios.data = 1.0 / ratios.data
    ratios = ratios.multiply(cnt)

    # sum rows in DoK matrix
    metric = np.array(ratios.sum(axis=1).flatten())[0]
    # averaging
    if avg == 'all':
        metric /= len(metric)
    elif avg == 'exist':
        ridx, _ = (ratios + ratios.T).nonzero()  # ensure actual 0s are counted
        for i, c in zip(*np.unique(ridx, return_counts=True)):
            metric[i] /= c

    # sort, larger row sums are better
    ranked = np.argsort(-metric)  # maximize
    ordids = np.array(indices)[ranked].tolist()
    scores = metric[ranked]

    # calibrate scores
    if calibration in ('platt', 'isotonic'):
        labels = scores > np.mean(scores)  # TRUE: s>mean(s)
        scores = calibrate(scores, labels, method=calibration)
    elif calibration == 'minmax':
        scores = minmax(scores)

    # done
    return ranked.tolist(), ordids, scores.tolist(), ratios


def ranking_minus_pvalues(cnt: scipy.sparse.csr_matrix,
                          indices: List[str],
                          avg: str='exist',
                          calibration: str='platt'):
    """
    Parameters:
    -----------

    Returns:
    --------

    Example:
    --------

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
    metric = np.array(P.sum(axis=1).flatten())[0]
    # averaging
    if avg == 'all':
        metric /= len(metric)
    elif avg == 'exist':
        ridx, _ = (P + P.T).nonzero()  # ensure actual 0s are counted
        for i, c in zip(*np.unique(ridx, return_counts=True)):
            metric[i] /= c

    # sort, larger row sums are better
    ranked = np.argsort(-metric)  # minimize
    ordids = np.array(indices)[ranked].tolist()
    scores = metric[ranked]

    # calibrate scores
    if calibration in ('platt', 'isotonic'):
        labels = scores > np.mean(scores)  # TRUE: s>mean(s)
        scores = calibrate(scores, labels, method=calibration)
    elif calibration == 'minmax':
        scores = minmax(scores)

    # done
    return ranked.tolist(), ordids, scores.tolist(), P


def scoring_eigenvector(cnt: scipy.sparse.csr_matrix,
                        indices: List[str],
                        calibration: str=None):
    """
    Parameters:
    -----------
    calibration: str (Default: None)
        The calibrated scores. For 'platt' and 'isotonic' we assume
          `label[i]=eigenvector[i]>0.5`. There is also the option to run
          Min-Max-Scaling (`'minmax'`) but won't recommend using it.

    Returns:
    --------

    Example:
    --------

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

    # compute "positive reciprocal near consistent pairwise comparison matrix"
    cnt = cnt.tocsr()
    cntT = cnt.T
    cntT.data = 1.0 / cntT.data
    ratios = cnt.multiply(cntT)

    # compute eigenvectors as scores
    eigval, eigenvec = scipy.sparse.linalg.eigs(ratios, k=1)
    metric = np.abs(np.real(eigenvec[:, 0]))

    # sort, larger row sums are better
    ranked = np.argsort(-metric)  # maximize
    ordids = np.array(indices)[ranked].tolist()
    scores = metric[ranked]

    # calibrate scores
    if calibration in ('platt', 'isotonic'):
        labels = scores > .5  # TRUE: s>.5
        scores = calibrate(scores, labels, method=calibration)
    elif calibration == 'minmax':
        scores = minmax(scores)

    # done
    return ranked.tolist(), ordids, scores.tolist(), (eigval, eigenvec)


def transition_simulation(cnt, indices, n_rounds=3, calibration: str='platt'):
    """

    Parameters:
    -----------
    calibration: str (Default: 'platt')
        The calibrated scores. We are predicting transition probabilities
          here, i.e. `SUM[transprob]=1`. Thus, we interpret `transprob[i]>1/N`
          as our true binary label for Platt Scaling (`'platt'`) and Isotonic
          Regression (`'isotonic'`). We don't recommend using Min-Max-Scaling 
          (`'minmax'`).

    Returns:
    --------


    Example:
    --------

    """
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
    scores = x[ranked]

    # calibrate scores
    if calibration in ('platt', 'isotonic'):
        labels = scores > 1.0 / len(scores)  # TRUE: s>1/N
        scores = calibrate(scores, labels, method=calibration)
    elif calibration == 'minmax':
        scores = minmax(scores)

    # done
    return ranked.tolist(), ordids, scores.tolist(), (x, transmat)
