import os
import shutil

from pybind11.setup_helpers import Pybind11Extension, build_ext
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError
from distutils.core import Distribution


ext_modules = [
    Pybind11Extension(
        "pycombo._combo",
        sources=["src/Combo/Graph.cpp", "src/Combo/Combo.cpp", "src/Binder.cpp"],
    )
]


class BuildFailed(Exception):
    pass


class ExtBuilder(build_ext):
    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError):
            raise BuildFailed("File not found. Could not compile C++ extension.")

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (
            CCompilerError,
            DistutilsExecError,
            DistutilsPlatformError,
            ValueError,
        ) as e:
            raise BuildFailed(f"Could not compile C++ extension: {e}")


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    distribution = Distribution({"name": "pycombo", "ext_modules": ext_modules})

    cmd = ExtBuilder(distribution)
    cmd.ensure_finalized()
    cmd.run()

    # Copy built extensions back to the project
    for output in cmd.get_outputs():
        relative_extension = os.path.relpath(output, cmd.build_lib)
        if not os.path.exists(output):
            continue

        shutil.copyfile(output, relative_extension)
        mode = os.stat(relative_extension).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(relative_extension, mode)

    return setup_kwargs


if __name__ == "__main__":
    build({})
