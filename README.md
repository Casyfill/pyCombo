# pyCOMBO
[![Build Status](https://travis-ci.org/Casyfill/pyCOMBO.svg?branch=master)](https://travis-ci.org/Casyfill/pyCOMBO)
[![Coverage Status](https://coveralls.io/repos/github/Casyfill/pyCombo/badge.svg?branch=master)](https://coveralls.io/github/Casyfill/pyCombo?branch=master)

**THis is the initial commit, not release version. any code shared AS IS**

This is a python wrapper around C++ implementation (for Modularity maximization) of the community detection algorithm called "Combo" described in the paper "General optimization technique for high-quality community detection in complex networks" by Stanislav Sobolevsky, Riccardo Campari, Alexander Belyi and Carlo Ratti.

![Portugal cellular talks partition](http://senseable.mit.edu/community_detection/img/portugal_img.png)

"Combo" algorithm for community detection  described in the paper:

	Sobolevsky S., Campari R., Belyi A., and Ratti C. "General optimization technique for high-quality community detection in complex networks" Phys. Rev. E 90, 012811

## Why Combo?

![algorithm comparison](http://senseable.mit.edu/community_detection/img/plot_yoon_01.png)

Combo achieves hight quality of partitioning, while being less greedy in terms of computation, than other algorithms.

## Installation

`pip install -e git+git@github.com:Casyfill/pyCombo.git@master#egg=pyCombo`

## Dependency

*pyCombo* does not have any dependency, yet it was created having [NetworkX](https://networkx.github.io/) module in mind.


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
- [ ] switched to Github Actions
- [ ] switch to poetry
- [ ] check & test modularity
- [ ] assert reproductibility
- [ ] understand 2 partitions issue/reason
- [ ] directed graph
- [ ] Exceptions




# Notes and issues

- pyCombo does not work on graph of N=1
- pyCombo for some reason always split the network into 2, even for the complete graph
- binaries are now pulled from https://github.com/Express50/Combo/blob/master/Main.cpp, which fixes a few bugs and passes 