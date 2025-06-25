from __future__ import annotations

import datetime
from datetime import timezone

import pytest

from hcloud.servers import (
    IPv4Address,
    IPv6Network,
    PrivateNet,
    PublicNetwork,
    PublicNetworkFirewall,
    Server,
    ServerCreatePublicNetwork,
)


@pytest.mark.parametrize(
    "value",
    [
        (Server(id=1),),
        (
            PublicNetwork(
                ipv4=None,
                ipv6=None,
                floating_ips=[],
                primary_ipv4=None,
                primary_ipv6=None,
            ),
        ),
        (PublicNetworkFirewall(firewall=object(), status="pending"),),
        (IPv4Address(ip="127.0.0.1", blocked=False, dns_ptr="example.com"),),
        (IPv6Network("2001:0db8::0/64", blocked=False, dns_ptr="example.com"),),
        (PrivateNet(network=object(), ip="127.0.0.1", alias_ips=[], mac_address=""),),
        (ServerCreatePublicNetwork(),),
    ],
)
def test_eq(value):
    assert value == value


class TestServer:
    def test_created_is_datetime(self):
        server = Server(id=1, created="2016-01-30T23:50+00:00")
        assert server.created == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
