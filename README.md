# pyCOMBO
![CI](https://github.com/Casyfill/pyCombo/workflows/CI/badge.svg)

pyCombo is a python wrapper around [C++ implementation](https://github.com/Alexander-Belyi/Combo) of the [network] community detection algorithm called "Combo".

Details of the algorythm are described in the paper "General optimization technique for high-quality community detection in the paper:


	Sobolevsky S., Campari R., Belyi A., and Ratti C. "General optimization technique for high-quality community detection in complex networks" Phys. Rev. E 90, 012811

## Installation
You can install current version of pycombo from github by executing
```bash
python -m pip install git+https://github.com/Casyfill/pyCombo.git#edd=pycombo
```

## Example
The basic usage is as follows:
```python
import pycombo
import networkx as nx

print(pycombo.get_combo_partition(nx.karate_club_graph()))
```
More examples could be found in [example](https://github.com/Casyfill/pyCombo/tree/master/example) folder.

## Dependencies
*pyCombo* does not have any dependency, yet it was created having [NetworkX](https://networkx.github.io/) module in mind.

## Why Combo?
![algorithm comparison](http://senseable.mit.edu/community_detection/img/plot_yoon_01.png)

Combo achieves hight quality of partitioning, while being less greedy in terms of computation, than other algorithms.



## More information
- [project web_site](http://senseable.mit.edu/community_detection/)
- [paper](http://journals.aps.org/pre/abstract/10.1103/PhysRevE.90.012811)

## Licensing
All copiryghts and licensing is same as covered in the initial package

## Roadmap
- [x] Initial release ASIS
- [x] Tests, Travis Ci, Coveralls
- [x] Package delivery, setup.py
- [x] Installation via pip
- [x] unweighted graph
- [x] switched to Github Actions
- [x] switch to poetry
- [x] assert reproductibility (random seed)
- [x] setup pybind11 binding
- [x] directed graph
- [ ] understand 2 partitions issue/reason
- [ ] full testing
- [ ] performance (speed) benchmarks
- [ ] Exceptions
- [ ] Logging
- [ ] Two Communities minumum


# Notes and issues
- pyCombo does not work on graph of N=1
- pyCombo for some reason always split the network into 2, even for the complete graph
- for now c++ sources duplicate https://github.com/Alexander-Belyi/Combo

# Development
Feel free to fork this repo and submit pull requests.

## Local development
Run `poetry install` in order to install local (dev) code.
It will be installed in editable mode within poetry environment.

## Build
To build distributions run `poetry build`.

## Links and resources
- [How to build C extension in poetry](https://github.com/python-poetry/poetry/issues/2740)
