Changelog
=========

### 1.2.0

#### Breaking
- **License changed from MIT to GPL-3.0-or-later** to align with the GPL-licensed [Combo C++ source](https://github.com/Alexander-Belyi/Combo) this package wraps. Downstream use must comply with GPLv3+ terms.
- Dropped Python 3.8 support (now requires Python 3.9+)

#### Added
- `community_attribute` and `as_clustering` kwargs for NetworkX/cdlib interop
- `CITATION.cff` with citation metadata
- `py.typed` marker and improved type hints on `execute()`
- `_combo.pyi` typing stub for IDE support
- Python 3.13 support
- Reproducibility test for `random_seed` and modularity quality check vs leidenalg

#### Fixed
- Edge weight defaults in `deconstruct_graph` (1.0 for unweighted, 0.0 fallback on weighted graphs)
- Dead `weight_key` variable in `deconstruct_graph` that masked the `weight=None` (unweighted) code path
- `execute()` overloads now correctly reflect return types for `as_clustering=True`

#### Removed
- Unused vendored `is_weighted()` function (use `nx.is_weighted()` directly)

#### Changed
- `is_graph()` now uses duck-typing (`hasattr`) instead of hardcoded class names, supporting NX subclasses
- `intermediate_results_path` is only passed to the C++ layer when set
- Migrated from Poetry to uv for package management
- Replaced custom `build.py` (distutils) with scikit-build-core + CMake
- Refactored `execute()` interface: shared params dict, improved type dispatch
- Switched release CI to cibuildwheel with Linux aarch64 + macOS arm64/x86_64 wheels
- Updated CI workflows to use uv and `pypa/gh-action-pypi-publish`

### 0.1.07
- Added a crash fix for C++ version

### 0.1.06
- Fixed C++ attachment in wheel generation

### 0.0.05
- attempting to publish multiplatform wheels using artifacts:
    - for python 3.7, 3.8, 3.9
    - for ubuntu-latest, macos-latest, windows-latest

NOTE: to be specified, perhaps should add arm

### 0.0.03
- fixing `poetry publish build` by adding `--no-interaction`
- test job now only runs on PR
- publish_test now only runs on merge to `master`, and incorporates matrix testing
- publish now works on tags with `*.*.*` pattern and incorporates matrix testing
### 0.1.02

- Added verbose (int) parameter to track progress.
- start_separate (bool) - Indicates if Combo should start by assigning each node into its own separate community. This could help to achieve higher modularity, but it makes execution much slower.
- Fixed an error and warnings in build on windows. (no windows wheels built for PyPI yet)
- few other minor fixes.


### 0.1.01

- readme improvement
- ci imrovement
- `Combo` is now set as a submodule in `src/Combo`


# 0.1.00

- initial version
