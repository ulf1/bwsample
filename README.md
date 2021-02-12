[![PyPI version](https://badge.fury.io/py/bwsample.svg)](https://badge.fury.io/py/bwsample)

# bwsample
Sampling algorithm for best-worst scaling sets.

## Usage
Table of Contents

* [Sampling: At least once, every `1/(I-1)`-th twice](#sampling-at-least-once-every-1i-1-th-twice)
* [Sampling: Almost twice](#sampling-almost-twice)
* [Extract Pairs from evaluated an BWS set](#extract-pairs-from-evaluated-an-bws-set)
* [Extract Pairs by Logical Inference between BWS sets](#extract-pairs-by-logical-inference-between-bws-sets)


### Sampling: At least once, every `1/(I-1)`-th twice
In the following example, we generate the indicies of `n_sets=4` BWS sets.
Each BWS set has `n_items=5` items.


```python
from bwsample import indices_overlap
n_sets, n_items, shuffle = 6, 4, False
bwsindices, n_examples = indices_overlap(n_sets, n_items, shuffle)
```

`n_examples=18` means that 19 integer indicies from `range(18)=[0, 17]` were spread across the BWS sets. In the example below, you can see that the last element of a BWS sets is used as the first element in the succeeding BWS sets.

```
bwsindices = 
[[0, 1, 2, 3],
 [3, 4, 5, 6],
 [6, 7, 8, 9],
 [9, 10, 11, 12],
 [12, 13, 14, 15],
 [15, 16, 17, 0]]
```

Assume the indices are mapped to the letters `A-S` (or any other data),
we can illustrate:

![Overlapping BWS sets.](/docs/bwsample-overlap.png)



The default setting is `shuffle=True` to shuffle each BWS set in a final step. 
Random shuffling requires approx. 5-8x more time. 
The behavior is still maintained to display 1 example in the succeeding BWS set.

```python
from bwsample import indices_overlap
import numpy as np
n_sets, n_items, shuffle = 6, 4, True
np.random.seed(42)
bwsindices, n_examples = indices_overlap(n_sets, n_items, shuffle)
```

```
bwsindices = 
[[3, 1, 0, 2],
 [4, 3, 5, 6],
 [9, 7, 6, 8],
 [12, 10, 9, 11],
 [13, 12, 15, 14],
 [16, 15, 0, 17]]
```


### Sampling: Almost twice
The function `indices_twice` also calls `indices_overlap` but connects the non-overlapping examples to new BWS sets.

![Connect not overlapped examples to new BWS sets.](/docs/bwsample-twice.png)


```python
from bwsample import indices_twice
n_sets, n_items, shuffle = 6, 4, False
bwsindices, n_examples = indices_twice(n_sets, n_items, shuffle)
bwsindices
```

```
bwsindices = 
[[0, 1, 2, 3],
 [3, 4, 5, 6],
 [6, 7, 8, 9],
 [9, 10, 11, 12],
 [12, 13, 14, 15],
 [15, 16, 17, 0],
 [1, 5, 10, 14],
 [2, 7, 11, 16],
 [4, 8, 13, 17]]
```

The function does **not** guarantees that all examples occur twice across BWS sets.
The reasons is that the numbers `n_sets` and `n_items` require a common denominator.
For example, if both `n_sets=7` and `n_items=3`  are prime numbers, then remainder examples are unavoidable. 

```python
from bwsample import indices_twice
n_sets, n_items, shuffle = 7, 3, False
bwsindices, n_examples = indices_twice(n_sets, n_items, shuffle)
```


If `n_items` is a prime number, you must ensure that `n_sets` is a multiple of `n_items`, e.g.

```python
from bwsample import indices_twice
n_items, shuffle = 3, False
n_sets = 123 * n_items
bwsindices, n_examples = indices_twice(n_sets, n_items, shuffle)
```



### Extract Pairs from evaluated an BWS set
...

### Extract Pairs by Logical Inference between BWS sets
...

## Appendix

### Installation
The `bwsample` [git repo](http://github.com/ulf1/bwsample) is available as [PyPi package](https://pypi.org/project/bwsample)

```
pip install bwsample
pip install git+ssh://git@github.com/ulf1/bwsample.git
```

### Install a virtual environment

```
python3.6 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
pip install -r requirements-dev.txt --no-cache-dir
pip install -r requirements-demo.txt --no-cache-dir
```

(If your git repo is stored in a folder with whitespaces, then don't use the subfolder `.venv`. Use an absolute path without whitespaces.)

### Python commands

* Jupyter for the examples: `jupyter lab`
* Check syntax: `flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')`
* Run Unit Tests: `pytest`
* Upload to PyPi with twine: `python setup.py sdist && twine upload -r pypi dist/*`

### Clean up 

```
find . -type f -name "*.pyc" | xargs rm
find . -type d -name "__pycache__" | xargs rm -r
rm -r .pytest_cache
rm -r .venv
```


### Support
Please [open an issue](https://github.com/ulf1/bwsample/issues/new) for support.


### Contributing
Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/ulf1/bwsample/compare/).
