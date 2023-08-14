from __future__ import annotations

from unittest import mock

import pytest

from hcloud.actions import BoundAction
from hcloud.floating_ips import BoundFloatingIP, FloatingIP, FloatingIPsClient
from hcloud.locations import BoundLocation, Location
from hcloud.servers import BoundServer, Server


class TestBoundFloatingIP:
    @pytest.fixture()
    def bound_floating_ip(self, hetzner_client):
        return BoundFloatingIP(client=hetzner_client.floating_ips, data=dict(id=14))

    def test_bound_floating_ip_init(self, floating_ip_response):
        bound_floating_ip = BoundFloatingIP(
            client=mock.MagicMock(), data=floating_ip_response["floating_ip"]
        )

        assert bound_floating_ip.id == 4711
        assert bound_floating_ip.description == "Web Frontend"
        assert bound_floating_ip.name == "Web Frontend"
        assert bound_floating_ip.ip == "131.232.99.1"
        assert bound_floating_ip.type == "ipv4"
        assert bound_floating_ip.protection == {"delete": False}
        assert bound_floating_ip.labels == {}
        assert bound_floating_ip.blocked is False

        assert isinstance(bound_floating_ip.server, BoundServer)
        assert bound_floating_ip.server.id == 42

        assert isinstance(bound_floating_ip.home_location, BoundLocation)
        assert bound_floating_ip.home_location.id == 1
        assert bound_floating_ip.home_location.name == "fsn1"
        assert bound_floating_ip.home_location.description == "Falkenstein DC Park 1"
        assert bound_floating_ip.home_location.country == "DE"
        assert bound_floating_ip.home_location.city == "Falkenstein"
        assert bound_floating_ip.home_location.latitude == 50.47612
        assert bound_floating_ip.home_location.longitude == 12.370071

    def test_get_actions(self, hetzner_client, bound_floating_ip, response_get_actions):
        hetzner_client.request.return_value = response_get_actions
        actions = bound_floating_ip.get_actions(sort="id")
        hetzner_client.request.assert_called_with(
            url="/floating_ips/14/actions",
            method="GET",
            params={"sort": "id", "page": 1, "per_page": 50},
        )

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == hetzner_client.actions
        assert actions[0].id == 13
        assert actions[0].command == "assign_floating_ip"

    def test_update(
        self, hetzner_client, bound_floating_ip, response_update_floating_ip
    ):
        hetzner_client.request.return_value = response_update_floating_ip
        floating_ip = bound_floating_ip.update(
            description="New description", name="New name"
        )
        hetzner_client.request.assert_called_with(
            url="/floating_ips/14",
            method="PUT",
            json={"description": "New description", "name": "New name"},
        )

        assert floating_ip.id == 4711
        assert floating_ip.description == "New description"
        assert floating_ip.name == "New name"

    def test_delete(self, hetzner_client, bound_floating_ip, generic_action):
        hetzner_client.request.return_value = generic_action
        delete_success = bound_floating_ip.delete()
        hetzner_client.request.assert_called_with(
            url="/floating_ips/14", method="DELETE"
        )

        assert delete_success is True

    def test_change_protection(self, hetzner_client, bound_floating_ip, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_floating_ip.change_protection(True)
        hetzner_client.request.assert_called_with(
            url="/floating_ips/14/actions/change_protection",
            method="POST",
            json={"delete": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", (Server(id=1), BoundServer(mock.MagicMock(), dict(id=1)))
    )
    def test_assign(self, hetzner_client, bound_floating_ip, server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_floating_ip.assign(server)
        hetzner_client.request.assert_called_with(
            url="/floating_ips/14/actions/assign", method="POST", json={"server": 1}
        )
        assert action.id == 1
        assert action.progress == 0

    def test_unassign(self, hetzner_client, bound_floating_ip, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_floating_ip.unassign()
        hetzner_client.request.assert_called_with(
            url="/floating_ips/14/actions/unassign", method="POST"
        )
        assert action.id == 1
        assert action.progress == 0

    def test_change_dns_ptr(self, hetzner_client, bound_floating_ip, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_floating_ip.change_dns_ptr("1.2.3.4", "server02.example.com")
        hetzner_client.request.assert_called_with(
            url="/floating_ips/14/actions/change_dns_ptr",
            method="POST",
            json={"ip": "1.2.3.4", "dns_ptr": "server02.example.com"},
        )
        assert action.id == 1
        assert action.progress == 0


class TestFloatingIPsClient:
    @pytest.fixture()
    def floating_ips_client(self):
        return FloatingIPsClient(client=mock.MagicMock())

    def test_get_by_id(self, floating_ips_client, floating_ip_response):
        floating_ips_client._client.request.return_value = floating_ip_response
        bound_floating_ip = floating_ips_client.get_by_id(1)
        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips/1", method="GET"
        )
        assert bound_floating_ip._client is floating_ips_client
        assert bound_floating_ip.id == 4711
        assert bound_floating_ip.description == "Web Frontend"

    def test_get_by_name(self, floating_ips_client, one_floating_ips_response):
        floating_ips_client._client.request.return_value = one_floating_ips_response
        bound_floating_ip = floating_ips_client.get_by_name("Web Frontend")
        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips", method="GET", params={"name": "Web Frontend"}
        )
        assert bound_floating_ip._client is floating_ips_client
        assert bound_floating_ip.id == 4711
        assert bound_floating_ip.name == "Web Frontend"
        assert bound_floating_ip.description == "Web Frontend"

    @pytest.mark.parametrize(
        "params",
        [{"label_selector": "label1", "page": 1, "per_page": 10}, {"name": ""}, {}],
    )
    def test_get_list(self, floating_ips_client, two_floating_ips_response, params):
        floating_ips_client._client.request.return_value = two_floating_ips_response
        result = floating_ips_client.get_list(**params)
        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips", method="GET", params=params
        )

        bound_floating_ips = result.floating_ips
        assert result.meta is None

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
    def test_get_all(self, floating_ips_client, two_floating_ips_response, params):
        floating_ips_client._client.request.return_value = two_floating_ips_response
        bound_floating_ips = floating_ips_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips", method="GET", params=params
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

    def test_create_with_location(self, floating_ips_client, floating_ip_response):
        floating_ips_client._client.request.return_value = floating_ip_response
        response = floating_ips_client.create(
            "ipv6", "Web Frontend", home_location=Location(name="location")
        )
        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips",
            method="POST",
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
        self, floating_ips_client, server, floating_ip_create_response
    ):
        floating_ips_client._client.request.return_value = floating_ip_create_response
        response = floating_ips_client.create(
            type="ipv6", description="Web Frontend", server=server
        )
        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips",
            method="POST",
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
        self, floating_ips_client, server, floating_ip_create_response
    ):
        floating_ips_client._client.request.return_value = floating_ip_create_response
        response = floating_ips_client.create(
            type="ipv6", description="Web Frontend", name="Web Frontend"
        )
        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips",
            method="POST",
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
    def test_get_actions(self, floating_ips_client, floating_ip, response_get_actions):
        floating_ips_client._client.request.return_value = response_get_actions
        actions = floating_ips_client.get_actions(floating_ip)
        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips/1/actions",
            method="GET",
            params={"page": 1, "per_page": 50},
        )

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)

        assert actions[0]._client == floating_ips_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "assign_floating_ip"

    @pytest.mark.parametrize(
        "floating_ip", [FloatingIP(id=1), BoundFloatingIP(mock.MagicMock(), dict(id=1))]
    )
    def test_update(
        self, floating_ips_client, floating_ip, response_update_floating_ip
    ):
        floating_ips_client._client.request.return_value = response_update_floating_ip
        floating_ip = floating_ips_client.update(
            floating_ip, description="New description", name="New name"
        )
        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips/1",
            method="PUT",
            json={"description": "New description", "name": "New name"},
        )

        assert floating_ip.id == 4711
        assert floating_ip.description == "New description"
        assert floating_ip.name == "New name"

    @pytest.mark.parametrize(
        "floating_ip", [FloatingIP(id=1), BoundFloatingIP(mock.MagicMock(), dict(id=1))]
    )
    def test_change_protection(self, floating_ips_client, floating_ip, generic_action):
        floating_ips_client._client.request.return_value = generic_action
        action = floating_ips_client.change_protection(floating_ip, True)
        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips/1/actions/change_protection",
            method="POST",
            json={"delete": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "floating_ip", [FloatingIP(id=1), BoundFloatingIP(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(self, floating_ips_client, floating_ip, generic_action):
        floating_ips_client._client.request.return_value = generic_action
        delete_success = floating_ips_client.delete(floating_ip)
        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips/1", method="DELETE"
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
    def test_assign(self, floating_ips_client, server, floating_ip, generic_action):
        floating_ips_client._client.request.return_value = generic_action
        action = floating_ips_client.assign(floating_ip, server)
        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips/12/actions/assign", method="POST", json={"server": 1}
        )
        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "floating_ip",
        [FloatingIP(id=12), BoundFloatingIP(mock.MagicMock(), dict(id=12))],
    )
    def test_unassign(self, floating_ips_client, floating_ip, generic_action):
        floating_ips_client._client.request.return_value = generic_action
        action = floating_ips_client.unassign(floating_ip)
        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips/12/actions/unassign", method="POST"
        )
        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "floating_ip",
        [FloatingIP(id=12), BoundFloatingIP(mock.MagicMock(), dict(id=12))],
    )
    def test_change_dns_ptr(self, floating_ips_client, floating_ip, generic_action):
        floating_ips_client._client.request.return_value = generic_action
        action = floating_ips_client.change_dns_ptr(
            floating_ip, "1.2.3.4", "server02.example.com"
        )
        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips/12/actions/change_dns_ptr",
            method="POST",
            json={"ip": "1.2.3.4", "dns_ptr": "server02.example.com"},
        )
        assert action.id == 1
        assert action.progress == 0

    def test_actions_get_by_id(self, floating_ips_client, response_get_actions):
        floating_ips_client._client.request.return_value = {
            "action": response_get_actions["actions"][0]
        }
        action = floating_ips_client.actions.get_by_id(13)

        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips/actions/13", method="GET"
        )

        assert isinstance(action, BoundAction)
        assert action._client == floating_ips_client._client.actions
        assert action.id == 13
        assert action.command == "assign_floating_ip"

    def test_actions_get_list(self, floating_ips_client, response_get_actions):
        floating_ips_client._client.request.return_value = response_get_actions
        result = floating_ips_client.actions.get_list()

        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips/actions",
            method="GET",
            params={},
        )

        actions = result.actions
        assert result.meta is None

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == floating_ips_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "assign_floating_ip"

    def test_actions_get_all(self, floating_ips_client, response_get_actions):
        floating_ips_client._client.request.return_value = response_get_actions
        actions = floating_ips_client.actions.get_all()

        floating_ips_client._client.request.assert_called_with(
            url="/floating_ips/actions",
            method="GET",
            params={"page": 1, "per_page": 50},
        )

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == floating_ips_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "assign_floating_ip"
