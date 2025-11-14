from __future__ import annotations

import pytest

from hcloud.storage_box_types import StorageBoxType


@pytest.mark.parametrize(
    "value",
    [
        (StorageBoxType(id=1),),
    ],
)
def test_eq(value):
    assert value.__eq__(value)
