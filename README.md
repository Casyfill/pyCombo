# pyCOMBO
![CI](https://github.com/Casyfill/pyCombo/workflows/CI/badge.svg)

pyCombo is a python wrapper around [C++ implementation](https://github.com/Alexander-Belyi/Combo) of the [network] community detection algorithm called "Combo".

Details of the algorithm are described in the paper "General optimization technique for high-quality community detection":

```
Sobolevsky, S., Campari, R., Belyi, A. and Ratti, C., 2014. General optimization technique for high-quality community detection in complex networks. Physical Review E, 90(1), p.012811.
```

## Installation
You can install the latest release of pycombo from PyPI by executing
```bash
python -m pip install pycombo
```

## Quick Start
The basic usage is as follows:
```python
import pycombo
import networkx as nx

partition = pycombo.execute(nx.karate_club_graph())
```
Package supports [NetworkX](https://networkx.github.io/) graphs and `.net` files. It can also use custom modularity metrics.
More examples could be found in [example](https://github.com/Casyfill/pyCombo/tree/master/example) folder.

## Development

This repo uses https://github.com/Alexander-Belyi/Combo as a [git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules).
So for local development, clone with `--recurse-submodules` flag, as:
```bash
git clone --recurse-submodules https://github.com/Casyfill/pyCombo
```
Or, if you've already cloned it without `--recurse-submodules`, run:
```bash
git submodule update --init --recursive
```

Package is built and managed via `poetry`.
- to install dev version, run `poetry install`
- To build distributions run `poetry build`.

# Information
- [project web_site](http://senseable.mit.edu/community_detection/)
- [paper](http://journals.aps.org/pre/abstract/10.1103/PhysRevE.90.012811)

### Other useful Links and resources
- [How to build C extension in poetry](https://github.com/python-poetry/poetry/issues/2740)