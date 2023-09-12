from __future__ import annotations

import warnings

warnings.warn(
    "The 'hcloud.hcloud' module is deprecated, please import from the 'hcloud' module instead (e.g. 'from hcloud import Client').",
    DeprecationWarning,
    stacklevel=2,
)

# pylint: disable=wildcard-import,wrong-import-position,unused-wildcard-import
from ._client import *  # noqa
