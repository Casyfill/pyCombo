Changelog
=========

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
