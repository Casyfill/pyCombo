# pyCOMBO
![CI](https://github.com/Casyfill/pyCombo/workflows/CI/badge.svg)

Python wrapper around C++ implementation of the [network] community detection algorithm called "Combo".

Details of the algorythm are described in the paper "General optimization technique for high-quality community detection in the paper:


	Sobolevsky S., Campari R., Belyi A., and Ratti C. "General optimization technique for high-quality community detection in complex networks" Phys. Rev. E 90, 012811

## Installation
for now, use:
```bash
python -m pip install https://github.com/Casyfill/pyCombo/archive/pybind11.tar.gz
```
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

##E Roadmap

- [x] Initial release ASIS
- [x] Tests, Travis Ci, Coveralls
- [x] Package delivery, setup.py
- [x] Installation via pip
- [x] unweighted graph
- [x] switched to Github Actions
- [x] switch to poetry
- [x] assert reproductibility (random seed)
- [x] setup pybind11 binding
- [ ] performance (speed) benchmarks
- [ ] full testing
- [ ] understand 2 partitions issue/reason
- [ ] directed graph
- [ ] Exceptions
- [ ] Logging
- [ ] Two Communities minumum


# Notes and issues

- pyCombo does not work on graph of N=1
- pyCombo for some reason always split the network into 2, even for the complete graph
- binaries are now pulled from https://github.com/Express50/Combo/blob/master/Main.cpp, which fixes a few bugs and passes

# Development
this section is for contributors and
## Build
run `poetry install` in order to build local (dev) code. It will
be installed in editable mode within poetry environment

## Links and resources
- [How to build C extension in poetry](https://stackoverflow.com/questions/60073711/how-to-build-c-extensions-via-poetry)
