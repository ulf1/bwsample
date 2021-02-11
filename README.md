[![PyPI version](https://badge.fury.io/py/bwsample.svg)](https://badge.fury.io/py/bwsample)

# bwsample
Sampling algorithm for best-worst scaling sets.

## Usage

Table of Contents

* [Use Case 1](#use-case-1)


### Sampling: At least once, every `1/(I-1)`-th twice

```python
n_sets, n_items, permute = 10, 4, False
bwsindices, n_examples = indices_overlap(n_sets, n_items, permute)
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
