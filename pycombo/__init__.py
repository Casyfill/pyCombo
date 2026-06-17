import importlib.metadata as importlib_metadata

__version__ = importlib_metadata.version(__name__)

from .pyCombo import execute

__all__ = ["execute"]
