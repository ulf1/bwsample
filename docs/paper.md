---
title: "`bwsample`: Sampling and Evaluation of Best-Worst Scaling sets"
tags:
  - Sampling
  - Best-Worst Scaling
  - Pairwise Comparison
  - Dictionary of Keys
  - Open-source
authors:
  - name: Ulf Hamster
    orcid: 0000-0002-0440-4868
    affiliation: "1"
affiliations:
 - name: Berlin-Brandenburgische Akademie der Wissenschaften, Berlin, Germany
   index: 1
date: 13 February 2021
codeRepository: https://github.com/ulf1/bwsample
license: Apache-2.0
bibliography: paper.bib
---


# Summary
`bwsample` is a Python package that provides algorithms to sample best-worst scaling sets (BWS sets), extract and count pairwise comparisons from user-evaluated BWS sets, and compute ranks and scores.

# Statement of need
We are using the `bwsample` package as part of an *Active Learning* experiment in which linguistics experts and lay people (crowdsourcing) are judging sentences examples with the *Best-Worst Scaling* (BWS) method (Fig. \ref{fig:active-learning-process}).
BWS is *"... the cognitive process by which respondents repeatedly choose the two objects in varying sets of three or more objects that they feel exhibit the largest perceptual difference on an underlying continuum of interest"* [@finn1992, pp.13].
In our context, BWS is primarily used as a means of data collection.
At least two methods or algorithms are implemented for sampling, counting and ranking, so that researchers can run A/B tests.

![Using `bwsample` (`bws`) in an Active Learning experiment.\label{fig:active-learning-process}](https://raw.githubusercontent.com/ulf1/bwsample/master/docs/bwsample-process.png)


## Sampling
The two sampling algorithms are deployed in the REST API for an Web App. 
While the `'twice'` sampling algorithm ensures that *every* item is displayed to an user at least twice (Fig. \ref{fig:sample-twice}), the `'overlap'` algorithm samples the minimal number of items shown twice.
A possible research questions is: How many items has be show twice to gather a reasonable amount of counting or resp. frequency data?

![Arrange items $[A, B, C, ...]$ so that BWS sets overlap. Then connect non-overlapping items to further BWS sets so that very item is part of at least two BWS sets.\label{fig:sample-twice}](https://raw.githubusercontent.com/ulf1/bwsample/master/docs/bwsample-twice.png){ width=49% }



## Counting
The package provide two counting algorithms. First, counting directly extracted pairs from one BWS set (Fig. \ref{fig:bwsample-extract}). We can distinct and separately count three cases

- 1 time `BEST>WORST`,
- $N_{items} - 2$ times `BEST>MIDDLE`, and
- $N_{items} - 2$ times `MIDDLE>WORST`.

![Extracting pairwise comparisons from one BWS set.\label{fig:bwsample-extract}](https://raw.githubusercontent.com/ulf1/bwsample/master/docs/bwsample-extract.png){ width=33% }

Second, counting logical inferred pairs by comparing two BWS sets with an overlapping item (Fig. \ref{fig:bwsample-logical}). 
Any newly user-evaluated BWS set needs to be assessed against a database of BWS sets, i.e. the algorithm is $\mathcal{O}(n^2)$ complex.
The benefit is that researcher can compare directly extracted pairs versus logical inferred pairs, e.g. are users consistent with their judgements? 

![The seven cases to logical infer pairwise comparisons from two BWS sets.\label{fig:bwsample-logical}](https://raw.githubusercontent.com/ulf1/bwsample/master/docs/bwsample-logical.png)

The count or resp. frequency data is organized as Dictionary of Keys (DoK) format.
We assume that each item has an unique identifier (e.g. UUID4).
In Python the DoK has the data type `Dict[Tuple[ID,ID],uint]`, 
what is serializable as JSON and storable in key-value databases.
For example, the data `{("id1", "id2"): 345, ("id2", "id1"): 678}` means that relation `id1>id2` was measured 345 times, and the contradicting relation `id2>id1` was counted 678 times.

## Ranking and Scoring
Rank and score items based on pairwise comparison frequencies.

### Simple Ratios
Ranks and scores based on *simple ratios* are computed as follows:

1. Compute all ratios $\mu_{ij} = \frac{N_{ij}}{N_{ij} + N_{ji}} \; \forall i,j$
2. Compute the row sums $s_i = \sum_j \mu_{ij}$
3. Calibrate the values $s_i$ by Platt-Scaling as scores

The *simple ratio* approach ignores the sample sizes $N_{ij} + N_{ji}$
across different pairs $(i,j)$.

### p-value based metric to rank
The question which opposing frequency $N_{ij}$ or $N_{ji}$ is larger,
can be treated as hypothesis test:

$$
\mu = \frac{N_{ij}}{N_{ij} + N_{ji}}
\quad , \quad
H_0: \mu = 0.5
\quad , \quad
H_a: \mu > 0.5
$$

The Pearson's $\chi^2$-test is implemented as alternative to the binomal test with its discrete distribution.

1. Compute *p-value based* metric $x_{ij}$. Using $1-p$ allows to store a sparse matrix as we expect many pairs $(i,j)$ having no user evaluation at all.
$$
x_{ij} = 
\left \{
\begin{aligned}
& 1-p_{ij}, & \text{if} \, N_{ij} > N_{ji} \\
& 0, & \text{otherwise}
\end{aligned} 
\right.
\quad
\forall i,j
$$
2. Sum each row $r_i = \sum_j x_{ij}$ and divide it by the actual number of row elements $n_i$
3. Calibrate the values $r_i/n_i$ by Platt-Scaling as scores



### Eigenvectors as scores
The idea is to solve pairwise comparison matrix as Eigenvalue-problem whereas the eigenvector can be interpreted as the items' scores [@saaty2003].

1. Create a reciprocal pairwise comparison matrix $A=(a_{ij})$ with 
$$
a_{ij} = 
\left \{
\begin{aligned}
& N_{ij} / N_{ji}, & \text{if} \, N_{ji} > 0 \\
& 0, & \text{otherwise}
\end{aligned} 
\right.
\quad
\forall i,j
$$
2. Solve the Eigenvalue-problem $A x = m x$ with $m$ the eigenvalue and $x=[x_1, x_2, ...,x_N]$ the eigenvector,
3. Calibrate the eigenvector $x$ by Platt-Scaling as scores


### Estimate and simulate a transition matrix
Approach:

1. Compute a transition probability matrix $\Pr(k|j)$ of items $e$ being evaluated $e_k > e_j$
2. Simulate the transition matrix
    - The initial items are equally distributed with item probability $\pi_j = 1/N \; \forall j$.
    - Predict the probability of the items $\pi_k = \pi_j \cdot \Pr(k|j)$
3. Calibrate the item probabilities $\pi_k$ to scores. Run Platt-Scaling against binary labels $y=1_{\pi_k>1/N}$


# Acknowledgements
This work was funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - [433249742](https://gepris.dfg.de/gepris/projekt/433249742).

# Software Citations
`bwsample` is written in Python 3.6+ [@python3] and uses the following software packages:

- `NumPy` [https://github.com/numpy/numpy](https://github.com/numpy/numpy) [@numpy]
- `SciPy` [https://github.com/scipy/scipy](https://github.com/scipy/scipy) [@scipy]
- `scikit-learn` [https://github.com/scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) [@scikit-learn] 

# References