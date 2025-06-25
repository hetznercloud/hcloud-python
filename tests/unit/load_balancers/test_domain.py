from __future__ import annotations

import datetime
from datetime import timezone

import pytest

from hcloud.load_balancers import (
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
    assert value == value


class TestLoadBalancers:
    def test_created_is_datetime(self):
        lb = LoadBalancer(id=1, created="2016-01-30T23:50+00:00")
        assert lb.created == datetime.datetime(2016, 1, 30, 23, 50, tzinfo=timezone.utc)
