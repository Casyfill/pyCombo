try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)

from .pyCombo import get_combo_partition

__all__ = ["get_combo_partition"]
