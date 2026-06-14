Changelog
=========

### 0.1.10
- Fixed edge weight defaults in `deconstruct_graph` (1.0 for unweighted, 0.0 fallback on weighted graphs)
- Added `community_attribute` and `as_clustering` kwargs for NetworkX/cdlib interop
- Added reproducibility test for `random_seed` and modularity quality check vs leidenalg
- Added `py.typed` marker and improved type hints on `execute()`
- Switched release CI to cibuildwheel with Linux aarch64 + macOS arm64/x86_64 wheels
- Added Python 3.13 support

### 0.1.09
- Migrated from Poetry to uv for package management
- Replaced custom `build.py` (distutils) with scikit-build-core + CMake
- Dropped Python 3.8 support (now requires Python 3.9+)
- Refactored `execute()` interface: shared params dict, improved type dispatch
- Added `_combo.pyi` typing stub for IDE support
- Updated CI workflows to use uv and `pypa/gh-action-pypi-publish`

### 0.1.07
- Added a crash fix for C++ version

### 1.0.06
- Fixed C++ attachment in wheel generation

### 1.0.05
- attempting to publish multiplatform wheels using artifacts:
    - for python 3.7, 3.8, 3.9
    - for ubuntu-latest, macos-latest, windows-latest

NOTE: to be specified, perhaps should add arm

### 1.0.03
- fixing (hopefully) `poetry publish build` by adding `--no-interaction`
- test job now only runs on PR
- publish_test now only runs on merge to `master`, and incorporates matrix testing
- publish now works on tags with `*.*.*` pattern and incorporates matrix testing
### 1.0.02

- Added verbose (int) parameter to track progress.
- start_separate (bool) - Indicates if Combo should start by assigning each node into its own separate community. This could help to achieve higher modularity, but it makes execution much slower.
- Fixed an error and warnings in build on windows. (no windows wheels built for PyPI yet)
- few other minor fixes.


### 1.0.01

- readme improvement
- ci imrovement
- `Combo` is now set as a submodule in `src/Combo`


# 1.0.00

- initial version
