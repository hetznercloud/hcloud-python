from __future__ import annotations

from unittest import mock

import pytest

from hcloud.actions import BoundAction
from hcloud.firewalls import (
    BoundFirewall,
    Firewall,
    FirewallResource,
    FirewallResourceLabelSelector,
    FirewallRule,
    FirewallsClient,
)
from hcloud.servers import Server


class TestBoundFirewall:
    @pytest.fixture()
    def bound_firewall(self, hetzner_client):
        return BoundFirewall(client=hetzner_client.firewalls, data=dict(id=1))

    def test_bound_firewall_init(self, firewall_response):
        bound_firewall = BoundFirewall(
            client=mock.MagicMock(), data=firewall_response["firewall"]
        )

        assert bound_firewall.id == 38
        assert bound_firewall.name == "Corporate Intranet Protection"
        assert bound_firewall.labels == {}
        assert isinstance(bound_firewall.rules, list)
        assert len(bound_firewall.rules) == 2

        assert isinstance(bound_firewall.applied_to, list)
        assert len(bound_firewall.applied_to) == 2
        assert bound_firewall.applied_to[0].server.id == 42
        assert bound_firewall.applied_to[0].type == "server"
        assert bound_firewall.applied_to[1].label_selector.selector == "key==value"
        assert bound_firewall.applied_to[1].type == "label_selector"

        firewall_in_rule = bound_firewall.rules[0]
        assert isinstance(firewall_in_rule, FirewallRule)
        assert firewall_in_rule.direction == FirewallRule.DIRECTION_IN
        assert firewall_in_rule.protocol == FirewallRule.PROTOCOL_TCP
        assert firewall_in_rule.port == "80"
        assert isinstance(firewall_in_rule.source_ips, list)
        assert len(firewall_in_rule.source_ips) == 3
        assert firewall_in_rule.source_ips == [
            "28.239.13.1/32",
            "28.239.14.0/24",
            "ff21:1eac:9a3b:ee58:5ca:990c:8bc9:c03b/128",
        ]
        assert isinstance(firewall_in_rule.destination_ips, list)
        assert len(firewall_in_rule.destination_ips) == 0
        assert firewall_in_rule.description == "allow http in"

        firewall_out_rule = bound_firewall.rules[1]
        assert isinstance(firewall_out_rule, FirewallRule)
        assert firewall_out_rule.direction == FirewallRule.DIRECTION_OUT
        assert firewall_out_rule.protocol == FirewallRule.PROTOCOL_TCP
        assert firewall_out_rule.port == "80"
        assert isinstance(firewall_out_rule.source_ips, list)
        assert len(firewall_out_rule.source_ips) == 0
        assert isinstance(firewall_out_rule.destination_ips, list)
        assert len(firewall_out_rule.destination_ips) == 3
        assert firewall_out_rule.destination_ips == [
            "28.239.13.1/32",
            "28.239.14.0/24",
            "ff21:1eac:9a3b:ee58:5ca:990c:8bc9:c03b/128",
        ]
        assert firewall_out_rule.description == "allow http out"

    @pytest.mark.parametrize(
        "params", [{}, {"sort": ["created"], "page": 1, "per_page": 2}]
    )
    def test_get_actions_list(
        self, hetzner_client, bound_firewall, response_get_actions, params
    ):
        hetzner_client.request.return_value = response_get_actions
        result = bound_firewall.get_actions_list(**params)
        hetzner_client.request.assert_called_with(
            url="/firewalls/1/actions", method="GET", params=params
        )

        actions = result.actions
        assert result.meta is None

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == hetzner_client.actions
        assert actions[0].id == 13
        assert actions[0].command == "set_firewall_rules"

    @pytest.mark.parametrize("params", [{}, {"sort": ["created"]}])
    def test_get_actions(
        self, hetzner_client, bound_firewall, response_get_actions, params
    ):
        hetzner_client.request.return_value = response_get_actions
        actions = bound_firewall.get_actions(**params)

        params.update({"page": 1, "per_page": 50})

        hetzner_client.request.assert_called_with(
            url="/firewalls/1/actions", method="GET", params=params
        )

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == hetzner_client.actions
        assert actions[0].id == 13
        assert actions[0].command == "set_firewall_rules"

    def test_update(self, hetzner_client, bound_firewall, response_update_firewall):
        hetzner_client.request.return_value = response_update_firewall
        firewall = bound_firewall.update(
            name="New Corporate Intranet Protection", labels={}
        )
        hetzner_client.request.assert_called_with(
            url="/firewalls/1",
            method="PUT",
            json={"name": "New Corporate Intranet Protection", "labels": {}},
        )

        assert firewall.id == 38
        assert firewall.name == "New Corporate Intranet Protection"

    def test_delete(self, hetzner_client, bound_firewall):
        delete_success = bound_firewall.delete()
        hetzner_client.request.assert_called_with(url="/firewalls/1", method="DELETE")

        assert delete_success is True

    def test_set_rules(self, hetzner_client, bound_firewall, response_set_rules):
        hetzner_client.request.return_value = response_set_rules
        actions = bound_firewall.set_rules(
            [
                FirewallRule(
                    direction=FirewallRule.DIRECTION_IN,
                    protocol=FirewallRule.PROTOCOL_ICMP,
                    source_ips=["0.0.0.0/0", "::/0"],
                    description="New firewall description",
                )
            ]
        )
        hetzner_client.request.assert_called_with(
            url="/firewalls/1/actions/set_rules",
            method="POST",
            json={
                "rules": [
                    {
                        "direction": "in",
                        "protocol": "icmp",
                        "source_ips": ["0.0.0.0/0", "::/0"],
                        "description": "New firewall description",
                    }
                ]
            },
        )

        assert actions[0].id == 13
        assert actions[0].progress == 100

    def test_apply_to_resources(
        self, hetzner_client, bound_firewall, response_set_rules
    ):
        hetzner_client.request.return_value = response_set_rules
        actions = bound_firewall.apply_to_resources(
            [FirewallResource(type=FirewallResource.TYPE_SERVER, server=Server(id=5))]
        )
        hetzner_client.request.assert_called_with(
            url="/firewalls/1/actions/apply_to_resources",
            method="POST",
            json={"apply_to": [{"type": "server", "server": {"id": 5}}]},
        )

        assert actions[0].id == 13
        assert actions[0].progress == 100

    def test_remove_from_resources(
        self, hetzner_client, bound_firewall, response_set_rules
    ):
        hetzner_client.request.return_value = response_set_rules
        actions = bound_firewall.remove_from_resources(
            [FirewallResource(type=FirewallResource.TYPE_SERVER, server=Server(id=5))]
        )
        hetzner_client.request.assert_called_with(
            url="/firewalls/1/actions/remove_from_resources",
            method="POST",
            json={"remove_from": [{"type": "server", "server": {"id": 5}}]},
        )

        assert actions[0].id == 13
        assert actions[0].progress == 100


class TestFirewallsClient:
    @pytest.fixture()
    def firewalls_client(self):
        return FirewallsClient(client=mock.MagicMock())

    def test_get_by_id(self, firewalls_client, firewall_response):
        firewalls_client._client.request.return_value = firewall_response
        firewall = firewalls_client.get_by_id(1)
        firewalls_client._client.request.assert_called_with(
            url="/firewalls/1", method="GET"
        )
        assert firewall._client is firewalls_client
        assert firewall.id == 38
        assert firewall.name == "Corporate Intranet Protection"

    @pytest.mark.parametrize(
        "params",
        [
            {
                "name": "Corporate Intranet Protection",
                "sort": "id",
                "label_selector": "k==v",
                "page": 1,
                "per_page": 10,
            },
            {"name": ""},
            {},
        ],
    )
    def test_get_list(self, firewalls_client, two_firewalls_response, params):
        firewalls_client._client.request.return_value = two_firewalls_response
        result = firewalls_client.get_list(**params)
        firewalls_client._client.request.assert_called_with(
            url="/firewalls", method="GET", params=params
        )

        firewalls = result.firewalls
        assert result.meta is None

        assert len(firewalls) == 2

        firewalls1 = firewalls[0]
        firewalls2 = firewalls[1]

        assert firewalls1._client is firewalls_client
        assert firewalls1.id == 38
        assert firewalls1.name == "Corporate Intranet Protection"

        assert firewalls2._client is firewalls_client
        assert firewalls2.id == 39
        assert firewalls2.name == "Corporate Extranet Protection"

    @pytest.mark.parametrize(
        "params",
        [
            {
                "name": "Corporate Intranet Protection",
                "sort": "id",
                "label_selector": "k==v",
            },
            {},
        ],
    )
    def test_get_all(self, firewalls_client, two_firewalls_response, params):
        firewalls_client._client.request.return_value = two_firewalls_response
        firewalls = firewalls_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        firewalls_client._client.request.assert_called_with(
            url="/firewalls", method="GET", params=params
        )

        assert len(firewalls) == 2

        firewalls1 = firewalls[0]
        firewalls2 = firewalls[1]

        assert firewalls1._client is firewalls_client
        assert firewalls1.id == 38
        assert firewalls1.name == "Corporate Intranet Protection"

        assert firewalls2._client is firewalls_client
        assert firewalls2.id == 39
        assert firewalls2.name == "Corporate Extranet Protection"

    def test_get_by_name(self, firewalls_client, one_firewalls_response):
        firewalls_client._client.request.return_value = one_firewalls_response
        firewall = firewalls_client.get_by_name("Corporate Intranet Protection")

        params = {"name": "Corporate Intranet Protection"}

        firewalls_client._client.request.assert_called_with(
            url="/firewalls", method="GET", params=params
        )

        assert firewall._client is firewalls_client
        assert firewall.id == 38
        assert firewall.name == "Corporate Intranet Protection"

    @pytest.mark.parametrize(
        "firewall", [Firewall(id=1), BoundFirewall(mock.MagicMock(), dict(id=1))]
    )
    def test_get_actions_list(self, firewalls_client, firewall, response_get_actions):
        firewalls_client._client.request.return_value = response_get_actions
        result = firewalls_client.get_actions_list(firewall)
        firewalls_client._client.request.assert_called_with(
            url="/firewalls/1/actions", method="GET", params={}
        )

        actions = result.actions
        assert result.meta is None

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)

        assert actions[0]._client == firewalls_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "set_firewall_rules"

    def test_create(self, firewalls_client, response_create_firewall):
        firewalls_client._client.request.return_value = response_create_firewall
        response = firewalls_client.create(
            "Corporate Intranet Protection",
            rules=[
                FirewallRule(
                    direction=FirewallRule.DIRECTION_IN,
                    protocol=FirewallRule.PROTOCOL_ICMP,
                    source_ips=["0.0.0.0/0"],
                )
            ],
            resources=[
                FirewallResource(
                    type=FirewallResource.TYPE_SERVER, server=Server(id=4711)
                ),
                FirewallResource(
                    type=FirewallResource.TYPE_LABEL_SELECTOR,
                    label_selector=FirewallResourceLabelSelector(selector="key==value"),
                ),
            ],
        )
        firewalls_client._client.request.assert_called_with(
            url="/firewalls",
            method="POST",
            json={
                "name": "Corporate Intranet Protection",
                "rules": [
                    {"direction": "in", "protocol": "icmp", "source_ips": ["0.0.0.0/0"]}
                ],
                "apply_to": [
                    {"type": "server", "server": {"id": 4711}},
                    {
                        "type": "label_selector",
                        "label_selector": {"selector": "key==value"},
                    },
                ],
            },
        )

        bound_firewall = response.firewall
        actions = response.actions

        assert bound_firewall._client is firewalls_client
        assert bound_firewall.id == 38
        assert bound_firewall.name == "Corporate Intranet Protection"
        assert len(bound_firewall.applied_to) == 2

        assert len(actions) == 2

    @pytest.mark.parametrize(
        "firewall", [Firewall(id=38), BoundFirewall(mock.MagicMock(), dict(id=38))]
    )
    def test_update(self, firewalls_client, firewall, response_update_firewall):
        firewalls_client._client.request.return_value = response_update_firewall
        firewall = firewalls_client.update(
            firewall, name="New Corporate Intranet Protection", labels={}
        )
        firewalls_client._client.request.assert_called_with(
            url="/firewalls/38",
            method="PUT",
            json={"name": "New Corporate Intranet Protection", "labels": {}},
        )

        assert firewall.id == 38
        assert firewall.name == "New Corporate Intranet Protection"

    @pytest.mark.parametrize(
        "firewall", [Firewall(id=1), BoundFirewall(mock.MagicMock(), dict(id=1))]
    )
    def test_set_rules(self, firewalls_client, firewall, response_set_rules):
        firewalls_client._client.request.return_value = response_set_rules
        actions = firewalls_client.set_rules(
            firewall,
            [
                FirewallRule(
                    direction=FirewallRule.DIRECTION_IN,
                    protocol=FirewallRule.PROTOCOL_ICMP,
                    source_ips=["0.0.0.0/0", "::/0"],
                )
            ],
        )
        firewalls_client._client.request.assert_called_with(
            url="/firewalls/1/actions/set_rules",
            method="POST",
            json={
                "rules": [
                    {
                        "direction": "in",
                        "protocol": "icmp",
                        "source_ips": ["0.0.0.0/0", "::/0"],
                    }
                ]
            },
        )

        assert actions[0].id == 13
        assert actions[0].progress == 100

    @pytest.mark.parametrize(
        "firewall", [Firewall(id=1), BoundFirewall(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(self, firewalls_client, firewall):
        delete_success = firewalls_client.delete(firewall)
        firewalls_client._client.request.assert_called_with(
            url="/firewalls/1", method="DELETE"
        )

        assert delete_success is True

    @pytest.mark.parametrize(
        "firewall", [Firewall(id=1), BoundFirewall(mock.MagicMock(), dict(id=1))]
    )
    def test_apply_to_resources(self, firewalls_client, firewall, response_set_rules):
        firewalls_client._client.request.return_value = response_set_rules

        actions = firewalls_client.apply_to_resources(
            firewall,
            [FirewallResource(type=FirewallResource.TYPE_SERVER, server=Server(id=5))],
        )
        firewalls_client._client.request.assert_called_with(
            url="/firewalls/1/actions/apply_to_resources",
            method="POST",
            json={"apply_to": [{"type": "server", "server": {"id": 5}}]},
        )

        assert actions[0].id == 13
        assert actions[0].progress == 100

    @pytest.mark.parametrize(
        "firewall", [Firewall(id=1), BoundFirewall(mock.MagicMock(), dict(id=1))]
    )
    def test_remove_from_resources(
        self, firewalls_client, firewall, response_set_rules
    ):
        firewalls_client._client.request.return_value = response_set_rules

        actions = firewalls_client.remove_from_resources(
            firewall,
            [FirewallResource(type=FirewallResource.TYPE_SERVER, server=Server(id=5))],
        )
        firewalls_client._client.request.assert_called_with(
            url="/firewalls/1/actions/remove_from_resources",
            method="POST",
            json={"remove_from": [{"type": "server", "server": {"id": 5}}]},
        )

        assert actions[0].id == 13
        assert actions[0].progress == 100

    def test_actions_get_by_id(self, firewalls_client, response_get_actions):
        firewalls_client._client.request.return_value = {
            "action": response_get_actions["actions"][0]
        }
        action = firewalls_client.actions.get_by_id(13)

        firewalls_client._client.request.assert_called_with(
            url="/firewalls/actions/13", method="GET"
        )

        assert isinstance(action, BoundAction)
        assert action._client == firewalls_client._client.actions
        assert action.id == 13
        assert action.command == "set_firewall_rules"

    def test_actions_get_list(self, firewalls_client, response_get_actions):
        firewalls_client._client.request.return_value = response_get_actions
        result = firewalls_client.actions.get_list()

        firewalls_client._client.request.assert_called_with(
            url="/firewalls/actions",
            method="GET",
            params={},
        )

        actions = result.actions
        assert result.meta is None

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == firewalls_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "set_firewall_rules"

    def test_actions_get_all(self, firewalls_client, response_get_actions):
        firewalls_client._client.request.return_value = response_get_actions
        actions = firewalls_client.actions.get_all()

        firewalls_client._client.request.assert_called_with(
            url="/firewalls/actions",
            method="GET",
            params={"page": 1, "per_page": 50},
        )

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == firewalls_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "set_firewall_rules"
