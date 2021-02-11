[![PyPI version](https://badge.fury.io/py/bwsample.svg)](https://badge.fury.io/py/bwsample)

# bwsample
Sampling algorithm for best-worst scaling sets.

## Usage

Table of Contents

* [Use Case 1](#use-case-1)


### Sampling: At least once, every `1/(I-1)`-th twice
In the following example, we generate the indicies of `n_sets=6` BWS sets.
Each BWS set has `n_items=4` items.


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

The default setting is `shuffle=True` to permutate all indices before splitting the BWS sets, 
and to shuffle each BWS set in a final step. 
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
[[5, 0, 8, 1],
 [13, 16, 5, 3],
 [11, 2, 16, 15],
 [4, 9, 2, 17],
 [10, 12, 4, 7],
 [0, 10, 6, 14]]
```


### Sampling: At least twice


### Extract Pairs from evaluated an BWS set


### Extract Pairs by Logical Inference between BWS sets


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
