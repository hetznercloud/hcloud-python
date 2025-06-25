from __future__ import annotations

import pytest

from hcloud.server_types import ServerType


@pytest.mark.parametrize(
    "value",
    [
        (ServerType(id=1),),
    ],
)
def test_eq(value):
    assert value == value
