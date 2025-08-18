from __future__ import annotations

from unittest import mock

import pytest

from hcloud import Client
from hcloud.load_balancer_types import LoadBalancerType
from hcloud.load_balancers import (
    BoundLoadBalancer,
    LoadBalancer,
    LoadBalancerAlgorithm,
    LoadBalancerHealthCheck,
    LoadBalancersClient,
    LoadBalancerService,
    LoadBalancerTarget,
    LoadBalancerTargetIP,
    LoadBalancerTargetLabelSelector,
)
from hcloud.locations import Location
from hcloud.networks import Network
from hcloud.servers import Server


class TestBoundLoadBalancer:
    @pytest.fixture()
    def bound_load_balancer(self, client: Client):
        return BoundLoadBalancer(client.load_balancers, data=dict(id=14))

    def test_bound_load_balancer_init(self, response_load_balancer):
        bound_load_balancer = BoundLoadBalancer(
            client=mock.MagicMock(), data=response_load_balancer["load_balancer"]
        )

        assert bound_load_balancer.id == 4711
        assert bound_load_balancer.name == "Web Frontend"

    def test_update(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        response_update_load_balancer,
    ):
        request_mock.return_value = response_update_load_balancer

        load_balancer = bound_load_balancer.update(name="new-name", labels={})

        request_mock.assert_called_with(
            method="PUT",
            url="/load_balancers/14",
            json={"name": "new-name", "labels": {}},
        )

        assert load_balancer.id == 4711
        assert load_balancer.name == "new-name"

    def test_delete(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        action_response,
    ):
        request_mock.return_value = action_response

        delete_success = bound_load_balancer.delete()

        request_mock.assert_called_with(
            method="DELETE",
            url="/load_balancers/14",
        )

        assert delete_success is True

    def test_get_metrics(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer: BoundLoadBalancer,
        response_get_metrics,
    ):
        request_mock.return_value = response_get_metrics

        response = bound_load_balancer.get_metrics(
            type=["requests_per_second"],
            start="2023-12-14T16:55:32+01:00",
            end="2023-12-14T16:55:32+01:00",
        )

        request_mock.assert_called_with(
            method="GET",
            url="/load_balancers/14/metrics",
            params={
                "type": "requests_per_second",
                "start": "2023-12-14T16:55:32+01:00",
                "end": "2023-12-14T16:55:32+01:00",
            },
        )
        assert "requests_per_second" in response.metrics.time_series
        assert len(response.metrics.time_series["requests_per_second"]["values"]) == 3

    def test_add_service(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        response_add_service,
    ):
        request_mock.return_value = response_add_service

        service = LoadBalancerService(listen_port=80, protocol="http")
        action = bound_load_balancer.add_service(service)

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/14/actions/add_service",
            json={"protocol": "http", "listen_port": 80},
        )

        assert action.id == 13
        assert action.progress == 100
        assert action.command == "add_service"

    def test_delete_service(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        response_delete_service,
    ):
        request_mock.return_value = response_delete_service

        service = LoadBalancerService(listen_port=12)
        action = bound_load_balancer.delete_service(service)

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/14/actions/delete_service",
            json={"listen_port": 12},
        )

        assert action.id == 13
        assert action.progress == 100
        assert action.command == "delete_service"

    @pytest.mark.parametrize(
        "target,params",
        [
            (
                LoadBalancerTarget(
                    type="server", server=Server(id=1), use_private_ip=True
                ),
                {"server": {"id": 1}, "use_private_ip": True},
            ),
            (
                LoadBalancerTarget(type="ip", ip=LoadBalancerTargetIP(ip="127.0.0.1")),
                {"ip": {"ip": "127.0.0.1"}},
            ),
            (
                LoadBalancerTarget(
                    type="label_selector",
                    label_selector=LoadBalancerTargetLabelSelector(selector="abc=def"),
                ),
                {"label_selector": {"selector": "abc=def"}},
            ),
        ],
    )
    def test_add_target(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        response_add_target,
        target,
        params,
    ):
        request_mock.return_value = response_add_target

        action = bound_load_balancer.add_target(target)
        params.update({"type": target.type})

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/14/actions/add_target",
            json=params,
        )

        assert action.id == 13
        assert action.progress == 100
        assert action.command == "add_target"

    @pytest.mark.parametrize(
        "target,params",
        [
            (
                LoadBalancerTarget(
                    type="server", server=Server(id=1), use_private_ip=True
                ),
                {"server": {"id": 1}},
            ),
            (
                LoadBalancerTarget(type="ip", ip=LoadBalancerTargetIP(ip="127.0.0.1")),
                {"ip": {"ip": "127.0.0.1"}},
            ),
            (
                LoadBalancerTarget(
                    type="label_selector",
                    label_selector=LoadBalancerTargetLabelSelector(selector="abc=def"),
                ),
                {"label_selector": {"selector": "abc=def"}},
            ),
        ],
    )
    def test_remove_target(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        response_remove_target,
        target,
        params,
    ):
        request_mock.return_value = response_remove_target

        action = bound_load_balancer.remove_target(target)
        params.update({"type": target.type})

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/14/actions/remove_target",
            json=params,
        )

        assert action.id == 13
        assert action.progress == 100
        assert action.command == "remove_target"

    def test_update_service(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        response_update_service,
    ):
        request_mock.return_value = response_update_service

        new_health_check = LoadBalancerHealthCheck(
            protocol="http", port=13, interval=1, timeout=1, retries=1
        )
        service = LoadBalancerService(listen_port=12, health_check=new_health_check)

        action = bound_load_balancer.update_service(service)

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/14/actions/update_service",
            json={
                "listen_port": 12,
                "health_check": {
                    "protocol": "http",
                    "port": 13,
                    "interval": 1,
                    "timeout": 1,
                    "retries": 1,
                },
            },
        )

        assert action.id == 13
        assert action.progress == 100
        assert action.command == "update_service"

    def test_change_algorithm(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        response_change_algorithm,
    ):
        request_mock.return_value = response_change_algorithm

        algorithm = LoadBalancerAlgorithm(type="round_robin")
        action = bound_load_balancer.change_algorithm(algorithm)

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/14/actions/change_algorithm",
            json={"type": "round_robin"},
        )

        assert action.id == 13
        assert action.progress == 100
        assert action.command == "change_algorithm"

    def test_change_dns_ptr(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        response_change_reverse_dns_entry,
    ):
        request_mock.return_value = response_change_reverse_dns_entry

        action = bound_load_balancer.change_dns_ptr(
            ip="1.2.3.4", dns_ptr="lb1.example.com"
        )

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/14/actions/change_dns_ptr",
            json={"dns_ptr": "lb1.example.com", "ip": "1.2.3.4"},
        )

        assert action.id == 13
        assert action.progress == 100
        assert action.command == "change_dns_ptr"

    def test_change_protection(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        response_change_protection,
    ):
        request_mock.return_value = response_change_protection

        action = bound_load_balancer.change_protection(delete=True)

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/14/actions/change_protection",
            json={"delete": True},
        )

        assert action.id == 13
        assert action.progress == 100
        assert action.command == "change_protection"

    def test_enable_public_interface(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        response_enable_public_interface,
    ):
        request_mock.return_value = response_enable_public_interface

        action = bound_load_balancer.enable_public_interface()

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/14/actions/enable_public_interface",
        )

        assert action.id == 13
        assert action.progress == 100
        assert action.command == "enable_public_interface"

    def test_disable_public_interface(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        response_disable_public_interface,
    ):
        request_mock.return_value = response_disable_public_interface

        action = bound_load_balancer.disable_public_interface()

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/14/actions/disable_public_interface",
        )

        assert action.id == 13
        assert action.progress == 100
        assert action.command == "disable_public_interface"

    def test_attach_to_network(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        response_attach_load_balancer_to_network,
    ):
        request_mock.return_value = response_attach_load_balancer_to_network

        action = bound_load_balancer.attach_to_network(Network(id=1))

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/14/actions/attach_to_network",
            json={"network": 1},
        )

        assert action.id == 13
        assert action.progress == 100
        assert action.command == "attach_to_network"

    def test_detach_from_network(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        response_detach_from_network,
    ):
        request_mock.return_value = response_detach_from_network

        action = bound_load_balancer.detach_from_network(Network(id=1))

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/14/actions/detach_from_network",
            json={"network": 1},
        )

        assert action.id == 13
        assert action.progress == 100
        assert action.command == "detach_from_network"

    def test_change_type(
        self,
        request_mock: mock.MagicMock,
        bound_load_balancer,
        action_response,
    ):
        request_mock.return_value = action_response

        action = bound_load_balancer.change_type(LoadBalancerType(name="lb21"))

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/14/actions/change_type",
            json={"load_balancer_type": "lb21"},
        )

        assert action.id == 1
        assert action.progress == 0


class TestLoadBalancerslient:
    @pytest.fixture()
    def load_balancers_client(self, client: Client):
        return LoadBalancersClient(client)

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        load_balancers_client: LoadBalancersClient,
        response_load_balancer,
    ):
        request_mock.return_value = response_load_balancer

        bound_load_balancer = load_balancers_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/load_balancers/1",
        )
        assert bound_load_balancer._client is load_balancers_client
        assert bound_load_balancer.id == 4711
        assert bound_load_balancer.name == "Web Frontend"
        assert bound_load_balancer.outgoing_traffic == 123456
        assert bound_load_balancer.ingoing_traffic == 123456
        assert bound_load_balancer.included_traffic == 654321

    @pytest.mark.parametrize(
        "params",
        [
            {
                "name": "load_balancer1",
                "label_selector": "label1",
                "page": 1,
                "per_page": 10,
            },
            {"name": ""},
            {},
        ],
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        load_balancers_client: LoadBalancersClient,
        response_simple_load_balancers,
        params,
    ):
        request_mock.return_value = response_simple_load_balancers

        result = load_balancers_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/load_balancers",
            params=params,
        )

        bound_load_balancers = result.load_balancers
        assert result.meta is not None

        assert len(bound_load_balancers) == 2

        bound_load_balancer1 = bound_load_balancers[0]
        bound_load_balancer2 = bound_load_balancers[1]

        assert bound_load_balancer1._client is load_balancers_client
        assert bound_load_balancer1.id == 4711
        assert bound_load_balancer1.name == "Web Frontend"

        assert bound_load_balancer2._client is load_balancers_client
        assert bound_load_balancer2.id == 4712
        assert bound_load_balancer2.name == "Web Frontend2"

    @pytest.mark.parametrize(
        "params", [{"name": "loadbalancer1", "label_selector": "label1"}, {}]
    )
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        load_balancers_client: LoadBalancersClient,
        response_simple_load_balancers,
        params,
    ):
        request_mock.return_value = response_simple_load_balancers

        bound_load_balancers = load_balancers_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/load_balancers",
            params=params,
        )

        assert len(bound_load_balancers) == 2

        bound_load_balancer1 = bound_load_balancers[0]
        bound_load_balancer2 = bound_load_balancers[1]

        assert bound_load_balancer1._client is load_balancers_client
        assert bound_load_balancer1.id == 4711
        assert bound_load_balancer1.name == "Web Frontend"

        assert bound_load_balancer2._client is load_balancers_client
        assert bound_load_balancer2.id == 4712
        assert bound_load_balancer2.name == "Web Frontend2"

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        load_balancers_client: LoadBalancersClient,
        response_simple_load_balancers,
    ):
        request_mock.return_value = response_simple_load_balancers

        bound_load_balancer = load_balancers_client.get_by_name("Web Frontend")

        params = {"name": "Web Frontend"}

        request_mock.assert_called_with(
            method="GET",
            url="/load_balancers",
            params=params,
        )

        assert bound_load_balancer._client is load_balancers_client
        assert bound_load_balancer.id == 4711
        assert bound_load_balancer.name == "Web Frontend"

    def test_create(
        self,
        request_mock: mock.MagicMock,
        load_balancers_client: LoadBalancersClient,
        response_create_load_balancer,
    ):
        request_mock.return_value = response_create_load_balancer

        response = load_balancers_client.create(
            "my-balancer",
            load_balancer_type=LoadBalancerType(name="lb11"),
            location=Location(id=1),
        )

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers",
            json={"name": "my-balancer", "load_balancer_type": "lb11", "location": 1},
        )

        bound_load_balancer = response.load_balancer

        assert bound_load_balancer._client is load_balancers_client
        assert bound_load_balancer.id == 1
        assert bound_load_balancer.name == "my-balancer"

    @pytest.mark.parametrize(
        "load_balancer",
        [LoadBalancer(id=1), BoundLoadBalancer(mock.MagicMock(), dict(id=1))],
    )
    def test_change_type_with_load_balancer_type_name(
        self,
        request_mock: mock.MagicMock,
        load_balancers_client: LoadBalancersClient,
        load_balancer,
        action_response,
    ):
        request_mock.return_value = action_response

        action = load_balancers_client.change_type(
            load_balancer, LoadBalancerType(name="lb11")
        )

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/1/actions/change_type",
            json={"load_balancer_type": "lb11"},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "load_balancer",
        [LoadBalancer(id=1), BoundLoadBalancer(mock.MagicMock(), dict(id=1))],
    )
    def test_change_type_with_load_balancer_type_id(
        self,
        request_mock: mock.MagicMock,
        load_balancers_client: LoadBalancersClient,
        load_balancer,
        action_response,
    ):
        request_mock.return_value = action_response

        action = load_balancers_client.change_type(
            load_balancer, LoadBalancerType(id=1)
        )

        request_mock.assert_called_with(
            method="POST",
            url="/load_balancers/1/actions/change_type",
            json={"load_balancer_type": 1},
        )

        assert action.id == 1
        assert action.progress == 0
