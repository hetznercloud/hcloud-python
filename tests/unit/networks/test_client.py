from __future__ import annotations

from unittest import mock

import pytest
from dateutil.parser import isoparse

from hcloud.actions import BoundAction
from hcloud.networks import (
    BoundNetwork,
    Network,
    NetworkRoute,
    NetworksClient,
    NetworkSubnet,
)
from hcloud.servers import BoundServer


class TestBoundNetwork:
    @pytest.fixture()
    def bound_network(self, hetzner_client):
        return BoundNetwork(client=hetzner_client.networks, data=dict(id=14))

    def test_bound_network_init(self, network_response):
        bound_network = BoundNetwork(
            client=mock.MagicMock(), data=network_response["network"]
        )

        assert bound_network.id == 1
        assert bound_network.created == isoparse("2016-01-30T23:50:11+00:00")
        assert bound_network.name == "mynet"
        assert bound_network.ip_range == "10.0.0.0/16"
        assert bound_network.protection["delete"] is False

        assert len(bound_network.servers) == 1
        assert isinstance(bound_network.servers[0], BoundServer)
        assert bound_network.servers[0].id == 42
        assert bound_network.servers[0].complete is False

        assert len(bound_network.subnets) == 2
        assert isinstance(bound_network.subnets[0], NetworkSubnet)
        assert bound_network.subnets[0].type == NetworkSubnet.TYPE_CLOUD
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
        hetzner_client.request.assert_called_with(
            url="/networks/14/actions",
            method="GET",
            params={"page": 1, "per_page": 50, "sort": "id"},
        )

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == hetzner_client.actions
        assert actions[0].id == 13
        assert actions[0].command == "add_subnet"

    def test_update(self, hetzner_client, bound_network, response_update_network):
        hetzner_client.request.return_value = response_update_network
        network = bound_network.update(name="new-name")
        hetzner_client.request.assert_called_with(
            url="/networks/14", method="PUT", json={"name": "new-name"}
        )

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
        hetzner_client.request.assert_called_with(
            url="/networks/14/actions/change_protection",
            method="POST",
            json={"delete": True},
        )

        assert action.id == 1
        assert action.progress == 0

    def test_add_subnet(self, hetzner_client, bound_network, generic_action):
        hetzner_client.request.return_value = generic_action
        subnet = NetworkSubnet(
            type=NetworkSubnet.TYPE_CLOUD,
            ip_range="10.0.1.0/24",
            network_zone="eu-central",
        )
        action = bound_network.add_subnet(subnet)
        hetzner_client.request.assert_called_with(
            url="/networks/14/actions/add_subnet",
            method="POST",
            json={
                "type": NetworkSubnet.TYPE_CLOUD,
                "ip_range": "10.0.1.0/24",
                "network_zone": "eu-central",
            },
        )

        assert action.id == 1
        assert action.progress == 0

    def test_delete_subnet(self, hetzner_client, bound_network, generic_action):
        hetzner_client.request.return_value = generic_action
        subnet = NetworkSubnet(ip_range="10.0.1.0/24")
        action = bound_network.delete_subnet(subnet)
        hetzner_client.request.assert_called_with(
            url="/networks/14/actions/delete_subnet",
            method="POST",
            json={"ip_range": "10.0.1.0/24"},
        )

        assert action.id == 1
        assert action.progress == 0

    def test_add_route(self, hetzner_client, bound_network, generic_action):
        hetzner_client.request.return_value = generic_action
        route = NetworkRoute(destination="10.100.1.0/24", gateway="10.0.1.1")
        action = bound_network.add_route(route)
        hetzner_client.request.assert_called_with(
            url="/networks/14/actions/add_route",
            method="POST",
            json={"destination": "10.100.1.0/24", "gateway": "10.0.1.1"},
        )

        assert action.id == 1
        assert action.progress == 0

    def test_delete_route(self, hetzner_client, bound_network, generic_action):
        hetzner_client.request.return_value = generic_action
        route = NetworkRoute(destination="10.100.1.0/24", gateway="10.0.1.1")
        action = bound_network.delete_route(route)
        hetzner_client.request.assert_called_with(
            url="/networks/14/actions/delete_route",
            method="POST",
            json={"destination": "10.100.1.0/24", "gateway": "10.0.1.1"},
        )

        assert action.id == 1
        assert action.progress == 0

    def test_change_ip(self, hetzner_client, bound_network, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_network.change_ip_range("10.0.0.0/12")
        hetzner_client.request.assert_called_with(
            url="/networks/14/actions/change_ip_range",
            method="POST",
            json={"ip_range": "10.0.0.0/12"},
        )

        assert action.id == 1
        assert action.progress == 0


class TestNetworksClient:
    @pytest.fixture()
    def networks_client(self):
        return NetworksClient(client=mock.MagicMock())

    @pytest.fixture()
    def network_subnet(self):
        return NetworkSubnet(
            type=NetworkSubnet.TYPE_CLOUD,
            ip_range="10.0.1.0/24",
            network_zone="eu-central",
        )

    @pytest.fixture()
    def network_vswitch_subnet(self):
        return NetworkSubnet(
            type=NetworkSubnet.TYPE_VSWITCH,
            ip_range="10.0.1.0/24",
            network_zone="eu-central",
            vswitch_id=123,
        )

    @pytest.fixture()
    def network_route(self):
        return NetworkRoute(destination="10.100.1.0/24", gateway="10.0.1.1")

    def test_get_by_id(self, networks_client, network_response):
        networks_client._client.request.return_value = network_response
        bound_network = networks_client.get_by_id(1)
        networks_client._client.request.assert_called_with(
            url="/networks/1", method="GET"
        )
        assert bound_network._client is networks_client
        assert bound_network.id == 1
        assert bound_network.name == "mynet"

    @pytest.mark.parametrize(
        "params",
        [{"label_selector": "label1", "page": 1, "per_page": 10}, {"name": ""}, {}],
    )
    def test_get_list(self, networks_client, two_networks_response, params):
        networks_client._client.request.return_value = two_networks_response
        result = networks_client.get_list(**params)
        networks_client._client.request.assert_called_with(
            url="/networks", method="GET", params=params
        )

        bound_networks = result.networks
        assert result.meta is None

        assert len(bound_networks) == 2

        bound_network1 = bound_networks[0]
        bound_network2 = bound_networks[1]

        assert bound_network1._client is networks_client
        assert bound_network1.id == 1
        assert bound_network1.name == "mynet"

        assert bound_network2._client is networks_client
        assert bound_network2.id == 2
        assert bound_network2.name == "myanothernet"

    @pytest.mark.parametrize("params", [{"label_selector": "label1"}])
    def test_get_all(self, networks_client, two_networks_response, params):
        networks_client._client.request.return_value = two_networks_response
        bound_networks = networks_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        networks_client._client.request.assert_called_with(
            url="/networks", method="GET", params=params
        )

        assert len(bound_networks) == 2

        bound_network1 = bound_networks[0]
        bound_network2 = bound_networks[1]

        assert bound_network1._client is networks_client
        assert bound_network1.id == 1
        assert bound_network1.name == "mynet"

        assert bound_network2._client is networks_client
        assert bound_network2.id == 2
        assert bound_network2.name == "myanothernet"

    def test_get_by_name(self, networks_client, one_network_response):
        networks_client._client.request.return_value = one_network_response
        bound_network = networks_client.get_by_name("mynet")

        params = {"name": "mynet"}

        networks_client._client.request.assert_called_with(
            url="/networks", method="GET", params=params
        )

        assert bound_network._client is networks_client
        assert bound_network.id == 1
        assert bound_network.name == "mynet"

    def test_create(self, networks_client, network_create_response):
        networks_client._client.request.return_value = network_create_response
        networks_client.create(name="mynet", ip_range="10.0.0.0/8")
        networks_client._client.request.assert_called_with(
            url="/networks",
            method="POST",
            json={"name": "mynet", "ip_range": "10.0.0.0/8"},
        )

    def test_create_with_expose_routes_to_vswitch(
        self, networks_client, network_create_response_with_expose_routes_to_vswitch
    ):
        networks_client._client.request.return_value = (
            network_create_response_with_expose_routes_to_vswitch
        )
        networks_client.create(
            name="mynet", ip_range="10.0.0.0/8", expose_routes_to_vswitch=True
        )
        networks_client._client.request.assert_called_with(
            url="/networks",
            method="POST",
            json={
                "name": "mynet",
                "ip_range": "10.0.0.0/8",
                "expose_routes_to_vswitch": True,
            },
        )

    def test_create_with_subnet(
        self, networks_client, network_subnet, network_create_response
    ):
        networks_client._client.request.return_value = network_create_response
        networks_client.create(
            name="mynet", ip_range="10.0.0.0/8", subnets=[network_subnet]
        )
        networks_client._client.request.assert_called_with(
            url="/networks",
            method="POST",
            json={
                "name": "mynet",
                "ip_range": "10.0.0.0/8",
                "subnets": [
                    {
                        "type": NetworkSubnet.TYPE_CLOUD,
                        "ip_range": "10.0.1.0/24",
                        "network_zone": "eu-central",
                    }
                ],
            },
        )

    def test_create_with_subnet_vswitch(
        self, networks_client, network_subnet, network_create_response
    ):
        networks_client._client.request.return_value = network_create_response
        network_subnet.type = NetworkSubnet.TYPE_VSWITCH
        network_subnet.vswitch_id = 1000
        networks_client.create(
            name="mynet", ip_range="10.0.0.0/8", subnets=[network_subnet]
        )
        networks_client._client.request.assert_called_with(
            url="/networks",
            method="POST",
            json={
                "name": "mynet",
                "ip_range": "10.0.0.0/8",
                "subnets": [
                    {
                        "type": NetworkSubnet.TYPE_VSWITCH,
                        "ip_range": "10.0.1.0/24",
                        "network_zone": "eu-central",
                        "vswitch_id": 1000,
                    }
                ],
            },
        )

    def test_create_with_route(
        self, networks_client, network_route, network_create_response
    ):
        networks_client._client.request.return_value = network_create_response
        networks_client.create(
            name="mynet", ip_range="10.0.0.0/8", routes=[network_route]
        )
        networks_client._client.request.assert_called_with(
            url="/networks",
            method="POST",
            json={
                "name": "mynet",
                "ip_range": "10.0.0.0/8",
                "routes": [{"destination": "10.100.1.0/24", "gateway": "10.0.1.1"}],
            },
        )

    def test_create_with_route_and_expose_routes_to_vswitch(
        self,
        networks_client,
        network_route,
        network_create_response_with_expose_routes_to_vswitch,
    ):
        networks_client._client.request.return_value = (
            network_create_response_with_expose_routes_to_vswitch
        )
        networks_client.create(
            name="mynet",
            ip_range="10.0.0.0/8",
            routes=[network_route],
            expose_routes_to_vswitch=True,
        )
        networks_client._client.request.assert_called_with(
            url="/networks",
            method="POST",
            json={
                "name": "mynet",
                "ip_range": "10.0.0.0/8",
                "routes": [{"destination": "10.100.1.0/24", "gateway": "10.0.1.1"}],
                "expose_routes_to_vswitch": True,
            },
        )

    def test_create_with_route_and_subnet(
        self, networks_client, network_subnet, network_route, network_create_response
    ):
        networks_client._client.request.return_value = network_create_response
        networks_client.create(
            name="mynet",
            ip_range="10.0.0.0/8",
            subnets=[network_subnet],
            routes=[network_route],
        )
        networks_client._client.request.assert_called_with(
            url="/networks",
            method="POST",
            json={
                "name": "mynet",
                "ip_range": "10.0.0.0/8",
                "subnets": [
                    {
                        "type": NetworkSubnet.TYPE_CLOUD,
                        "ip_range": "10.0.1.0/24",
                        "network_zone": "eu-central",
                    }
                ],
                "routes": [{"destination": "10.100.1.0/24", "gateway": "10.0.1.1"}],
            },
        )

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_get_actions_list(self, networks_client, network, response_get_actions):
        networks_client._client.request.return_value = response_get_actions
        result = networks_client.get_actions_list(network, sort="id")
        networks_client._client.request.assert_called_with(
            url="/networks/1/actions", method="GET", params={"sort": "id"}
        )

        actions = result.actions
        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)

        assert actions[0]._client == networks_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "add_subnet"

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_update(self, networks_client, network, response_update_network):
        networks_client._client.request.return_value = response_update_network
        network = networks_client.update(
            network, name="new-name", expose_routes_to_vswitch=True
        )
        networks_client._client.request.assert_called_with(
            url="/networks/1",
            method="PUT",
            json={"name": "new-name", "expose_routes_to_vswitch": True},
        )

        assert network.id == 4711
        assert network.name == "new-name"
        assert network.expose_routes_to_vswitch is True

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_change_protection(self, networks_client, network, generic_action):
        networks_client._client.request.return_value = generic_action
        action = networks_client.change_protection(network, True)
        networks_client._client.request.assert_called_with(
            url="/networks/1/actions/change_protection",
            method="POST",
            json={"delete": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(self, networks_client, network, generic_action):
        networks_client._client.request.return_value = generic_action
        delete_success = networks_client.delete(network)
        networks_client._client.request.assert_called_with(
            url="/networks/1", method="DELETE"
        )

        assert delete_success is True

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_add_subnet(self, networks_client, network, generic_action, network_subnet):
        networks_client._client.request.return_value = generic_action

        action = networks_client.add_subnet(network, network_subnet)
        networks_client._client.request.assert_called_with(
            url="/networks/1/actions/add_subnet",
            method="POST",
            json={
                "type": NetworkSubnet.TYPE_CLOUD,
                "ip_range": "10.0.1.0/24",
                "network_zone": "eu-central",
            },
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_add_subnet_vswitch(
        self, networks_client, network, generic_action, network_vswitch_subnet
    ):
        networks_client._client.request.return_value = generic_action

        action = networks_client.add_subnet(network, network_vswitch_subnet)
        networks_client._client.request.assert_called_with(
            url="/networks/1/actions/add_subnet",
            method="POST",
            json={
                "type": NetworkSubnet.TYPE_VSWITCH,
                "ip_range": "10.0.1.0/24",
                "network_zone": "eu-central",
                "vswitch_id": 123,
            },
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_delete_subnet(
        self, networks_client, network, generic_action, network_subnet
    ):
        networks_client._client.request.return_value = generic_action

        action = networks_client.delete_subnet(network, network_subnet)
        networks_client._client.request.assert_called_with(
            url="/networks/1/actions/delete_subnet",
            method="POST",
            json={"ip_range": "10.0.1.0/24"},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_add_route(self, networks_client, network, generic_action, network_route):
        networks_client._client.request.return_value = generic_action

        action = networks_client.add_route(network, network_route)
        networks_client._client.request.assert_called_with(
            url="/networks/1/actions/add_route",
            method="POST",
            json={"destination": "10.100.1.0/24", "gateway": "10.0.1.1"},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_delete_route(
        self, networks_client, network, generic_action, network_route
    ):
        networks_client._client.request.return_value = generic_action

        action = networks_client.delete_route(network, network_route)
        networks_client._client.request.assert_called_with(
            url="/networks/1/actions/delete_route",
            method="POST",
            json={"destination": "10.100.1.0/24", "gateway": "10.0.1.1"},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_change_ip_range(self, networks_client, network, generic_action):
        networks_client._client.request.return_value = generic_action
        action = networks_client.change_ip_range(network, "10.0.0.0/12")
        networks_client._client.request.assert_called_with(
            url="/networks/1/actions/change_ip_range",
            method="POST",
            json={"ip_range": "10.0.0.0/12"},
        )

        assert action.id == 1
        assert action.progress == 0

    def test_actions_get_by_id(self, networks_client, response_get_actions):
        networks_client._client.request.return_value = {
            "action": response_get_actions["actions"][0]
        }
        action = networks_client.actions.get_by_id(13)

        networks_client._client.request.assert_called_with(
            url="/networks/actions/13", method="GET"
        )

        assert isinstance(action, BoundAction)
        assert action._client == networks_client._client.actions
        assert action.id == 13
        assert action.command == "add_subnet"

    def test_actions_get_list(self, networks_client, response_get_actions):
        networks_client._client.request.return_value = response_get_actions
        result = networks_client.actions.get_list()

        networks_client._client.request.assert_called_with(
            url="/networks/actions",
            method="GET",
            params={},
        )

        actions = result.actions
        assert result.meta is None

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == networks_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "add_subnet"

    def test_actions_get_all(self, networks_client, response_get_actions):
        networks_client._client.request.return_value = response_get_actions
        actions = networks_client.actions.get_all()

        networks_client._client.request.assert_called_with(
            url="/networks/actions",
            method="GET",
            params={"page": 1, "per_page": 50},
        )

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == networks_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "add_subnet"
