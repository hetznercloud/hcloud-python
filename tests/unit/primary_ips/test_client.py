from __future__ import annotations

from unittest import mock

import pytest

from hcloud.actions import BoundAction
from hcloud.datacenters import BoundDatacenter, Datacenter
from hcloud.primary_ips import BoundPrimaryIP, PrimaryIP, PrimaryIPsClient


class TestBoundPrimaryIP:
    @pytest.fixture()
    def bound_primary_ip(self, hetzner_client):
        return BoundPrimaryIP(client=hetzner_client.primary_ips, data=dict(id=14))

    def test_bound_primary_ip_init(self, primary_ip_response):
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

    def test_update(self, hetzner_client, bound_primary_ip, response_update_primary_ip):
        hetzner_client.request.return_value = response_update_primary_ip
        primary_ip = bound_primary_ip.update(auto_delete=True, name="my-resource")
        hetzner_client.request.assert_called_with(
            url="/primary_ips/14",
            method="PUT",
            json={"auto_delete": True, "name": "my-resource"},
        )

        assert primary_ip.id == 42
        assert primary_ip.auto_delete is True

    def test_delete(self, hetzner_client, bound_primary_ip, generic_action):
        hetzner_client.request.return_value = generic_action
        delete_success = bound_primary_ip.delete()
        hetzner_client.request.assert_called_with(
            url="/primary_ips/14", method="DELETE"
        )

        assert delete_success is True

    def test_change_protection(self, hetzner_client, bound_primary_ip, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_primary_ip.change_protection(True)
        hetzner_client.request.assert_called_with(
            url="/primary_ips/14/actions/change_protection",
            method="POST",
            json={"delete": True},
        )

        assert action.id == 1
        assert action.progress == 0

    def test_assign(self, hetzner_client, bound_primary_ip, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_primary_ip.assign(assignee_id=12, assignee_type="server")
        hetzner_client.request.assert_called_with(
            url="/primary_ips/14/actions/assign",
            method="POST",
            json={"assignee_id": 12, "assignee_type": "server"},
        )
        assert action.id == 1
        assert action.progress == 0

    def test_unassign(self, hetzner_client, bound_primary_ip, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_primary_ip.unassign()
        hetzner_client.request.assert_called_with(
            url="/primary_ips/14/actions/unassign", method="POST"
        )
        assert action.id == 1
        assert action.progress == 0

    def test_change_dns_ptr(self, hetzner_client, bound_primary_ip, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_primary_ip.change_dns_ptr("1.2.3.4", "server02.example.com")
        hetzner_client.request.assert_called_with(
            url="/primary_ips/14/actions/change_dns_ptr",
            method="POST",
            json={"ip": "1.2.3.4", "dns_ptr": "server02.example.com"},
        )
        assert action.id == 1
        assert action.progress == 0


class TestPrimaryIPsClient:
    @pytest.fixture()
    def primary_ips_client(self):
        return PrimaryIPsClient(client=mock.MagicMock())

    def test_get_by_id(self, primary_ips_client, primary_ip_response):
        primary_ips_client._client.request.return_value = primary_ip_response
        bound_primary_ip = primary_ips_client.get_by_id(1)
        primary_ips_client._client.request.assert_called_with(
            url="/primary_ips/1", method="GET"
        )
        assert bound_primary_ip._client is primary_ips_client
        assert bound_primary_ip.id == 42

    def test_get_by_name(self, primary_ips_client, one_primary_ips_response):
        primary_ips_client._client.request.return_value = one_primary_ips_response
        bound_primary_ip = primary_ips_client.get_by_name("my-resource")
        primary_ips_client._client.request.assert_called_with(
            url="/primary_ips", method="GET", params={"name": "my-resource"}
        )
        assert bound_primary_ip._client is primary_ips_client
        assert bound_primary_ip.id == 42
        assert bound_primary_ip.name == "my-resource"

    @pytest.mark.parametrize("params", [{"label_selector": "label1"}])
    def test_get_all(self, primary_ips_client, all_primary_ips_response, params):
        primary_ips_client._client.request.return_value = all_primary_ips_response
        bound_primary_ips = primary_ips_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        primary_ips_client._client.request.assert_called_with(
            url="/primary_ips", method="GET", params=params
        )

        assert len(bound_primary_ips) == 1

        bound_primary_ip1 = bound_primary_ips[0]

        assert bound_primary_ip1._client is primary_ips_client
        assert bound_primary_ip1.id == 42
        assert bound_primary_ip1.name == "my-resource"

    def test_create_with_datacenter(self, primary_ips_client, primary_ip_response):
        primary_ips_client._client.request.return_value = primary_ip_response
        response = primary_ips_client.create(
            type="ipv6", name="my-resource", datacenter=Datacenter(name="datacenter")
        )
        primary_ips_client._client.request.assert_called_with(
            url="/primary_ips",
            method="POST",
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
        self, primary_ips_client, primary_ip_create_response
    ):
        primary_ips_client._client.request.return_value = primary_ip_create_response
        response = primary_ips_client.create(
            type="ipv6",
            name="my-ip",
            assignee_id=17,
            assignee_type="server",
        )
        primary_ips_client._client.request.assert_called_with(
            url="/primary_ips",
            method="POST",
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
    def test_update(self, primary_ips_client, primary_ip, response_update_primary_ip):
        primary_ips_client._client.request.return_value = response_update_primary_ip
        primary_ip = primary_ips_client.update(
            primary_ip, auto_delete=True, name="my-resource"
        )
        primary_ips_client._client.request.assert_called_with(
            url="/primary_ips/1",
            method="PUT",
            json={"auto_delete": True, "name": "my-resource"},
        )

        assert primary_ip.id == 42
        assert primary_ip.auto_delete is True
        assert primary_ip.name == "my-resource"

    @pytest.mark.parametrize(
        "primary_ip", [PrimaryIP(id=1), BoundPrimaryIP(mock.MagicMock(), dict(id=1))]
    )
    def test_change_protection(self, primary_ips_client, primary_ip, generic_action):
        primary_ips_client._client.request.return_value = generic_action
        action = primary_ips_client.change_protection(primary_ip, True)
        primary_ips_client._client.request.assert_called_with(
            url="/primary_ips/1/actions/change_protection",
            method="POST",
            json={"delete": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "primary_ip", [PrimaryIP(id=1), BoundPrimaryIP(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(self, primary_ips_client, primary_ip, generic_action):
        primary_ips_client._client.request.return_value = generic_action
        delete_success = primary_ips_client.delete(primary_ip)
        primary_ips_client._client.request.assert_called_with(
            url="/primary_ips/1", method="DELETE"
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
        self, primary_ips_client, assignee_id, assignee_type, primary_ip, generic_action
    ):
        primary_ips_client._client.request.return_value = generic_action
        action = primary_ips_client.assign(primary_ip, assignee_id, assignee_type)
        primary_ips_client._client.request.assert_called_with(
            url="/primary_ips/12/actions/assign",
            method="POST",
            json={"assignee_id": 1, "assignee_type": "server"},
        )
        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "primary_ip", [PrimaryIP(id=12), BoundPrimaryIP(mock.MagicMock(), dict(id=12))]
    )
    def test_unassign(self, primary_ips_client, primary_ip, generic_action):
        primary_ips_client._client.request.return_value = generic_action
        action = primary_ips_client.unassign(primary_ip)
        primary_ips_client._client.request.assert_called_with(
            url="/primary_ips/12/actions/unassign", method="POST"
        )
        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "primary_ip", [PrimaryIP(id=12), BoundPrimaryIP(mock.MagicMock(), dict(id=12))]
    )
    def test_change_dns_ptr(self, primary_ips_client, primary_ip, generic_action):
        primary_ips_client._client.request.return_value = generic_action
        action = primary_ips_client.change_dns_ptr(
            primary_ip, "1.2.3.4", "server02.example.com"
        )
        primary_ips_client._client.request.assert_called_with(
            url="/primary_ips/12/actions/change_dns_ptr",
            method="POST",
            json={"ip": "1.2.3.4", "dns_ptr": "server02.example.com"},
        )
        assert action.id == 1
        assert action.progress == 0

    def test_actions_get_by_id(self, primary_ips_client, response_get_actions):
        primary_ips_client._client.request.return_value = {
            "action": response_get_actions["actions"][0]
        }
        action = primary_ips_client.actions.get_by_id(13)

        primary_ips_client._client.request.assert_called_with(
            url="/primary_ips/actions/13", method="GET"
        )

        assert isinstance(action, BoundAction)
        assert action._client == primary_ips_client._client.actions
        assert action.id == 13
        assert action.command == "assign_primary_ip"

    def test_actions_get_list(self, primary_ips_client, response_get_actions):
        primary_ips_client._client.request.return_value = response_get_actions
        result = primary_ips_client.actions.get_list()

        primary_ips_client._client.request.assert_called_with(
            url="/primary_ips/actions",
            method="GET",
            params={},
        )

        actions = result.actions
        assert result.meta is None

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == primary_ips_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "assign_primary_ip"

    def test_actions_get_all(self, primary_ips_client, response_get_actions):
        primary_ips_client._client.request.return_value = response_get_actions
        actions = primary_ips_client.actions.get_all()

        primary_ips_client._client.request.assert_called_with(
            url="/primary_ips/actions",
            method="GET",
            params={"page": 1, "per_page": 50},
        )

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == primary_ips_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "assign_primary_ip"
