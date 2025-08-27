from __future__ import annotations

from unittest import mock

import pytest

from hcloud import Client
from hcloud.datacenters import BoundDatacenter, Datacenter
from hcloud.primary_ips import BoundPrimaryIP, PrimaryIP, PrimaryIPsClient

from ..conftest import BoundModelTestCase


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

    def test_init(self, primary_ip_response):
        bound_primary_ip = BoundPrimaryIP(
            client=mock.MagicMock(), data=primary_ip_response["primary_ip"]
        )

        assert bound_primary_ip.id == 42
        assert bound_primary_ip.name == "my-resource"
        assert bound_primary_ip.ip == "131.232.99.1"
        assert bound_primary_ip.type == "ipv4"
        assert bound_primary_ip.protection == {"delete": False}
        assert bound_primary_ip.labels == {}
        assert bound_primary_ip.blocked is False

        assert bound_primary_ip.assignee_id == 17
        assert bound_primary_ip.assignee_type == "server"

        assert isinstance(bound_primary_ip.datacenter, BoundDatacenter)
        assert bound_primary_ip.datacenter.id == 42
        assert bound_primary_ip.datacenter.name == "fsn1-dc8"
        assert bound_primary_ip.datacenter.description == "Falkenstein DC Park 8"
        assert bound_primary_ip.datacenter.location.country == "DE"
        assert bound_primary_ip.datacenter.location.city == "Falkenstein"
        assert bound_primary_ip.datacenter.location.latitude == 50.47612
        assert bound_primary_ip.datacenter.location.longitude == 12.370071


class TestPrimaryIPsClient:
    @pytest.fixture()
    def primary_ips_client(self, client: Client):
        return PrimaryIPsClient(client)

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        primary_ips_client: PrimaryIPsClient,
        primary_ip_response,
    ):
        request_mock.return_value = primary_ip_response

        bound_primary_ip = primary_ips_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/primary_ips/1",
        )
        assert bound_primary_ip._client is primary_ips_client
        assert bound_primary_ip.id == 42

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        primary_ips_client: PrimaryIPsClient,
        one_primary_ips_response,
    ):
        request_mock.return_value = one_primary_ips_response

        bound_primary_ip = primary_ips_client.get_by_name("my-resource")

        request_mock.assert_called_with(
            method="GET",
            url="/primary_ips",
            params={"name": "my-resource"},
        )
        assert bound_primary_ip._client is primary_ips_client
        assert bound_primary_ip.id == 42
        assert bound_primary_ip.name == "my-resource"

    @pytest.mark.parametrize("params", [{"label_selector": "label1"}])
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        primary_ips_client: PrimaryIPsClient,
        all_primary_ips_response,
        params,
    ):
        request_mock.return_value = all_primary_ips_response

        bound_primary_ips = primary_ips_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/primary_ips",
            params=params,
        )

        assert len(bound_primary_ips) == 1

        bound_primary_ip1 = bound_primary_ips[0]

        assert bound_primary_ip1._client is primary_ips_client
        assert bound_primary_ip1.id == 42
        assert bound_primary_ip1.name == "my-resource"

    def test_create_with_datacenter(
        self,
        request_mock: mock.MagicMock,
        primary_ips_client: PrimaryIPsClient,
        primary_ip_response,
    ):
        request_mock.return_value = primary_ip_response

        response = primary_ips_client.create(
            type="ipv6", name="my-resource", datacenter=Datacenter(name="datacenter")
        )

        request_mock.assert_called_with(
            method="POST",
            url="/primary_ips",
            json={
                "name": "my-resource",
                "type": "ipv6",
                "assignee_type": "server",
                "datacenter": "datacenter",
                "auto_delete": False,
            },
        )

        bound_primary_ip = response.primary_ip
        action = response.action

        assert bound_primary_ip._client is primary_ips_client
        assert bound_primary_ip.id == 42
        assert bound_primary_ip.name == "my-resource"
        assert action is None

    def test_create_with_assignee_id(
        self,
        request_mock: mock.MagicMock,
        primary_ips_client: PrimaryIPsClient,
        primary_ip_create_response,
    ):
        request_mock.return_value = primary_ip_create_response

        response = primary_ips_client.create(
            type="ipv6",
            name="my-ip",
            assignee_id=17,
            assignee_type="server",
        )

        request_mock.assert_called_with(
            method="POST",
            url="/primary_ips",
            json={
                "name": "my-ip",
                "type": "ipv6",
                "assignee_id": 17,
                "assignee_type": "server",
                "auto_delete": False,
            },
        )
        bound_primary_ip = response.primary_ip
        action = response.action

        assert bound_primary_ip._client is primary_ips_client
        assert bound_primary_ip.id == 42
        assert bound_primary_ip.name == "my-ip"
        assert bound_primary_ip.assignee_id == 17
        assert action.id == 13

    @pytest.mark.parametrize(
        "primary_ip", [PrimaryIP(id=1), BoundPrimaryIP(mock.MagicMock(), dict(id=1))]
    )
    def test_update(
        self,
        request_mock: mock.MagicMock,
        primary_ips_client: PrimaryIPsClient,
        primary_ip,
        response_update_primary_ip,
    ):
        request_mock.return_value = response_update_primary_ip

        primary_ip = primary_ips_client.update(
            primary_ip, auto_delete=True, name="my-resource"
        )

        request_mock.assert_called_with(
            method="PUT",
            url="/primary_ips/1",
            json={"auto_delete": True, "name": "my-resource"},
        )

        assert primary_ip.id == 42
        assert primary_ip.auto_delete is True
        assert primary_ip.name == "my-resource"

    @pytest.mark.parametrize(
        "primary_ip", [PrimaryIP(id=1), BoundPrimaryIP(mock.MagicMock(), dict(id=1))]
    )
    def test_change_protection(
        self,
        request_mock: mock.MagicMock,
        primary_ips_client: PrimaryIPsClient,
        primary_ip,
        action_response,
    ):
        request_mock.return_value = action_response

        action = primary_ips_client.change_protection(primary_ip, True)

        request_mock.assert_called_with(
            method="POST",
            url="/primary_ips/1/actions/change_protection",
            json={"delete": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "primary_ip", [PrimaryIP(id=1), BoundPrimaryIP(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(
        self,
        request_mock: mock.MagicMock,
        primary_ips_client: PrimaryIPsClient,
        primary_ip,
        action_response,
    ):
        request_mock.return_value = action_response

        delete_success = primary_ips_client.delete(primary_ip)

        request_mock.assert_called_with(
            method="DELETE",
            url="/primary_ips/1",
        )

        assert delete_success is True

    @pytest.mark.parametrize(
        "assignee_id,assignee_type,primary_ip",
        [
            (1, "server", PrimaryIP(id=12)),
            (1, "server", BoundPrimaryIP(mock.MagicMock(), dict(id=12))),
        ],
    )
    def test_assign(
        self,
        request_mock: mock.MagicMock,
        primary_ips_client: PrimaryIPsClient,
        assignee_id,
        assignee_type,
        primary_ip,
        action_response,
    ):
        request_mock.return_value = action_response

        action = primary_ips_client.assign(primary_ip, assignee_id, assignee_type)

        request_mock.assert_called_with(
            method="POST",
            url="/primary_ips/12/actions/assign",
            json={"assignee_id": 1, "assignee_type": "server"},
        )
        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "primary_ip", [PrimaryIP(id=12), BoundPrimaryIP(mock.MagicMock(), dict(id=12))]
    )
    def test_unassign(
        self,
        request_mock: mock.MagicMock,
        primary_ips_client: PrimaryIPsClient,
        primary_ip,
        action_response,
    ):
        request_mock.return_value = action_response

        action = primary_ips_client.unassign(primary_ip)

        request_mock.assert_called_with(
            method="POST",
            url="/primary_ips/12/actions/unassign",
        )
        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "primary_ip", [PrimaryIP(id=12), BoundPrimaryIP(mock.MagicMock(), dict(id=12))]
    )
    def test_change_dns_ptr(
        self,
        request_mock: mock.MagicMock,
        primary_ips_client: PrimaryIPsClient,
        primary_ip,
        action_response,
    ):
        request_mock.return_value = action_response

        action = primary_ips_client.change_dns_ptr(
            primary_ip, "1.2.3.4", "server02.example.com"
        )

        request_mock.assert_called_with(
            method="POST",
            url="/primary_ips/12/actions/change_dns_ptr",
            json={"ip": "1.2.3.4", "dns_ptr": "server02.example.com"},
        )
        assert action.id == 1
        assert action.progress == 0
