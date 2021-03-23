# pyCOMBO
![CI](https://github.com/Casyfill/pyCombo/workflows/CI/badge.svg)

pyCombo is a python wrapper around [C++ implementation](https://github.com/Alexander-Belyi/Combo) of the [network] community detection algorithm called "Combo".

Combo achieves hight quality of partitioning, while being less greedy in terms of computation, than other algorithms.
![algorithm comparison](http://senseable.mit.edu/community_detection/img/plot_yoon_01.png)

Details of the algorithm are described in the paper "General optimization technique for high-quality community detection in the paper:

```
Sobolevsky, S., Campari, R., Belyi, A. and Ratti, C., 2014. General optimization technique for high-quality community detection in complex networks. Physical Review E, 90(1), p.012811.
```

## Installation
You can install current version of pycombo from github by executing
```bash
pip install pycombo
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

Package is built and managed via `poetry`.
- to install dev version, run `poetry install`
- To build distributions run `poetry build`.

# Information
- [project web_site](http://senseable.mit.edu/community_detection/)
- [paper](http://journals.aps.org/pre/abstract/10.1103/PhysRevE.90.012811)
### Other useful Links and resources
- [How to build C extension in poetry](https://github.com/python-poetry/poetry/issues/2740)
