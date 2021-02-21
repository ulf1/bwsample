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
 - name: Berlin-Brandenburgische Akademie der Wissenschaften, Berlin, Berlin, Germany
   index: 1
date: 13 February 2021
codeRepository: https://github.com/ulf1/bwsample
license: Apache-2.0
bibliography: paper.bib
---


# Summary
`bwsample` is a [@python3] package that provides algorithms to sample best-worst scaling sets (BWS sets), extract and count pairwise comparisons from user-evaluated BWS sets, and compute ranks and scores.

# Statement of need
We are using the `bwsample` package as part of an *Active Learning* experiment in which linguistics experts and lay people (crowdsourcing) judging sentences examples with the *Best-Worst Scaling* (BWS) method (Fig. \ref{fig:active-learning-process}).
At least two methods or algorithms were implemented for sampling, counting and ranking, so that researchers can run A/B tests.

![Using `bwsample` (`bws`) in an Active Learning experiment.\label{fig:active-learning-process}](https://raw.githubusercontent.com/ulf1/bwsample/master/docs/bwsample-process.png)


## Sampling
The two sampling algorithms are deployed in the REST API for an Web App. 
While the `'twice'` sampling algorithm ensures that *every* item is displayed to an user at least twice (Fig. \ref{fig:sample-twice}), the `'overlap'` algorithm samples the minimal number of items shown twice (Fig. \ref{fig:sample-overlap}).
A possible research questions is: How many items has be show twice to gather a reasonable amount of counting or resp. frequency data?


\twocolumn

![Arrange items (A, B, C, ...) so that BWS sets overlap.\label{fig:sample-overlap}](https://raw.githubusercontent.com/ulf1/bwsample/master/docs/bwsample-overlap.png){ width=49% }

\newpage

![Connect non-overlapping items to further BWS sets so that very item is part of at least two BWS sets.\label{fig:sample-twice}](https://raw.githubusercontent.com/ulf1/bwsample/master/docs/bwsample-twice.png){ width=49% }

\onecolumn


## Counting
The package provide two counting algorithms. First, counting directly extracted pairs from one BWS set (Fig. \ref{fig:bwsample-extract}). Second, counting logical inferred pairs by comparing two BWS sets with an overlapping item (Fig. \ref{fig:bwsample-logical}). 

![Extracting pairwise comparisons from one BWS set.\label{fig:bwsample-extract}](https://raw.githubusercontent.com/ulf1/bwsample/master/docs/bwsample-extract.png){ width=33% }

![The nine combinations to logical infer pairwise comparisons from two BWS sets.\label{fig:bwsample-logical}](https://raw.githubusercontent.com/ulf1/bwsample/master/docs/bwsample-logical.png)


## Ranking and Scoring
For ranking and scoring the package provides three algorithms: Ranking based on simple ratios, ranking based on Chi-Square tests' p-values, or scoring based on the estimated and simulated transition matrix.



# Acknowledgements
This work was funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - [433249742](https://gepris.dfg.de/gepris/projekt/433249742).

# Software Citations
`bwsample` is written in Python 3.6+ [@python3] and uses the following software packages:

- `NumPy` [https://github.com/numpy/numpy](https://github.com/numpy/numpy) [@numpy]
- `SciPy` [https://github.com/scipy/scipy](https://github.com/scipy/scipy) [@scipy]

# References
