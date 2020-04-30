import mock
import pytest

from hcloud.networks.client import BoundNetwork
from hcloud.networks.domain import Network, NetworkSubnet, NetworkRoute


class TestBoundNetwork(object):

    @pytest.fixture()
    def bound_network(self, hetzner_client):
        return BoundNetwork(client=hetzner_client.networks, data=dict(id=4711))

    @pytest.fixture()
    def network_subnet(self):
        return NetworkSubnet(type="cloud", ip_range="10.0.1.0/24", network_zone="eu-central")

    @pytest.fixture()
    def network_route(self):
        return NetworkRoute(destination="10.100.1.0/24", gateway="10.0.1.1")

    def test_get_actions_list(self, bound_network):
        result = bound_network.get_actions_list()
        actions = result.actions

        assert len(actions) == 1
        assert actions[0].id == 13
        assert actions[0].command == "add_subnet"

    def test_update(self, bound_network):
        network = bound_network.update(name="new-name", labels={})
        assert network.id == 4711
        assert network.name == "new-name"

    def test_delete(self, bound_network):
        resp = bound_network.delete()
        assert resp is True

    def test_change_protection(self, bound_network):
        action = bound_network.change_protection(True)

        assert action.id == 13
        assert action.command == "change_protection"

    def test_add_subnet(self, bound_network, network_subnet):
        action = bound_network.add_subnet(network_subnet)

        assert action.id == 13
        assert action.command == "add_subnet"

    def test_delete_subnet(self, bound_network, network_subnet):
        action = bound_network.delete_subnet(network_subnet)

        assert action.id == 13
        assert action.command == "delete_subnet"

    def test_add_route(self, bound_network, network_route):
        action = bound_network.add_route(network_route)

        assert action.id == 13
        assert action.command == "add_route"

    def test_delete_route(self, bound_network, network_route):
        action = bound_network.delete_route(network_route)

        assert action.id == 13
        assert action.command == "delete_route"

    def test_change_ip_range(self, bound_network, ):
        action = bound_network.change_ip_range("10.0.0.0/12")

        assert action.id == 13
        assert action.command == "change_ip_range"


class TestNetworksClient(object):

    @pytest.fixture()
    def network_subnet(self):
        return NetworkSubnet(type="cloud", ip_range="10.0.1.0/24", network_zone="eu-central")

    @pytest.fixture()
    def network_route(self):
        return NetworkRoute(destination="10.100.1.0/24", gateway="10.0.1.1")

    def test_get_by_id(self, hetzner_client):
        network = hetzner_client.networks.get_by_id(4711)
        assert network.id == 4711
        assert network.name == "mynet"
        assert network.ip_range == "10.0.0.0/16"
        assert len(network.subnets) == 1
        assert len(network.routes) == 1
        assert len(network.servers) == 1
        assert network.protection['delete'] is False

    def test_get_by_name(self, hetzner_client):
        network = hetzner_client.networks.get_by_name("mynet")
        assert network.id == 4711
        assert network.name == "mynet"
        assert network.ip_range == "10.0.0.0/16"
        assert len(network.subnets) == 1
        assert len(network.routes) == 1
        assert len(network.servers) == 1
        assert network.protection['delete'] is False

    def test_get_list(self, hetzner_client):
        result = hetzner_client.networks.get_list()
        networks = result.networks
        assert networks[0].id == 4711
        assert networks[0].name == "mynet"
        assert networks[0].ip_range == "10.0.0.0/16"
        assert len(networks[0].subnets) == 1
        assert len(networks[0].routes) == 1
        assert len(networks[0].servers) == 1
        assert networks[0].protection['delete'] is False

    def test_get_all(self, hetzner_client):
        networks = hetzner_client.networks.get_all()
        assert networks[0].id == 4711
        assert networks[0].name == "mynet"
        assert networks[0].ip_range == "10.0.0.0/16"
        assert len(networks[0].subnets) == 1
        assert len(networks[0].routes) == 1
        assert len(networks[0].servers) == 1
        assert networks[0].protection['delete'] is False

    def test_create(self, hetzner_client, network_subnet, network_route):
        network = hetzner_client.networks.create(name="mynet", ip_range="10.0.0.0/16", subnets=[network_subnet],
                                                 routes=[network_route])
        assert network.id == 4711
        assert network.name == "mynet"
        assert network.ip_range == "10.0.0.0/16"
        assert len(network.subnets) == 1
        assert len(network.routes) == 1
        assert len(network.servers) == 1
        assert network.protection['delete'] is False

    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_get_actions_list(self, hetzner_client, network):
        result = hetzner_client.networks.get_actions_list(network)
        actions = result.actions

        assert len(actions) == 1
        assert actions[0].id == 13
        assert actions[0].command == "add_subnet"

    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_update(self, hetzner_client, network):
        network = hetzner_client.networks.update(network, name="new-name", labels={})

        assert network.id == 4711
        assert network.name == "new-name"

    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_delete(self, hetzner_client, network):
        result = hetzner_client.networks.delete(network)

        assert result is True

    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_change_protection(self, hetzner_client, network):
        action = hetzner_client.networks.change_protection(network, delete=True)

        assert action.id == 13
        assert action.command == "change_protection"

    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_add_subnet(self, hetzner_client, network, network_subnet):
        action = hetzner_client.networks.add_subnet(network, network_subnet)

        assert action.id == 13
        assert action.command == "add_subnet"

    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_delete_subnet(self, hetzner_client, network, network_subnet):
        action = hetzner_client.networks.delete_subnet(network, network_subnet)

        assert action.id == 13
        assert action.command == "delete_subnet"

    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_add_route(self, hetzner_client, network, network_route):
        action = hetzner_client.networks.add_route(network, network_route)

        assert action.id == 13
        assert action.command == "add_route"

    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_delete_route(self, hetzner_client, network, network_route):
        action = hetzner_client.networks.delete_route(network, network_route)

        assert action.id == 13
        assert action.command == "delete_route"

    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_change_ip_range(self, hetzner_client, network):
        action = hetzner_client.networks.change_ip_range(network, "10.0.0.0/12")

        assert action.id == 13
        assert action.command == "change_ip_range"
