from __future__ import annotations

from unittest import mock

import pytest
from dateutil.parser import isoparse

from hcloud import Client
from hcloud.networks import (
    BoundNetwork,
    Network,
    NetworkRoute,
    NetworksClient,
    NetworkSubnet,
)
from hcloud.servers import BoundServer

from ..conftest import BoundModelTestCase


class TestBoundNetwork(BoundModelTestCase):
    methods = [
        BoundNetwork.update,
        BoundNetwork.delete,
        BoundNetwork.add_subnet,
        BoundNetwork.delete_subnet,
        BoundNetwork.add_route,
        BoundNetwork.delete_route,
        BoundNetwork.change_ip_range,
        BoundNetwork.change_protection,
    ]

    @pytest.fixture()
    def resource_client(self, client: Client):
        return client.networks

    @pytest.fixture()
    def bound_model(self, resource_client: NetworksClient):
        return BoundNetwork(resource_client, data=dict(id=14))

    def test_init(self, network_response):
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


class TestNetworksClient:
    @pytest.fixture()
    def networks_client(self, client: Client):
        return NetworksClient(client)

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

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network_response,
    ):
        request_mock.return_value = network_response

        bound_network = networks_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/networks/1",
        )
        assert bound_network._client is networks_client
        assert bound_network.id == 1
        assert bound_network.name == "mynet"

    @pytest.mark.parametrize(
        "params",
        [{"label_selector": "label1", "page": 1, "per_page": 10}, {"name": ""}, {}],
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        two_networks_response,
        params,
    ):
        request_mock.return_value = two_networks_response

        result = networks_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/networks",
            params=params,
        )

        bound_networks = result.networks
        assert result.meta is not None

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
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        two_networks_response,
        params,
    ):
        request_mock.return_value = two_networks_response

        bound_networks = networks_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/networks",
            params=params,
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

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        one_network_response,
    ):
        request_mock.return_value = one_network_response

        bound_network = networks_client.get_by_name("mynet")

        params = {"name": "mynet"}

        request_mock.assert_called_with(
            method="GET",
            url="/networks",
            params=params,
        )

        assert bound_network._client is networks_client
        assert bound_network.id == 1
        assert bound_network.name == "mynet"

    def test_create(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network_create_response,
    ):
        request_mock.return_value = network_create_response

        networks_client.create(name="mynet", ip_range="10.0.0.0/8")

        request_mock.assert_called_with(
            method="POST",
            url="/networks",
            json={"name": "mynet", "ip_range": "10.0.0.0/8"},
        )

    def test_create_with_expose_routes_to_vswitch(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network_create_response_with_expose_routes_to_vswitch,
    ):
        request_mock.return_value = (
            network_create_response_with_expose_routes_to_vswitch
        )
        networks_client.create(
            name="mynet", ip_range="10.0.0.0/8", expose_routes_to_vswitch=True
        )

        request_mock.assert_called_with(
            method="POST",
            url="/networks",
            json={
                "name": "mynet",
                "ip_range": "10.0.0.0/8",
                "expose_routes_to_vswitch": True,
            },
        )

    def test_create_with_subnet(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network_subnet,
        network_create_response,
    ):
        request_mock.return_value = network_create_response

        networks_client.create(
            name="mynet", ip_range="10.0.0.0/8", subnets=[network_subnet]
        )

        request_mock.assert_called_with(
            method="POST",
            url="/networks",
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
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network_subnet,
        network_create_response,
    ):
        request_mock.return_value = network_create_response

        network_subnet.type = NetworkSubnet.TYPE_VSWITCH
        network_subnet.vswitch_id = 1000
        networks_client.create(
            name="mynet", ip_range="10.0.0.0/8", subnets=[network_subnet]
        )

        request_mock.assert_called_with(
            method="POST",
            url="/networks",
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
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network_route,
        network_create_response,
    ):
        request_mock.return_value = network_create_response

        networks_client.create(
            name="mynet", ip_range="10.0.0.0/8", routes=[network_route]
        )

        request_mock.assert_called_with(
            method="POST",
            url="/networks",
            json={
                "name": "mynet",
                "ip_range": "10.0.0.0/8",
                "routes": [{"destination": "10.100.1.0/24", "gateway": "10.0.1.1"}],
            },
        )

    def test_create_with_route_and_expose_routes_to_vswitch(
        self,
        request_mock: mock.MagicMock,
        networks_client,
        network_route,
        network_create_response_with_expose_routes_to_vswitch,
    ):
        request_mock.return_value = (
            network_create_response_with_expose_routes_to_vswitch
        )
        networks_client.create(
            name="mynet",
            ip_range="10.0.0.0/8",
            routes=[network_route],
            expose_routes_to_vswitch=True,
        )

        request_mock.assert_called_with(
            method="POST",
            url="/networks",
            json={
                "name": "mynet",
                "ip_range": "10.0.0.0/8",
                "routes": [{"destination": "10.100.1.0/24", "gateway": "10.0.1.1"}],
                "expose_routes_to_vswitch": True,
            },
        )

    def test_create_with_route_and_subnet(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network_subnet,
        network_route,
        network_create_response,
    ):
        request_mock.return_value = network_create_response

        networks_client.create(
            name="mynet",
            ip_range="10.0.0.0/8",
            subnets=[network_subnet],
            routes=[network_route],
        )

        request_mock.assert_called_with(
            method="POST",
            url="/networks",
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
    def test_update(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network,
        response_update_network,
    ):
        request_mock.return_value = response_update_network

        network = networks_client.update(
            network, name="new-name", expose_routes_to_vswitch=True
        )

        request_mock.assert_called_with(
            method="PUT",
            url="/networks/1",
            json={"name": "new-name", "expose_routes_to_vswitch": True},
        )

        assert network.id == 4711
        assert network.name == "new-name"
        assert network.expose_routes_to_vswitch is True

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_change_protection(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network,
        action_response,
    ):
        request_mock.return_value = action_response

        action = networks_client.change_protection(network, True)

        request_mock.assert_called_with(
            method="POST",
            url="/networks/1/actions/change_protection",
            json={"delete": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network,
        action_response,
    ):
        request_mock.return_value = action_response

        delete_success = networks_client.delete(network)

        request_mock.assert_called_with(
            method="DELETE",
            url="/networks/1",
        )

        assert delete_success is True

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_add_subnet(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network,
        action_response,
        network_subnet,
    ):
        request_mock.return_value = action_response

        action = networks_client.add_subnet(network, network_subnet)

        request_mock.assert_called_with(
            method="POST",
            url="/networks/1/actions/add_subnet",
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
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network,
        action_response,
        network_vswitch_subnet,
    ):
        request_mock.return_value = action_response

        action = networks_client.add_subnet(network, network_vswitch_subnet)

        request_mock.assert_called_with(
            method="POST",
            url="/networks/1/actions/add_subnet",
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
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network,
        action_response,
        network_subnet,
    ):
        request_mock.return_value = action_response

        action = networks_client.delete_subnet(network, network_subnet)

        request_mock.assert_called_with(
            method="POST",
            url="/networks/1/actions/delete_subnet",
            json={"ip_range": "10.0.1.0/24"},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_add_route(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network,
        action_response,
        network_route,
    ):
        request_mock.return_value = action_response

        action = networks_client.add_route(network, network_route)

        request_mock.assert_called_with(
            method="POST",
            url="/networks/1/actions/add_route",
            json={"destination": "10.100.1.0/24", "gateway": "10.0.1.1"},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_delete_route(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network,
        action_response,
        network_route,
    ):
        request_mock.return_value = action_response

        action = networks_client.delete_route(network, network_route)

        request_mock.assert_called_with(
            method="POST",
            url="/networks/1/actions/delete_route",
            json={"destination": "10.100.1.0/24", "gateway": "10.0.1.1"},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "network", [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=1))]
    )
    def test_change_ip_range(
        self,
        request_mock: mock.MagicMock,
        networks_client: NetworksClient,
        network,
        action_response,
    ):
        request_mock.return_value = action_response

        action = networks_client.change_ip_range(network, "10.0.0.0/12")

        request_mock.assert_called_with(
            method="POST",
            url="/networks/1/actions/change_ip_range",
            json={"ip_range": "10.0.0.0/12"},
        )

        assert action.id == 1
        assert action.progress == 0
