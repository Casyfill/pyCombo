try:
    from pyCombo.version import version as __version__
except ImportError:
    __version__ = '0.1.0.dev-unknown'

from combo import getComboPartition as combo
from combo import modularit
