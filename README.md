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
**Input Data:**
The input data `examples` for `bwsample.sample` should be a `List[anything]`.
For example, `List[Dict[ID,DATA]]` with identifiers using the key `"id"` and the associated data using the key `"data"`, e.g.

```python
examples = [
    {"id": "id1", "data": "data..."},
    {"id": "id2", "data": ["other", "data"]},
    {"id": "id3", "data": {"key", "value"}},
    {"id": "id4", "data": "lorem"},
    {"id": "id5", "data": "ipsum"},
    {"id": "id6", "data": "blind"},
    {"id": "id7", "data": "text"}
]
```

**Call the function:**
The number of items per BWS set `n_items` (`M`) must be specified, e.g. `n_items=4` if your App displays four items.
The `'overlap'` algorithm assigns every `i*(M-1)+1`-th example to two consecutive BWS sets, so that `1/(M-1)` of examples are evaluated two times.
The `'twice'` algorithm connects the remaining `(M-2)/(M-1)` non-overlapping from `'overlapping'` so that all examples occur twice.
The total number of sampled BWS sets might differ accordingly.

```python
import bwsample as bws
samples = bws.sample(examples, n_items=4, method='overlap')
```

**Output Data:**
The output has the following structure

```
[
    [{'id': 'id1', 'data': 'data...'}, {'id': 'id2', 'data': ['other', 'data']}, {'id': 'id3', 'data': {'key', 'value'}}, {'id': 'id4', 'data': 'lorem'}], 
    [{'id': 'id1', 'data': 'data...'}, {'id': 'id4', 'data': 'lorem'}, {'id': 'id5', 'data': 'ipsum'}, {'id': 'id6', 'data': 'blind'}]
]
```

**Warning**: `len(examples)` must be a multiple of `(n_items - 1)`


### Counting
**Input Data:**
The input data`evaluations` for `bwsample.count` should structured as `List[Tuple[List[ItemState], List[ItemID]]]`. 
The labelling/annotation application should produce a list of item states `List[ItemState]` with the states `BEST:1`, `WORST:2` and `NOT:0` for each item. 
And the corresponding list of IDs `List[ItemID]` for each item or resp. example.

```python
evaluations = (
    ([0, 0, 2, 1], ['id1', 'id2', 'id3', 'id4']), 
    ([0, 1, 0, 2], ['id4', 'id5', 'id6', 'id7']),
    ([1, 2, 0, 0], ['id7', 'id8', 'id9', 'id1'])
)
```

**Call the function:**

```python
import bwsample as bws
agg_dok, direct_dok, direct_detail, logical_dok, logical_detail = bws.count(evaluations)
```


**Output Data:**
The function `bwsample.count` outputs Dictionary of Keys (DOK) with the data strcuture `Dict[Tuple[ItemID, ItemID], int]`, e.g. `agg_dok`, `direct_dok`, `direct_detail["bw"]`, etc., what contain variants which pairs where counted:

- `agg_dok`
    - `direct_dok`
        - `direct_detail["bw"]`
        - `direct_detail["bn"]`
        - `direct_detail["nw"]`
    - `logical_dok`
        - `logical_detail["nn"]`
        - `logical_detail["nb"]`
        - `logical_detail["nw"]`
        - `logical_detail["bn"]`
        - `logical_detail["bw"]`
        - `logical_detail["wn"]`
        - `logical_detail["wb"]`



**Update Frequencies:**
The function `bwsample.count` is an update function, i.e. you can provide previous count or resp. frequency data (e.g. `logical_dok`, `logical_database`) or start from scratch (e.g. `agg_dok=None`).


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
