import mock
import pytest
from hcloud.servers.domain import Server
from hcloud.load_balancers.domain import LoadBalancerAlgorithm, LoadBalancer, LoadBalancerTarget, LoadBalancerService, \
    LoadBalancerHealthCheck
from hcloud.load_balancer_types.domain import LoadBalancerType
from hcloud.load_balancers.client import BoundLoadBalancer


class TestBoundLoadBalancer(object):
    @pytest.fixture()
    def bound_load_balancer(self, hetzner_client):
        return BoundLoadBalancer(client=hetzner_client.load_balancers, data=dict(id=42))

    def test_get_actions_list(self, bound_load_balancer):
        result = bound_load_balancer.get_actions_list()
        actions = result.actions

        assert len(actions) == 1
        assert actions[0].id == 13
        assert actions[0].command == "add_service"


class TestLoadBalancersClient(object):
    def test_get_by_id(self, hetzner_client):
        load_balancer = hetzner_client.load_balancers.get_by_id(4711)
        assert load_balancer.id == 4711

    def test_get_by_name(self, hetzner_client):
        load_balancer = hetzner_client.load_balancers.get_by_name("Web Frontend")
        assert load_balancer.id == 4711
        assert load_balancer.name == "Web Frontend"

    def test_get_list(self, hetzner_client):
        result = hetzner_client.load_balancers.get_list()
        load_balancers = result.load_balancers
        assert load_balancers[0].id == 4711

    def test_create(self, hetzner_client):
        resp = hetzner_client.load_balancers.create(
            "Web Frontend",
            load_balancer_type=LoadBalancerType(name="lb1"),
            algorithm=LoadBalancerAlgorithm("round_robin"))
        load_balancer = resp.load_balancer
        assert load_balancer.id == 4711
        assert load_balancer.name == "Web Frontend"

    @pytest.mark.parametrize("load_balancer", [LoadBalancer(id=4711), BoundLoadBalancer(mock.MagicMock(), dict(id=1))])
    def test_get_actions_list(self, hetzner_client, load_balancer):
        result = hetzner_client.load_balancers.get_actions_list(load_balancer)
        actions = result.actions

        assert len(actions) == 1
        assert actions[0].id == 13
        assert actions[0].command == "add_service"

    @pytest.mark.parametrize("load_balancer", [LoadBalancer(id=4711), BoundLoadBalancer(mock.MagicMock(), dict(id=1))])
    def test_update(self, hetzner_client, load_balancer):
        lb = hetzner_client.load_balancers.update(load_balancer, name="new-name", labels={})

        assert lb.id == 4711
        assert lb.name == "new-name"

    @pytest.mark.parametrize("load_balancer", [LoadBalancer(id=4711), BoundLoadBalancer(mock.MagicMock(), dict(id=1))])
    def test_delete(self, hetzner_client, load_balancer):
        response = hetzner_client.load_balancers.delete(load_balancer)
        assert response is True

    @pytest.mark.parametrize("load_balancer", [LoadBalancer(id=4711), BoundLoadBalancer(mock.MagicMock(), dict(id=1))])
    def test_add_target(self, hetzner_client, load_balancer):
        action = hetzner_client.load_balancers.add_target(load_balancer, LoadBalancerTarget(type="server", server=Server(id=1)))
        assert action.id == 13
        assert action.command == "add_target"

    @pytest.mark.parametrize("load_balancer", [LoadBalancer(id=4711), BoundLoadBalancer(mock.MagicMock(), dict(id=1))])
    def test_remove_target(self, hetzner_client, load_balancer):
        action = hetzner_client.load_balancers.remove_target(load_balancer,
                                                             LoadBalancerTarget(type="server", server=Server(id=1)))
        assert action.id == 13
        assert action.command == "remove_target"

    @pytest.mark.parametrize("load_balancer", [LoadBalancer(id=4711), BoundLoadBalancer(mock.MagicMock(), dict(id=1))])
    def test_change_algorithm(self, hetzner_client, load_balancer):
        action = hetzner_client.load_balancers.change_algorithm(load_balancer, LoadBalancerAlgorithm(type="round_robin"))
        assert action.id == 13
        assert action.command == "change_algorithm"

    @pytest.mark.parametrize("load_balancer", [LoadBalancer(id=4711), BoundLoadBalancer(mock.MagicMock(), dict(id=1))])
    def test_add_service(self, hetzner_client, load_balancer):
        action = hetzner_client.load_balancers.add_service(load_balancer,
                                                           LoadBalancerService(protocol="http", listen_port=123, destination_port=124, proxyprotocol=False))
        assert action.id == 13
        assert action.command == "add_service"

    @pytest.mark.parametrize("load_balancer", [LoadBalancer(id=4711), BoundLoadBalancer(mock.MagicMock(), dict(id=1))])
    def test_delete_service(self, hetzner_client, load_balancer):
        action = hetzner_client.load_balancers.delete_service(load_balancer,
                                                              LoadBalancerService(protocol="http", listen_port=123,
                                                                                  destination_port=124,
                                                                                  proxyprotocol=False))
        assert action.id == 13
        assert action.command == "delete_service"

    @pytest.mark.parametrize("load_balancer", [LoadBalancer(id=4711), BoundLoadBalancer(mock.MagicMock(), dict(id=1))])
    def test_update_service(self, hetzner_client, load_balancer):
        action = hetzner_client.load_balancers.update_service(load_balancer,
                                                              LoadBalancerService(protocol="http", listen_port=123,
                                                                                  destination_port=124,
                                                                                  proxyprotocol=False,
                                                                                  health_check=LoadBalancerHealthCheck(protocol='http', port=123, interval=1, timeout=1, retries=1)))
        assert action.id == 13
        assert action.command == "update_service"

    @pytest.mark.parametrize("load_balancer", [LoadBalancer(id=4711), BoundLoadBalancer(mock.MagicMock(), dict(id=1))])
    def test_change_protection(self, hetzner_client, load_balancer):
        action = hetzner_client.load_balancers.change_protection(load_balancer, {"delete": True})
        assert action.command == "change_protection"
