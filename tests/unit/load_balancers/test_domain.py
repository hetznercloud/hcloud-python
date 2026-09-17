from __future__ import annotations

import datetime
from datetime import timezone
from unittest import mock

import pytest

from hcloud.load_balancers import (
    BoundLoadBalancer,
    IPv4Address,
    IPv6Network,
    LoadBalancer,
    LoadBalancerAlgorithm,
    LoadBalancerHealthCheck,
    LoadBalancerHealthCheckHttp,
    LoadBalancerService,
    LoadBalancerServiceHttp,
    LoadBalancerTarget,
    LoadBalancerTargetHealthStatus,
    LoadBalancerTargetIP,
    LoadBalancerTargetLabelSelector,
    PrivateNet,
    PublicNetwork,
)
from hcloud.networks import Network


@pytest.mark.parametrize(
    "value",
    [
        (LoadBalancer(id=1),),
        (LoadBalancerService,),
        (LoadBalancerServiceHttp(),),
        (LoadBalancerHealthCheck(),),
        (LoadBalancerHealthCheckHttp(),),
        (LoadBalancerTarget(),),
        (LoadBalancerTargetHealthStatus(),),
        (LoadBalancerTargetLabelSelector(),),
        (LoadBalancerTargetIP(),),
        (LoadBalancerAlgorithm(),),
        (
            PublicNetwork(
                ipv4=IPv4Address(ip="127.0.0.1", dns_ptr="example.com"),
                ipv6=IPv6Network("2001:0db8::0/64", dns_ptr="example.com"),
                enabled=True,
            ),
        ),
        (IPv4Address(ip="127.0.0.1", dns_ptr="example.com"),),
        (IPv6Network("2001:0db8::0/64", dns_ptr="example.com"),),
        (PrivateNet(network=object(), ip="127.0.0.1"),),
    ],
)
def test_eq(value):
    assert value.__eq__(value)


class TestLoadBalancers:
    def test_created_is_datetime(self):
        lb = LoadBalancer(id=1, created="2016-01-30T23:50+00:00")
        assert lb.created == datetime.datetime(2016, 1, 30, 23, 50, tzinfo=timezone.utc)

    def test_private_net_for(self):
        network1 = Network(id=1)
        network2 = Network(id=2)
        network3 = Network(id=3)

        load_balancer = LoadBalancer(
            id=42,
            private_net=[
                PrivateNet(network=network1, ip="127.0.0.1"),
                PrivateNet(network=network2, ip="127.0.0.1"),
            ],
        )

        assert load_balancer.private_net_for(network1).network.id == 1
        assert load_balancer.private_net_for(network3) is None

        load_balancer = BoundLoadBalancer(
            client=mock.MagicMock(),
            data={
                "id": 42,
                "private_net": [
                    {"network": 1, "ip": "127.0.0.1"},
                    {"network": 2, "ip": "127.0.0.1"},
                ],
            },
        )

        assert load_balancer.private_net_for(network1).network.id == 1
        assert load_balancer.private_net_for(network3) is None


def test_load_balancer_service_to_payload_keeps_set_properties():
    health_check = LoadBalancerHealthCheck()
    health_check.protocol = "tcp"
    health_check.port = 80
    health_check.interval = 15
    health_check.timeout = 10
    health_check.retries = 3

    service = LoadBalancerService(
        protocol="tcp",
        listen_port=80,
        destination_port=80,
        health_check=health_check,
    )

    payload = service.to_payload()

    assert payload["health_check"] == {
        "protocol": "tcp",
        "port": 80,
        "interval": 15,
        "timeout": 10,
        "retries": 3,
    }


def test_load_balancer_service_to_payload_omits_unset_properties():
    # Regression test for https://github.com/ansible-collections/hetzner.hcloud/issues/158
    #
    # When only some of the health_check fields are set, the payload must not
    # include the unset ones as `null`, otherwise the Hetzner Cloud API rejects
    # the request with "invalid input in field 'health_check'".
    health_check = LoadBalancerHealthCheck()
    health_check.http = LoadBalancerHealthCheckHttp()
    health_check.http.status_codes = ["404"]
    health_check.http.tls = False

    service = LoadBalancerService(
        protocol="https",
        listen_port=443,
        proxyprotocol=False,
        health_check=health_check,
    )

    payload = service.to_payload()

    assert payload["health_check"] == {
        "http": {
            "status_codes": ["404"],
            "tls": False,
        },
    }
