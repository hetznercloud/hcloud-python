import warnings

warnings.warn(
    "The 'hcloud.__version__.VERSION' constant is deprecated, please use 'hcloud.__version__' instead.",
    DeprecationWarning,
    stacklevel=2,
)

from ._version import __version__ as VERSION  # noqa
