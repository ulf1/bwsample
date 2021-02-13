import numpy as np
import scipy.stats
import scipy.sparse


def scale_simple(cnt):
    """simple ratios (Ni - Nj)/(Nj + Ni)
    - Problem: Ignores different total number of observations
    """
    ratios = (cnt - cnt.T) / (cnt + cnt.T)
    ratios = np.nan_to_num(ratios)
    return ratios


def scale_pvalues(cnt):
    """Compute p-value of the Chi-Squared test for the two frequencies (i,j)
        and (j,i). Assign the p-value to (i,j) and (1-pval) to (j,i)
    """
    n, _ = cnt.shape
    P = scipy.sparse.dok_matrix((n, n), dtype=np.float64)
    for i in range(n):
        for j in range(n):
            if i > j:
                f1, f2 = cnt[i, j], cnt[j, i]
                fe = (f1 + f2) / 2
                if fe > 0:
                    _, pval = scipy.stats.chisquare(
                        f_obs=[f1, f2], f_exp=[fe, fe], ddof=0)
                    P[i, j], P[j, i] = pval, 1 - pval
    return P
