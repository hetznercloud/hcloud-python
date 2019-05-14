import pytest
from dateutil.parser import isoparse
import mock

from hcloud.actions.client import BoundAction
from hcloud.networks.client import BoundNetwork
from hcloud.networks.domain import NetworkSubnet, NetworkRoute
from hcloud.servers.client import BoundServer


class TestBoundNetwork(object):

    @pytest.fixture()
    def bound_network(self, hetzner_client):
        return BoundNetwork(client=hetzner_client.networks, data=dict(id=14))

    def test_bound_network_init(self, network_response):
        bound_network = BoundNetwork(
            client=mock.MagicMock(),
            data=network_response['network']
        )

        assert bound_network.id == 1
        assert bound_network.created == isoparse("2016-01-30T23:50:11+00:00")
        assert bound_network.name == "mynet"
        assert bound_network.ip_range == "10.0.0.0/16"
        assert bound_network.protection['delete'] is False

        assert len(bound_network.servers) == 1
        assert isinstance(bound_network.servers[0], BoundServer)
        assert bound_network.servers[0].id == 42
        assert bound_network.servers[0].complete is False

        assert len(bound_network.subnets) == 2
        assert isinstance(bound_network.subnets[0], NetworkSubnet)
        assert bound_network.subnets[0].type == "server"
        assert bound_network.subnets[0].ip_range == "10.0.1.0/24"
        assert bound_network.subnets[0].network_zone == "eu-central"
        assert bound_network.subnets[0].gateway == "10.0.0.1"

        assert len(bound_network.routes) == 1
        assert isinstance(bound_network.routes[0], NetworkRoute)
        assert bound_network.routes[0].destination == "10.100.1.0/24"
        assert bound_network.routes[0].gateway == "10.0.1.1"

    def test_get_actions(self, hetzner_client, bound_network, response_get_actions):
        hetzner_client.request.return_value = response_get_actions
        actions = bound_network.get_actions(sort="id")
        hetzner_client.request.assert_called_with(url="/networks/14/actions", method="GET",
                                                  params={"page": 1, "per_page": 50, "sort": "id"})

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0].id == 13
        assert actions[0].command == "add_subnet"

    def test_update(self, hetzner_client, bound_network, response_update_network):
        hetzner_client.request.return_value = response_update_network
        network = bound_network.update(name="new-name")
        hetzner_client.request.assert_called_with(url="/networks/14", method="PUT", json={"name": "new-name"})

        assert network.id == 4711
        assert network.name == "new-name"

    def test_delete(self, hetzner_client, bound_network, generic_action):
        hetzner_client.request.return_value = generic_action
        delete_success = bound_network.delete()
        hetzner_client.request.assert_called_with(url="/networks/14", method="DELETE")

        assert delete_success is True

    def test_change_protection(self, hetzner_client, bound_network, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_network.change_protection(True)
        hetzner_client.request.assert_called_with(url="/networks/14/actions/change_protection", method="POST",
                                                  json={"delete": True})

        assert action.id == 1
        assert action.progress == 0

    def test_add_subnet(self, hetzner_client, bound_network, generic_action):
        hetzner_client.request.return_value = generic_action
        subnet = NetworkSubnet(type="server", ip_range="10.0.1.0/24", network_zone="eu-central")
        action = bound_network.add_subnet(subnet)
        hetzner_client.request.assert_called_with(url="/networks/14/actions/add_subnet", method="POST",
                                                  json={"type": "server", "ip_range": "10.0.1.0/24",
                                                        "network_zone": "eu-central"})

        assert action.id == 1
        assert action.progress == 0

    def test_delete_subnet(self, hetzner_client, bound_network, generic_action):
        hetzner_client.request.return_value = generic_action
        subnet = NetworkSubnet(ip_range="10.0.1.0/24")
        action = bound_network.delete_subnet(subnet)
        hetzner_client.request.assert_called_with(url="/networks/14/actions/delete_subnet", method="POST",
                                                  json={"ip_range": "10.0.1.0/24"})

        assert action.id == 1
        assert action.progress == 0

    def test_add_route(self, hetzner_client, bound_network, generic_action):
        hetzner_client.request.return_value = generic_action
        route = NetworkRoute(destination="10.100.1.0/24", gateway="10.0.1.1")
        action = bound_network.add_route(route)
        hetzner_client.request.assert_called_with(url="/networks/14/actions/add_route", method="POST",
                                                  json={"destination": "10.100.1.0/24", "gateway": "10.0.1.1"})

        assert action.id == 1
        assert action.progress == 0

    def test_delete_route(self, hetzner_client, bound_network, generic_action):
        hetzner_client.request.return_value = generic_action
        route = NetworkRoute(destination="10.100.1.0/24", gateway="10.0.1.1")
        action = bound_network.delete_route(route)
        hetzner_client.request.assert_called_with(url="/networks/14/actions/delete_route", method="POST",
                                                  json={"destination": "10.100.1.0/24", "gateway": "10.0.1.1"})

        assert action.id == 1
        assert action.progress == 0
