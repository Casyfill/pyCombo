try:
    from pyCombo.version import version as __version__
except ImportError:
    __version__ = '0.1.0.dev-unknown'


from pyCombo import getComboPartition as combo
from pyCombo import modularity as modularity