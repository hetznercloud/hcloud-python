from __future__ import annotations

import datetime
from datetime import timezone

import pytest

from hcloud.floating_ips import FloatingIP


@pytest.mark.parametrize(
    "value",
    [
        (FloatingIP(id=1),),
    ],
)
def test_eq(value):
    assert value.__eq__(value)


class TestFloatingIP:
    def test_created_is_datetime(self):
        floating_ip = FloatingIP(id=1, created="2016-01-30T23:50+00:00")
        assert floating_ip.created == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
