from __future__ import annotations

import pytest

from hcloud.storage_boxes import StorageBox


@pytest.mark.parametrize(
    "value",
    [
        (StorageBox(id=1),),
    ],
)
def test_eq(value):
    assert value.__eq__(value)
