# Modernize build and packaging toolchain (uv + scikit-build-core)
date: `2026-06-14`
branch: [migrate-to-uv](https://github.com/Casyfill/pyCombo/tree/migrate-to-uv)

## Status
Accepted

## Decision
Replace the legacy Poetry + `build.py` (distutils) toolchain with a modern, standards-based stack:

- **uv** for dependency resolution, locking (`uv.lock`), and virtual-environment management (replaces Poetry / `poetry.lock`).
- **scikit-build-core + CMake** as the PEP 517 build backend for the C++ extension (replaces the hand-rolled `build.py` distutils script). `pybind11` remains the binding layer, now discovered via CMake `find_package`.
- **cibuildwheel** in release CI to produce multi-platform binary wheels (Linux `x86_64`/`aarch64`, macOS `arm64`/`x86_64`, Windows `AMD64`) for CPython 3.9–3.13, published with `pypa/gh-action-pypi-publish`.
- **Drop Python 3.8**; the project now requires Python 3.9+.
- **Ship type information**: add a `py.typed` marker and a `_combo.pyi` stub for the compiled extension, plus improved hints on the public API.

Project metadata moves from `[tool.poetry]` to the standard `[project]` table, dev dependencies to `[dependency-groups]`, and `pytest.ini` config into `[tool.pytest.ini_options]` in `pyproject.toml`.

## Impact on Consumers
What changes for someone who `pip install pycombo` and imports it. The import surface is unchanged — `import pycombo; pycombo.execute(...)` still works, and the package still has **no runtime dependencies**.

**Breaking / action needed:**
- **Python 3.9+ required.** Python 3.8 is no longer supported; consumers on 3.8 must stay on an older release (`0.1.10`/earlier) or upgrade their interpreter.
- **Building from source now needs CMake.** When no prebuilt wheel matches the platform, installing the sdist requires a CMake toolchain in addition to a C++ compiler (previously just a compiler via distutils).
- **Subtle results change:** edge-weight defaults in graph deconstruction were fixed (1.0 for unweighted, 0.0 fallback on weighted graphs). Partition output for some weighted graphs may differ slightly from prior versions.

**Improvements (no action needed):**
- **More prebuilt wheels** via cibuildwheel — Linux `x86_64`/`aarch64`, macOS `arm64` (Apple Silicon) + `x86_64`, Windows `AMD64`, for CPython 3.9–3.13. Faster, more reliable `pip install` with no local compiler needed on supported platforms.
- **The package is now typed** (`py.typed` + `_combo.pyi`), enabling editor autocomplete and `mypy` checking against `pycombo`.
- **New `execute()` keyword arguments** (additive, backward compatible) for NetworkX/cdlib interop:
  - `community_attribute: Optional[str]` — write the resulting community label back onto each NetworkX node.
  - `as_clustering: bool` — return a `cdlib.NodeClustering` instead of a dict.
  Both apply to NetworkX graph inputs only; all existing positional/keyword arguments keep their previous defaults and behavior.

## Context
The previous setup had several pain points:

- `build.py` manually drove distutils/`Pybind11Extension`, copied artifacts, and handled compiler errors by hand — fragile and hard to reproduce across platforms.
- Poetry's build path did not cleanly support compiled extensions or modern wheel-building, and `poetry.lock` (~3.3k lines) was heavy and slow.
- Wheel publishing was repeatedly broken (see CHANGES `1.0.02`–`0.1.10`: Windows build issues, `upload-artifact@v4` breakage, manual matrix juggling).
- Python 3.8 reached end-of-life, and the package shipped no typing information for downstream users.

## Options Considered

### 1. Stay on Poetry + `build.py` (status quo)
- **Pros:** No migration effort; familiar.
- **Cons:** Continues fragile compiled-extension builds; ongoing CI breakage; non-standard metadata; no clean multi-platform wheel story.

### 2. setuptools + `setup.py`/`pyproject.toml`
- **Pros:** Ubiquitous; well understood.
- **Cons:** Still imperative for C++ builds; CMake integration is awkward; doesn't modernize dependency management.

### 3. scikit-build-core + CMake for builds, uv for dependency management (chosen)
- **Pros:** CMake is the de-facto standard for C++; scikit-build-core is purpose-built for compiled Python extensions and integrates with cibuildwheel; uv gives fast, reproducible locking and is a drop-in workflow tool; all metadata becomes PEP 621 standard.
- **Cons:** Two newer tools to learn; contributors need uv installed; CMake adds a build-time dependency.

## Consequences

**Easier:**
- Reproducible, cross-platform builds; multi-arch wheels produced automatically by cibuildwheel.
- Faster, standard dependency management and locking via uv.
- Standards-compliant `pyproject.toml` (PEP 517/621) — portable across tooling.
- Better downstream DX: typed package via `py.typed` + `_combo.pyi`.
- Simpler release pipeline using `pypa/gh-action-pypi-publish`.

**More difficult / trade-offs:**
- Contributors must install uv and a CMake/C++ toolchain for local development.
- Python 3.8 users are no longer supported.
- New maintenance surface in `CMakeLists.txt` and cibuildwheel config.
- The `_combo.pyi` stub must be kept in sync with the C++ binding by hand.
