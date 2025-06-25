from __future__ import annotations

import datetime
from datetime import timezone

import pytest

from hcloud.firewalls import (
    Firewall,
    FirewallResource,
    FirewallResourceAppliedToResources,
    FirewallResourceLabelSelector,
    FirewallRule,
)


@pytest.mark.parametrize(
    "value",
    [
        (Firewall(id=1),),
        (FirewallRule(direction="in", protocol="icmp", source_ips=[]),),
        (FirewallResource(type="server"),),
        (FirewallResourceAppliedToResources(type="server"),),
        (FirewallResourceLabelSelector(),),
    ],
)
def test_eq(value):
    assert value == value


class TestFirewall:
    def test_created_is_datetime(self):
        firewall = Firewall(id=1, created="2016-01-30T23:50+00:00")
        assert firewall.created == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
