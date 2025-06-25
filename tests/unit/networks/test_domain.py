from __future__ import annotations

import datetime
from datetime import timezone

import pytest

from hcloud.networks import Network, NetworkRoute, NetworkSubnet


@pytest.mark.parametrize(
    "value",
    [
        (Network(id=1),),
        (NetworkSubnet(ip_range="10.0.1.0/24"),),
        (NetworkRoute(destination="10.0.1.2", gateway="10.0.1.1"),),
    ],
)
def test_eq(value):
    assert value == value


class TestNetwork:
    def test_created_is_datetime(self):
        network = Network(id=1, created="2016-01-30T23:50+00:00")
        assert network.created == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
