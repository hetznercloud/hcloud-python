from __future__ import annotations

from unittest import mock

import pytest

from hcloud import Client
from hcloud.datacenters import BoundDatacenter, Datacenter
from hcloud.locations import BoundLocation, Location
from hcloud.primary_ips import BoundPrimaryIP, PrimaryIP, PrimaryIPsClient

from ..conftest import BoundModelTestCase, assert_bound_action1


def assert_bound_primary_ip1(o: BoundPrimaryIP, client: PrimaryIPsClient):
    assert isinstance(o, BoundPrimaryIP)
    assert o._client is client
    assert o.id == 42
    assert o.name == "primary-ip1"


def assert_bound_primary_ip2(o: BoundPrimaryIP, client: PrimaryIPsClient):
    assert isinstance(o, BoundPrimaryIP)
    assert o._client is client
    assert o.id == 52
    assert o.name == "primary-ip2"


class TestBoundPrimaryIP(BoundModelTestCase):
    methods = [
        BoundPrimaryIP.update,
        BoundPrimaryIP.delete,
        BoundPrimaryIP.change_dns_ptr,
        BoundPrimaryIP.change_protection,
        BoundPrimaryIP.assign,
        BoundPrimaryIP.unassign,
    ]

    @pytest.fixture()
    def resource_client(self, client: Client):
        return client.primary_ips

    @pytest.fixture()
    def bound_model(self, resource_client: PrimaryIPsClient):
        return BoundPrimaryIP(resource_client, data=dict(id=14))

    def test_init(self, primary_ip1):
        o = BoundPrimaryIP(client=mock.MagicMock(), data=primary_ip1)

        assert o.id == 42
        assert o.name == "primary-ip1"
        assert o.ip == "131.232.99.1"
        assert o.type == "ipv4"
        assert o.protection == {"delete": False}
        assert o.labels == {"key": "value"}
        assert o.blocked is False

        assert o.assignee_id == 17
        assert o.assignee_type == "server"

        assert isinstance(o.location, BoundLocation)
        assert o.location.id == 1
        assert o.location.name == "fsn1"

        with pytest.deprecated_call():
            datacenter = o.datacenter

        assert isinstance(datacenter, BoundDatacenter)
        assert datacenter.id == 4
        assert datacenter.name == "fsn1-dc14"


class TestPrimaryIPsClient:
    @pytest.fixture()
    def resource_client(self, client: Client):
        return PrimaryIPsClient(client)

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        resource_client: PrimaryIPsClient,
        primary_ip1,
    ):
        request_mock.return_value = {"primary_ip": primary_ip1}

        result = resource_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/primary_ips/1",
        )
        assert_bound_primary_ip1(result, resource_client)

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        resource_client: PrimaryIPsClient,
        primary_ip1,
    ):
        request_mock.return_value = {"primary_ips": [primary_ip1]}

        result = resource_client.get_by_name("primary-ip1")

        request_mock.assert_called_with(
            method="GET",
            url="/primary_ips",
            params={"name": "primary-ip1"},
        )
        assert_bound_primary_ip1(result, resource_client)

    @pytest.mark.parametrize(
        "params",
        [
            {"name": "primary-ip1"},
            {"label_selector": "key=value"},
        ],
    )
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        resource_client: PrimaryIPsClient,
        primary_ip1,
        primary_ip2,
        params,
    ):
        request_mock.return_value = {"primary_ips": [primary_ip1, primary_ip2]}

        result = resource_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/primary_ips",
            params=params,
        )

        assert len(result) == 2
        assert_bound_primary_ip1(result[0], resource_client)
        assert_bound_primary_ip2(result[1], resource_client)

    def test_create_with_location(
        self,
        request_mock: mock.MagicMock,
        resource_client: PrimaryIPsClient,
        primary_ip1,
    ):
        request_mock.return_value = {
            "primary_ip": primary_ip1,
            "action": None,
        }

        result = resource_client.create(
            type="ipv4",
            name="primary-ip1",
            location=Location(name="fsn1"),
        )

        request_mock.assert_called_with(
            method="POST",
            url="/primary_ips",
            json={
                "name": "primary-ip1",
                "type": "ipv4",
                "location": "fsn1",
                "auto_delete": False,
            },
        )
        assert_bound_primary_ip1(result.primary_ip, resource_client)
        assert result.action is None

    def test_create_with_datacenter(
        self,
        request_mock: mock.MagicMock,
        resource_client: PrimaryIPsClient,
        primary_ip1,
    ):
        request_mock.return_value = {
            "primary_ip": primary_ip1,
            "action": None,
        }

        with pytest.deprecated_call():
            result = resource_client.create(
                type="ipv4",
                name="primary-ip1",
                datacenter=Datacenter(name="fsn1-dc14"),
            )

        request_mock.assert_called_with(
            method="POST",
            url="/primary_ips",
            json={
                "name": "primary-ip1",
                "type": "ipv4",
                "datacenter": "fsn1-dc14",
                "auto_delete": False,
            },
        )
        assert_bound_primary_ip1(result.primary_ip, resource_client)
        assert result.action is None

    def test_create_with_assignee_id(
        self,
        request_mock: mock.MagicMock,
        resource_client: PrimaryIPsClient,
        primary_ip1,
        action1_running,
    ):
        request_mock.return_value = {
            "primary_ip": primary_ip1,
            "action": action1_running,
        }

        result = resource_client.create(
            type="ipv4",
            name="primary-ip1",
            assignee_id=17,
            assignee_type="server",
        )

        request_mock.assert_called_with(
            method="POST",
            url="/primary_ips",
            json={
                "name": "primary-ip1",
                "type": "ipv4",
                "assignee_id": 17,
                "assignee_type": "server",
                "auto_delete": False,
            },
        )

        assert_bound_primary_ip1(result.primary_ip, resource_client)
        assert_bound_action1(result.action, resource_client._parent.actions)

    def test_create_with_assignee_type_deprecation(
        self,
        request_mock: mock.MagicMock,
        resource_client: PrimaryIPsClient,
        primary_ip1,
        action1_running,
    ):
        request_mock.return_value = {
            "primary_ip": primary_ip1,
            "action": action1_running,
        }

        with pytest.deprecated_call():
            resource_client.create(
                type="ipv4",
                name="primary-ip1",
                assignee_id=17,
            )

        request_mock.assert_called_with(
            method="POST",
            url="/primary_ips",
            json={
                "name": "primary-ip1",
                "type": "ipv4",
                "assignee_id": 17,
                "assignee_type": "server",
                "auto_delete": False,
            },
        )

    @pytest.mark.parametrize(
        "primary_ip",
        [
            PrimaryIP(id=42),
            BoundPrimaryIP(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_update(
        self,
        request_mock: mock.MagicMock,
        resource_client: PrimaryIPsClient,
        primary_ip,
        primary_ip1,
    ):
        request_mock.return_value = {"primary_ip": primary_ip1}

        result = resource_client.update(
            primary_ip,
            name="changed",
            auto_delete=True,
        )

        request_mock.assert_called_with(
            method="PUT",
            url="/primary_ips/42",
            json={
                "name": "changed",
                "auto_delete": True,
            },
        )
        assert_bound_primary_ip1(result, resource_client)

    @pytest.mark.parametrize(
        "primary_ip",
        [
            PrimaryIP(id=42),
            BoundPrimaryIP(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_delete(
        self,
        request_mock: mock.MagicMock,
        resource_client: PrimaryIPsClient,
        primary_ip,
    ):
        request_mock.return_value = None

        result = resource_client.delete(primary_ip)

        request_mock.assert_called_with(
            method="DELETE",
            url="/primary_ips/42",
        )

        assert result is True

    @pytest.mark.parametrize(
        "primary_ip",
        [
            PrimaryIP(id=42),
            BoundPrimaryIP(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_change_protection(
        self,
        request_mock: mock.MagicMock,
        resource_client: PrimaryIPsClient,
        primary_ip,
        action_response,
    ):
        request_mock.return_value = action_response

        result = resource_client.change_protection(
            primary_ip,
            delete=True,
        )

        request_mock.assert_called_with(
            method="POST",
            url="/primary_ips/42/actions/change_protection",
            json={
                "delete": True,
            },
        )
        assert_bound_action1(result, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "primary_ip",
        [
            PrimaryIP(id=42),
            BoundPrimaryIP(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_assign(
        self,
        request_mock: mock.MagicMock,
        resource_client: PrimaryIPsClient,
        primary_ip,
        action_response,
    ):
        request_mock.return_value = action_response

        result = resource_client.assign(
            primary_ip,
            assignee_id=17,
            assignee_type="server",
        )

        request_mock.assert_called_with(
            method="POST",
            url="/primary_ips/42/actions/assign",
            json={
                "assignee_id": 17,
                "assignee_type": "server",
            },
        )
        assert_bound_action1(result, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "primary_ip",
        [
            PrimaryIP(id=42),
            BoundPrimaryIP(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_unassign(
        self,
        request_mock: mock.MagicMock,
        resource_client: PrimaryIPsClient,
        primary_ip,
        action_response,
    ):
        request_mock.return_value = action_response

        result = resource_client.unassign(primary_ip)

        request_mock.assert_called_with(
            method="POST",
            url="/primary_ips/42/actions/unassign",
        )
        assert_bound_action1(result, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "primary_ip",
        [
            PrimaryIP(id=42),
            BoundPrimaryIP(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_change_dns_ptr(
        self,
        request_mock: mock.MagicMock,
        resource_client: PrimaryIPsClient,
        primary_ip,
        action_response,
    ):
        request_mock.return_value = action_response

        result = resource_client.change_dns_ptr(
            primary_ip,
            ip="1.2.3.4",
            dns_ptr="server02.example.com",
        )

        request_mock.assert_called_with(
            method="POST",
            url="/primary_ips/42/actions/change_dns_ptr",
            json={
                "ip": "1.2.3.4",
                "dns_ptr": "server02.example.com",
            },
        )
        assert_bound_action1(result, resource_client._parent.actions)
