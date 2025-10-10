from __future__ import annotations

from unittest import mock

import pytest

from hcloud import Client
from hcloud.firewalls import (
    BoundFirewall,
    Firewall,
    FirewallResource,
    FirewallResourceLabelSelector,
    FirewallRule,
    FirewallsClient,
)
from hcloud.servers import Server

from ..conftest import BoundModelTestCase


class TestBoundFirewall(BoundModelTestCase):
    methods = [
        BoundFirewall.update,
        BoundFirewall.delete,
        BoundFirewall.apply_to_resources,
        BoundFirewall.remove_from_resources,
        BoundFirewall.set_rules,
    ]

    @pytest.fixture()
    def resource_client(self, client: Client):
        return client.firewalls

    @pytest.fixture()
    def bound_model(self, resource_client, firewall_response):
        return BoundFirewall(resource_client, data=firewall_response["firewall"])

    def test_init(self, bound_model: BoundFirewall):
        o = bound_model
        assert o.id == 38
        assert o.name == "Corporate Intranet Protection"
        assert o.labels == {}
        assert isinstance(o.rules, list)
        assert len(o.rules) == 2

        assert isinstance(o.applied_to, list)
        assert len(o.applied_to) == 2
        assert o.applied_to[0].server.id == 42
        assert o.applied_to[0].type == "server"
        assert o.applied_to[1].label_selector.selector == "key==value"
        assert o.applied_to[1].type == "label_selector"

        firewall_in_rule = o.rules[0]
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

        firewall_out_rule = o.rules[1]
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


class TestFirewallsClient:
    @pytest.fixture()
    def firewalls_client(self, client: Client):
        return FirewallsClient(client)

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        firewalls_client: FirewallsClient,
        firewall_response,
    ):
        request_mock.return_value = firewall_response

        firewall = firewalls_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/firewalls/1",
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
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        firewalls_client: FirewallsClient,
        two_firewalls_response,
        params,
    ):
        request_mock.return_value = two_firewalls_response

        result = firewalls_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/firewalls",
            params=params,
        )

        firewalls = result.firewalls
        assert result.meta is not None

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
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        firewalls_client: FirewallsClient,
        two_firewalls_response,
        params,
    ):
        request_mock.return_value = two_firewalls_response

        firewalls = firewalls_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/firewalls",
            params=params,
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

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        firewalls_client: FirewallsClient,
        one_firewalls_response,
    ):
        request_mock.return_value = one_firewalls_response

        firewall = firewalls_client.get_by_name("Corporate Intranet Protection")

        params = {"name": "Corporate Intranet Protection"}

        request_mock.assert_called_with(
            method="GET",
            url="/firewalls",
            params=params,
        )

        assert firewall._client is firewalls_client
        assert firewall.id == 38
        assert firewall.name == "Corporate Intranet Protection"

    def test_create(
        self,
        request_mock: mock.MagicMock,
        firewalls_client: FirewallsClient,
        response_create_firewall,
    ):
        request_mock.return_value = response_create_firewall

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

        request_mock.assert_called_with(
            method="POST",
            url="/firewalls",
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
    def test_update(
        self,
        request_mock: mock.MagicMock,
        firewalls_client: FirewallsClient,
        firewall,
        response_update_firewall,
    ):
        request_mock.return_value = response_update_firewall

        firewall = firewalls_client.update(
            firewall, name="New Corporate Intranet Protection", labels={}
        )

        request_mock.assert_called_with(
            method="PUT",
            url="/firewalls/38",
            json={"name": "New Corporate Intranet Protection", "labels": {}},
        )

        assert firewall.id == 38
        assert firewall.name == "New Corporate Intranet Protection"

    @pytest.mark.parametrize(
        "firewall", [Firewall(id=1), BoundFirewall(mock.MagicMock(), dict(id=1))]
    )
    def test_set_rules(
        self,
        request_mock: mock.MagicMock,
        firewalls_client: FirewallsClient,
        firewall,
        response_set_rules,
    ):
        request_mock.return_value = response_set_rules

        actions = firewalls_client.set_rules(
            firewall,
            [
                FirewallRule(
                    direction=FirewallRule.DIRECTION_IN,
                    protocol=FirewallRule.PROTOCOL_ICMP,
                    source_ips=["0.0.0.0/0", "::/0"],
                    description="Allow ICMP from everywhere",
                ),
                FirewallRule(
                    direction=FirewallRule.DIRECTION_IN,
                    protocol=FirewallRule.PROTOCOL_TCP,
                    port="80",
                    source_ips=["0.0.0.0/0", "::/0"],
                    description="Allow HTTP from everywhere",
                ),
            ],
        )

        request_mock.assert_called_with(
            method="POST",
            url="/firewalls/1/actions/set_rules",
            json={
                "rules": [
                    {
                        "direction": "in",
                        "protocol": "icmp",
                        "source_ips": ["0.0.0.0/0", "::/0"],
                        "description": "Allow ICMP from everywhere",
                    },
                    {
                        "direction": "in",
                        "protocol": "tcp",
                        "port": "80",
                        "source_ips": ["0.0.0.0/0", "::/0"],
                        "description": "Allow HTTP from everywhere",
                    },
                ]
            },
        )

        assert actions[0].id == 13
        assert actions[0].progress == 100

    @pytest.mark.parametrize(
        "firewall", [Firewall(id=1), BoundFirewall(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(
        self,
        request_mock: mock.MagicMock,
        firewalls_client: FirewallsClient,
        firewall,
    ):
        delete_success = firewalls_client.delete(firewall)

        request_mock.assert_called_with(
            method="DELETE",
            url="/firewalls/1",
        )

        assert delete_success is True

    @pytest.mark.parametrize(
        "firewall", [Firewall(id=1), BoundFirewall(mock.MagicMock(), dict(id=1))]
    )
    def test_apply_to_resources(
        self,
        request_mock: mock.MagicMock,
        firewalls_client: FirewallsClient,
        firewall,
        response_set_rules,
    ):
        request_mock.return_value = response_set_rules

        actions = firewalls_client.apply_to_resources(
            firewall,
            [FirewallResource(type=FirewallResource.TYPE_SERVER, server=Server(id=5))],
        )

        request_mock.assert_called_with(
            method="POST",
            url="/firewalls/1/actions/apply_to_resources",
            json={"apply_to": [{"type": "server", "server": {"id": 5}}]},
        )

        assert actions[0].id == 13
        assert actions[0].progress == 100

    @pytest.mark.parametrize(
        "firewall", [Firewall(id=1), BoundFirewall(mock.MagicMock(), dict(id=1))]
    )
    def test_remove_from_resources(
        self,
        request_mock: mock.MagicMock,
        firewalls_client: FirewallsClient,
        firewall,
        response_set_rules,
    ):
        request_mock.return_value = response_set_rules

        actions = firewalls_client.remove_from_resources(
            firewall,
            [FirewallResource(type=FirewallResource.TYPE_SERVER, server=Server(id=5))],
        )

        request_mock.assert_called_with(
            method="POST",
            url="/firewalls/1/actions/remove_from_resources",
            json={"remove_from": [{"type": "server", "server": {"id": 5}}]},
        )

        assert actions[0].id == 13
        assert actions[0].progress == 100
