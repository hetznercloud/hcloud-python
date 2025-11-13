from __future__ import annotations

import datetime
from datetime import timezone
from unittest import mock

import pytest

from hcloud.networks import Network
from hcloud.servers import (
    BoundServer,
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
    assert value.__eq__(value)


class TestServer:
    def test_created_is_datetime(self):
        server = Server(id=1, created="2016-01-30T23:50+00:00")
        assert server.created == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )

    def test_private_net_for(self):
        network1 = Network(id=1)
        network2 = Network(id=2)
        network3 = Network(id=3)

        server = Server(
            id=42,
            private_net=[
                PrivateNet(
                    network=network1, ip="127.0.0.1", alias_ips=[], mac_address=""
                ),
                PrivateNet(
                    network=network2, ip="127.0.0.1", alias_ips=[], mac_address=""
                ),
            ],
        )

        assert server.private_net_for(network1).network.id == 1
        assert server.private_net_for(network3) is None

        server = BoundServer(
            client=mock.MagicMock(),
            data={
                "id": 42,
                "private_net": [
                    {
                        "network": 1,
                        "ip": "127.0.0.1",
                        "alias_ips": [],
                        "mac_address": "",
                    },
                    {
                        "network": 2,
                        "ip": "127.0.0.1",
                        "alias_ips": [],
                        "mac_address": "",
                    },
                ],
            },
        )

        assert server.private_net_for(network1).network.id == 1
        assert server.private_net_for(network3) is None
