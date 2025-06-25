from __future__ import annotations

import pytest

from hcloud.deprecation import DeprecationInfo


@pytest.mark.parametrize(
    "value",
    [
        (DeprecationInfo(),),
    ],
)
def test_eq(value):
    assert value == value
