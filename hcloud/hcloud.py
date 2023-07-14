import warnings

warnings.warn(
    "The 'hcloud.hcloud' module is deprecated, please import from the 'hcloud' module instead (e.g. 'from hcloud import Client').",
    DeprecationWarning,
    stacklevel=2,
)

from ._client import *  # noqa
