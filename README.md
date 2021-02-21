[![PyPI version](https://badge.fury.io/py/bwsample.svg)](https://badge.fury.io/py/bwsample)

# bwsample: Sampling and Evaluation of Best-Worst Scaling sets
Sampling algorithm for best-worst scaling (BWS) sets, extracting pairs from evaluated BWS sets, and count in dictionary of keys sparse matrix.


## Usage
The package `bwsample` addresses three areas:

* [Sampling](#sampling)
* [Counting](#counting)
* [Ranking](#ranking)

Within an Active Learning process the `bwsample` functions can be deployed as followed:

![](/docs/bwsample-process.png)

### Sampling
```python
import bwsample as bws
samples = bws.sample(examples, n_sets, n_items, method='overlap')
```

The input data `examples` for `bwsample.sample` should be a `List[DATA]` ([further details](/docs/sampling-preprocessing.ipynb)), e.g.

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


`n_sets` is the requested number of BWS sets, and `n_items` the specified number of examples per BWS set. There are two algorithms available: `'overlap'` ([further details](/docs/sampling-overlap.ipynb)) and `'twice'` ([further details](/docs/sampling-twice.ipynb)).



### Counting
The function `bwsample.count` is an update function, i.e. you can provide previous count or resp. frequency data (e.g. `dok_all`, `db_infer`) or start from scratch (e.g. `dok_all=None`). See example [here](/docs/count.ipynb)


```python
import bwsample as bws
dok_all, dok_direct, dok_best, dok_worst, dok_infer = bws.count(
    evaluations, dok_all=None, 
    dok_direct=None, dok_best=None, dok_worst=None, 
    dok_infer=None, db_infer=None)
```

The input data `evaluations` for `bwsample.count` should structured as `List[Tuple[List[State], List[ID]]]`. The labelling/annotation application should produce a list of item states `List[EvalState]` with the states `BEST:1`, `WORST:2` and `MIDDLE:0` for each item. And the corresponding list of IDs for each item or resp. example.

```python
evaluations = (
    ([0, 0, 2, 1], ['id1', 'id2', 'id3', 'id4']), 
    ([0, 1, 0, 2], ['id4', 'id5', 'id6', 'id7']),
    ([1, 2, 0, 0], ['id7', 'id8', 'id9', 'id1'])
)
```

The prefix `dok_..` means "Dictionary of Keys", a sparse matrix format, and has the structure `Dict[Tuple[ID, ID], uint]` in our case, i.e. the number of `">"` (gt) relations two examples.

- `'dok_all'`  aggregate counts from extracted pairs (`'dok_direct'`, `'dok_best'`, `'dok_worst'`; [further details](/docs/counting-extract-pairs.ipynb)) plus logical inferred pairs (`'dok_infer'`).
- `'dok_direct'`  pairs of explicit best and worst examples within one BWS set.
- `'dok_best'`   pairs of explicit best and unselected examples within one BWS set.
- `'dok_worst'`  pairs of unselected and explicit worst examples within one BWS set.
- `'dok_infer'`  logical inferred pairs from two BWS sets. Requires previous instances of BWS sets stored in `db_infer`; it has has the same data structure like `evaluations`. If `db_infer=None` then `evaluations` itself is used has database. [further details](/docs/counting-logical-inference.ipynb). Make sure to insert new evaluations, e.g. `db_infer.extends(list(evaluations))`.


### Ranking
The function `bwsample.ranking` computes python index variable with a proposed ordering (`ranked`), and ordered list of example IDs (`ordids`), min-max scaled scores (`scores`) and further information depdending on the selected `method`.


```python
import bwsample as bws
ranked, ordids, scores, info = bws.ranking(dok, method='pvalue')
```

The input data is a `dok_..` dictionary variable described in the [previous section](#counting). 

There are three methods currently available to generate rankings und scores ([further details](/docs/ranking.ipynb)):

* `'ratio'`: by highest sum of min-max-scaled pairs 
* `'pvalue'`: by lowest sum of chi-squared tests' p-values 
* `'eigen'`: derive scores by solving an eigenvalue problem [(Saaty, 2003)](http://dx.doi.org/10.1016/S0377-2217(02)00227-8)
* `'transition'`: predict items that are probably evaluated better




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
