# pyCOMBO
![CI](https://github.com/Casyfill/pyCombo/workflows/CI/badge.svg)

pyCombo is a python wrapper around [C++ implementation](https://github.com/Alexander-Belyi/Combo) of the [network] community detection algorithm called "Combo".

Details of the algorithm are described in the paper "General optimization technique for high-quality community detection":

```
Sobolevsky, S., Campari, R., Belyi, A. and Ratti, C., 2014. General optimization technique for high-quality community detection in complex networks. Physical Review E, 90(1), p.012811.
```

## Installation
You can install the latest release of pycombo directly from PyPI:
```bash
python -m pip install pycombo
```
Pre-built wheels are published for Linux (x86_64, aarch64), macOS (Intel + Apple Silicon), and Windows.

If you use Python 3.8, install pyCombo 0.1.07:
```bash
python -m pip install pycombo==0.1.07
```

## Quick Start

Partition a NetworkX graph and get the modularity score:
```python
import networkx as nx
import pycombo

G = nx.karate_club_graph()
partition, modularity = pycombo.execute(G, random_seed=42)
print(f"Found {len(set(partition.values()))} communities, modularity={modularity:.4f}")
```

Write community labels back onto the graph nodes:
```python
partition, modularity = pycombo.execute(
    G,
    random_seed=42,
    community_attribute="community",
)
assert G.nodes[0]["community"] == partition[0]
```

Return a `cdlib` clustering for comparison with other methods:
```python
from cdlib import algorithms

combo_clustering, modularity = pycombo.execute(G, random_seed=42, as_clustering=True)
leiden_clustering = algorithms.leiden(G)
```

Package supports [NetworkX](https://networkx.org/) graphs, Pajek `.net` files, and adjacency matrices passed as numpy array or list.
Combo algorithm uses modularity score as a loss function, but you can use your own metrics as edge weights with `treat_as_modularity=True` parameter.

#### Parameters

* **graph** : `nx.Graph` object, or string treated as path to Pajek `.net` file.
* **weight** : `Optional[str]`, defaults to `weight`. Graph edges property to use as weights. If `None`, graph assumed to be unweighted.
           Ignored if graph is passed as string (path to the file), or such property does not exist.
* **max_communities** : `Optional[int]`, defaults to `None`. Maximum number of communities. If <= 0 or None, assume to be infinite.
* **modularity_resolution** : `float`, defaults to 1.0. Modularity resolution parameter.
* **num_split_attempts** : `int`, defaults to 0. Number of split attempts. If 0, autoadjust this number automatically.
* **fixed_split_step** : `int`, defaults to 0. Step number to apply predefined split. If 0, use only random splits. if >0, sets up the usage of 6 fixed type splits on every fixed_split_step.
* **start_separate** : bool, default False. Indicates if Combo should start from assigning each node into its own separate community. This could help to achieve higher modularity, but it makes execution much slower.
* **treat_as_modularity** : bool, default False. Indicates if edge weights should be treated as modularity scores. If True, the algorithm solves clique partitioning problem over the given graph, treated as modularity graph (matrix). For example, this allows users to provide their own custom 'modularity' matrix. `modularity_resolution` is ignored in this case.
* **verbose** : int, defaults to 0. Indicates how much progress information Combo should print out. For now Combo has only one level starting at verbose >= 1.
* **intermediate_results_path** : Optional str, defaults to None. Path to the file where community assignments will be saved on each iteration. If None or empty, intermediate results will not be saved.
* **return_modularity** : bool, defaults to `True`. Indicates if function should return achieved modularity score.
* **random_seed** : int, defaults to None. Random seed to use. None indicates using some internal default value that is based on time and is expected to be different for each call.
* **community_attribute** : Optional str. When partitioning a NetworkX graph, write labels to `graph.nodes[node][community_attribute]`.
* **as_clustering** : bool, defaults to `False`. Return a `cdlib.classes.NodeClustering` instead of a dict (requires cdlib).

#### Returns

* partition : `Dict{int : int}`, community labels for each node.
* modularity : `float`. Achieved modularity value. Only returned if `return_modularity=True`.

More examples can be found in [example](https://github.com/Casyfill/pyCombo/tree/master/example) folder.

## Development

This repo uses [C++ source](https://github.com/Alexander-Belyi/Combo) as a [git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules).
So for local development, clone with `--recurse-submodules` flag, as:
```bash
git clone --recurse-submodules https://github.com/Casyfill/pyCombo
```
Or, if you've already cloned it without `--recurse-submodules`, run:
```bash
git submodule update --init --recursive
```

Package is built and managed via [uv](https://docs.astral.sh/uv/).
- To use a specific Python version run `uv python pin 3.13`.
- To install dev dependencies, run `uv sync`.
- To build distributions run `uv build`.
- To build all platform wheels locally run `uv run cibuildwheel --output-dir wheelhouse`.
- To run tests execute `uv run pytest`.

# Information
- [project web_site](http://senseable.mit.edu/community_detection/)
- [PyCombo paper](http://journals.aps.org/pre/abstract/10.1103/PhysRevE.90.012811) ([Arxiv](https://arxiv.org/abs/1308.3508))
