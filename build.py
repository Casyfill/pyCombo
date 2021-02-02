# from distutils.command.build_ext import build_ext
# from distutils.core import Extension
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError
from pybind11.setup_helpers import Pybind11Extension, build_ext


ext_modules = [
    Pybind11Extension(
        "pycombo.combo", sources=["src/Main.cpp", "src/Graph.cpp", "src/Binder.cpp"]
    )
]


class BuildFailed(Exception):
    pass


class ExtBuilder(build_ext):
    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError):
            raise BuildFailed("File not found. Could not compile C extension.")

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (
            CCompilerError,
            DistutilsExecError,
            DistutilsPlatformError,
            ValueError,
        ) as e:
            raise BuildFailed(f"Could not compile C extension: {e}")


def build(setup_kwargs):
    """
    This function is mandatory in order to build the extensions.
    """
    setup_kwargs.update(
        {"ext_modules": ext_modules, "cmdclass": {"build_ext": ExtBuilder}}
    )
