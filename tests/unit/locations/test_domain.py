from __future__ import annotations

import pytest

from hcloud.locations import Location


@pytest.mark.parametrize(
    "value",
    [
        (Location(id=1),),
    ],
)
def test_eq(value):
    assert value == value
