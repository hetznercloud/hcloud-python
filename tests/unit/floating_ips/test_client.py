from __future__ import annotations

from unittest import mock

import pytest

from hcloud import Client
from hcloud.floating_ips import BoundFloatingIP, FloatingIP, FloatingIPsClient
from hcloud.locations import BoundLocation, Location
from hcloud.servers import BoundServer, Server

from ..conftest import BoundModelTestCase


class TestBoundFloatingIP(BoundModelTestCase):
    methods = [
        BoundFloatingIP.update,
        BoundFloatingIP.delete,
        BoundFloatingIP.change_protection,
        BoundFloatingIP.change_dns_ptr,
        BoundFloatingIP.assign,
        BoundFloatingIP.unassign,
    ]

    @pytest.fixture()
    def resource_client(self, client: Client):
        return client.floating_ips

    @pytest.fixture()
    def bound_model(self, resource_client, floating_ip_response):
        return BoundFloatingIP(
            resource_client, data=floating_ip_response["floating_ip"]
        )

    def test_init(self, bound_model: BoundFloatingIP):
        o = bound_model
        assert o.id == 4711
        assert o.description == "Web Frontend"
        assert o.name == "Web Frontend"
        assert o.ip == "131.232.99.1"
        assert o.type == "ipv4"
        assert o.protection == {"delete": False}
        assert o.labels == {}
        assert o.blocked is False

        assert isinstance(o.server, BoundServer)
        assert o.server.id == 42

        assert isinstance(o.home_location, BoundLocation)
        assert o.home_location.id == 1
        assert o.home_location.name == "fsn1"
        assert o.home_location.description == "Falkenstein DC Park 1"
        assert o.home_location.country == "DE"
        assert o.home_location.city == "Falkenstein"
        assert o.home_location.latitude == 50.47612
        assert o.home_location.longitude == 12.370071


class TestFloatingIPsClient:
    @pytest.fixture()
    def floating_ips_client(self, client: Client):
        return FloatingIPsClient(client)

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        floating_ips_client: FloatingIPsClient,
        floating_ip_response,
    ):
        request_mock.return_value = floating_ip_response

        bound_floating_ip = floating_ips_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/floating_ips/1",
        )
        assert bound_floating_ip._client is floating_ips_client
        assert bound_floating_ip.id == 4711
        assert bound_floating_ip.description == "Web Frontend"

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        floating_ips_client: FloatingIPsClient,
        one_floating_ips_response,
    ):
        request_mock.return_value = one_floating_ips_response

        bound_floating_ip = floating_ips_client.get_by_name("Web Frontend")

        request_mock.assert_called_with(
            method="GET",
            url="/floating_ips",
            params={"name": "Web Frontend"},
        )
        assert bound_floating_ip._client is floating_ips_client
        assert bound_floating_ip.id == 4711
        assert bound_floating_ip.name == "Web Frontend"
        assert bound_floating_ip.description == "Web Frontend"

    @pytest.mark.parametrize(
        "params",
        [{"label_selector": "label1", "page": 1, "per_page": 10}, {"name": ""}, {}],
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        floating_ips_client: FloatingIPsClient,
        two_floating_ips_response,
        params,
    ):
        request_mock.return_value = two_floating_ips_response

        result = floating_ips_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/floating_ips",
            params=params,
        )

        bound_floating_ips = result.floating_ips
        assert result.meta is not None

        assert len(bound_floating_ips) == 2

        bound_floating_ip1 = bound_floating_ips[0]
        bound_floating_ip2 = bound_floating_ips[1]

        assert bound_floating_ip1._client is floating_ips_client
        assert bound_floating_ip1.id == 4711
        assert bound_floating_ip1.description == "Web Frontend"

        assert bound_floating_ip2._client is floating_ips_client
        assert bound_floating_ip2.id == 4712
        assert bound_floating_ip2.description == "Web Backend"

    @pytest.mark.parametrize("params", [{"label_selector": "label1"}, {}])
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        floating_ips_client: FloatingIPsClient,
        two_floating_ips_response,
        params,
    ):
        request_mock.return_value = two_floating_ips_response

        bound_floating_ips = floating_ips_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/floating_ips",
            params=params,
        )

        assert len(bound_floating_ips) == 2

        bound_floating_ip1 = bound_floating_ips[0]
        bound_floating_ip2 = bound_floating_ips[1]

        assert bound_floating_ip1._client is floating_ips_client
        assert bound_floating_ip1.id == 4711
        assert bound_floating_ip1.description == "Web Frontend"

        assert bound_floating_ip2._client is floating_ips_client
        assert bound_floating_ip2.id == 4712
        assert bound_floating_ip2.description == "Web Backend"

    def test_create_with_location(
        self,
        request_mock: mock.MagicMock,
        floating_ips_client: FloatingIPsClient,
        floating_ip_response,
    ):
        request_mock.return_value = floating_ip_response

        response = floating_ips_client.create(
            "ipv6", "Web Frontend", home_location=Location(name="location")
        )

        request_mock.assert_called_with(
            method="POST",
            url="/floating_ips",
            json={
                "description": "Web Frontend",
                "type": "ipv6",
                "home_location": "location",
            },
        )

        bound_floating_ip = response.floating_ip
        action = response.action

        assert bound_floating_ip._client is floating_ips_client
        assert bound_floating_ip.id == 4711
        assert bound_floating_ip.description == "Web Frontend"
        assert action is None

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_create_with_server(
        self,
        request_mock: mock.MagicMock,
        floating_ips_client: FloatingIPsClient,
        server,
        floating_ip_create_response,
    ):
        request_mock.return_value = floating_ip_create_response

        response = floating_ips_client.create(
            type="ipv6", description="Web Frontend", server=server
        )

        request_mock.assert_called_with(
            method="POST",
            url="/floating_ips",
            json={"description": "Web Frontend", "type": "ipv6", "server": 1},
        )
        bound_floating_ip = response.floating_ip
        action = response.action

        assert bound_floating_ip._client is floating_ips_client
        assert bound_floating_ip.id == 4711
        assert bound_floating_ip.description == "Web Frontend"
        assert action.id == 13

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_create_with_name(
        self,
        request_mock: mock.MagicMock,
        floating_ips_client: FloatingIPsClient,
        server,
        floating_ip_create_response,
    ):
        request_mock.return_value = floating_ip_create_response

        response = floating_ips_client.create(
            type="ipv6", description="Web Frontend", name="Web Frontend"
        )

        request_mock.assert_called_with(
            method="POST",
            url="/floating_ips",
            json={
                "description": "Web Frontend",
                "type": "ipv6",
                "name": "Web Frontend",
            },
        )
        bound_floating_ip = response.floating_ip
        action = response.action

        assert bound_floating_ip._client is floating_ips_client
        assert bound_floating_ip.id == 4711
        assert bound_floating_ip.description == "Web Frontend"
        assert bound_floating_ip.name == "Web Frontend"
        assert action.id == 13

    @pytest.mark.parametrize(
        "floating_ip", [FloatingIP(id=1), BoundFloatingIP(mock.MagicMock(), dict(id=1))]
    )
    def test_update(
        self,
        request_mock: mock.MagicMock,
        floating_ips_client: FloatingIPsClient,
        floating_ip,
        response_update_floating_ip,
    ):
        request_mock.return_value = response_update_floating_ip

        floating_ip = floating_ips_client.update(
            floating_ip, description="New description", name="New name"
        )

        request_mock.assert_called_with(
            method="PUT",
            url="/floating_ips/1",
            json={"description": "New description", "name": "New name"},
        )

        assert floating_ip.id == 4711
        assert floating_ip.description == "New description"
        assert floating_ip.name == "New name"

    @pytest.mark.parametrize(
        "floating_ip", [FloatingIP(id=1), BoundFloatingIP(mock.MagicMock(), dict(id=1))]
    )
    def test_change_protection(
        self,
        request_mock: mock.MagicMock,
        floating_ips_client: FloatingIPsClient,
        floating_ip,
        action_response,
    ):
        request_mock.return_value = action_response

        action = floating_ips_client.change_protection(floating_ip, True)

        request_mock.assert_called_with(
            method="POST",
            url="/floating_ips/1/actions/change_protection",
            json={"delete": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "floating_ip", [FloatingIP(id=1), BoundFloatingIP(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(
        self,
        request_mock: mock.MagicMock,
        floating_ips_client: FloatingIPsClient,
        floating_ip,
        action_response,
    ):
        request_mock.return_value = action_response

        delete_success = floating_ips_client.delete(floating_ip)

        request_mock.assert_called_with(
            method="DELETE",
            url="/floating_ips/1",
        )

        assert delete_success is True

    @pytest.mark.parametrize(
        "server,floating_ip",
        [
            (Server(id=1), FloatingIP(id=12)),
            (
                BoundServer(mock.MagicMock(), dict(id=1)),
                BoundFloatingIP(mock.MagicMock(), dict(id=12)),
            ),
        ],
    )
    def test_assign(
        self,
        request_mock: mock.MagicMock,
        floating_ips_client: FloatingIPsClient,
        server,
        floating_ip,
        action_response,
    ):
        request_mock.return_value = action_response

        action = floating_ips_client.assign(floating_ip, server)

        request_mock.assert_called_with(
            method="POST",
            url="/floating_ips/12/actions/assign",
            json={"server": 1},
        )
        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "floating_ip",
        [FloatingIP(id=12), BoundFloatingIP(mock.MagicMock(), dict(id=12))],
    )
    def test_unassign(
        self,
        request_mock: mock.MagicMock,
        floating_ips_client: FloatingIPsClient,
        floating_ip,
        action_response,
    ):
        request_mock.return_value = action_response

        action = floating_ips_client.unassign(floating_ip)

        request_mock.assert_called_with(
            method="POST",
            url="/floating_ips/12/actions/unassign",
        )
        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "floating_ip",
        [FloatingIP(id=12), BoundFloatingIP(mock.MagicMock(), dict(id=12))],
    )
    def test_change_dns_ptr(
        self,
        request_mock: mock.MagicMock,
        floating_ips_client: FloatingIPsClient,
        floating_ip,
        action_response,
    ):
        request_mock.return_value = action_response

        action = floating_ips_client.change_dns_ptr(
            floating_ip, "1.2.3.4", "server02.example.com"
        )

        request_mock.assert_called_with(
            method="POST",
            url="/floating_ips/12/actions/change_dns_ptr",
            json={"ip": "1.2.3.4", "dns_ptr": "server02.example.com"},
        )
        assert action.id == 1
        assert action.progress == 0
