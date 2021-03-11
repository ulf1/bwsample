[![PyPI version](https://badge.fury.io/py/bwsample.svg)](https://badge.fury.io/py/bwsample)
[![DOI](https://zenodo.org/badge/335090754.svg)](https://zenodo.org/badge/latestdoi/335090754)

# bwsample: Sampling and Evaluation of Best-Worst Scaling sets
Sampling algorithm for best-worst scaling (BWS) sets, extracting pairs from evaluated BWS sets, count in dictionary of keys sparse matrix, and compute scores based on it.

## Installation
The `bwsample` [git repo](http://github.com/ulf1/bwsample) is available as [PyPi package](https://pypi.org/project/bwsample)

```
pip install bwsample>=0.6.0
```

## Usage
The package `bwsample` addresses three areas:

* [Sampling](#sampling)
* [Counting](#counting)
* [Ranking](#ranking)

### Sampling


### Counting


### Ranking



## Appendix

### Install a virtual environment
In order to run the Jupyter notebooks or want to work on this project (e.g. unit tests, syntax checks) you should install a Python virtual environment.

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
