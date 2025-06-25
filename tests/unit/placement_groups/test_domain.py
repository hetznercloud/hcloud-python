from __future__ import annotations

import datetime
from datetime import timezone

import pytest

from hcloud.placement_groups import PlacementGroup


@pytest.mark.parametrize(
    "value",
    [
        (PlacementGroup(id=1),),
    ],
)
def test_eq(value):
    assert value == value


class TestPlacementGroup:
    def test_created_is_datetime(self):
        placement_group = PlacementGroup(id=1, created="2016-01-30T23:50+00:00")
        assert placement_group.created == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
