from __future__ import annotations

import datetime
from datetime import timezone

import pytest

from hcloud.primary_ips import PrimaryIP


@pytest.mark.parametrize(
    "value",
    [
        (PrimaryIP(id=1),),
    ],
)
def test_eq(value):
    assert value == value


class TestPrimaryIP:
    def test_created_is_datetime(self):
        primaryIP = PrimaryIP(id=1, created="2016-01-30T23:50+00:00")
        assert primaryIP.created == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
