from __future__ import annotations

import datetime
from datetime import timezone

import pytest

from hcloud.volumes import Volume


@pytest.mark.parametrize(
    "value",
    [
        (Volume(id=1),),
    ],
)
def test_eq(value):
    assert value == value


class TestVolume:
    def test_created_is_datetime(self):
        volume = Volume(id=1, created="2016-01-30T23:50+00:00")
        assert volume.created == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
