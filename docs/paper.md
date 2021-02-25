---
title: "`bwsample`: Sampling and Analysis of Best-Worst Scaling sets"
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

![Using `bwsample` (`bws`) in an Active Learning experiment.\label{fig:active-learning-process}](https://raw.githubusercontent.com/ulf1/bwsample/master/docs/bwsample-process.png)


### Software Feature
The *sampling* algorithms ensure overlapping BWS sets, and are deployed in the REST API for an Web App. Overlaps are required for counting pairs by logical inference (SEE TR-223a REPORT!). A possible question is how many items has to be shown twice a) initially, and b) after the pairs frequency database grew over time to gather reasonable amounts counting or resp. frequency data?

The implemented *counting* algorithms can distinct between 3 types of directly extract pairs, and 7 logical inferred pairs. This opens the opportunity for further analysis, e.g. detect inconsistent evaluations. It also allows comparing results with previous studies [@kiritchenko2016, @kiritchenko2017] that used a subset of extractable pairs, e.g. only pairs with explicitly selected best and worst items [@orme2009].

The implemented algorithms to compute rankings and scores from pairwise comparisons are described in (TR-223b).  
Compare the pairwise frequency matrix with its transposed matrix, e.g. a) by differences [@orme2009], b) by percentage ratio, c) by p-value based metric of Chi-Squared test, and use the row sums to rank and score.
d) Compute eigenvectors as scores [@saaty2003].
e) Estimate and simulate a transition matrix.
f) MLE estimation of the Bradley-Terry-Luce (BTL) probability model [@hunter2004, pp.~386-387].



# Acknowledgements
This work was funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - [433249742](https://gepris.dfg.de/gepris/projekt/433249742).

# Software Citations
`bwsample` is written in Python 3.6+ [@python3] and uses the following software packages:

- `NumPy` [https://github.com/numpy/numpy](https://github.com/numpy/numpy) [@numpy]
- `SciPy` [https://github.com/scipy/scipy](https://github.com/scipy/scipy) [@scipy]
- `scikit-learn` [https://github.com/scikit-learn/scikit-learn](https://github.com/scikit-learn/scikit-learn) [@scikit-learn] 

# References
