from __future__ import annotations

from unittest import mock

import pytest

from hcloud.actions import BoundAction
from hcloud.datacenters import BoundDatacenter, Datacenter
from hcloud.firewalls import BoundFirewall, Firewall
from hcloud.floating_ips import BoundFloatingIP
from hcloud.images import BoundImage, Image
from hcloud.isos import BoundIso, Iso
from hcloud.locations import Location
from hcloud.networks import BoundNetwork, Network
from hcloud.placement_groups import BoundPlacementGroup, PlacementGroup
from hcloud.server_types import BoundServerType, ServerType
from hcloud.servers import (
    BoundServer,
    IPv4Address,
    IPv6Network,
    PrivateNet,
    PublicNetwork,
    PublicNetworkFirewall,
    Server,
    ServersClient,
)
from hcloud.volumes import BoundVolume, Volume


class TestBoundServer:
    @pytest.fixture()
    def bound_server(self, hetzner_client):
        return BoundServer(client=hetzner_client.servers, data=dict(id=14))

    def test_bound_server_init(self, response_full_server):
        bound_server = BoundServer(
            client=mock.MagicMock(), data=response_full_server["server"]
        )

        assert bound_server.id == 42
        assert bound_server.name == "my-server"
        assert bound_server.primary_disk_size == 20
        assert isinstance(bound_server.public_net, PublicNetwork)
        assert isinstance(bound_server.public_net.ipv4, IPv4Address)
        assert bound_server.public_net.ipv4.ip == "1.2.3.4"
        assert bound_server.public_net.ipv4.blocked is False
        assert bound_server.public_net.ipv4.dns_ptr == "server01.example.com"

        assert isinstance(bound_server.public_net.ipv6, IPv6Network)
        assert bound_server.public_net.ipv6.ip == "2001:db8::/64"
        assert bound_server.public_net.ipv6.blocked is False
        assert bound_server.public_net.ipv6.network == "2001:db8::"
        assert bound_server.public_net.ipv6.network_mask == "64"

        assert isinstance(bound_server.public_net.firewalls, list)
        assert isinstance(bound_server.public_net.firewalls[0], PublicNetworkFirewall)
        firewall = bound_server.public_net.firewalls[0]
        assert isinstance(firewall.firewall, BoundFirewall)
        assert bound_server.public_net.ipv6.blocked is False
        assert firewall.status == PublicNetworkFirewall.STATUS_APPLIED

        assert isinstance(bound_server.public_net.floating_ips[0], BoundFloatingIP)
        assert bound_server.public_net.floating_ips[0].id == 478
        assert bound_server.public_net.floating_ips[0].complete is False

        assert isinstance(bound_server.datacenter, BoundDatacenter)
        assert (
            bound_server.datacenter._client == bound_server._client._client.datacenters
        )
        assert bound_server.datacenter.id == 1
        assert bound_server.datacenter.complete is True

        assert isinstance(bound_server.server_type, BoundServerType)
        assert (
            bound_server.server_type._client
            == bound_server._client._client.server_types
        )
        assert bound_server.server_type.id == 1
        assert bound_server.server_type.complete is True

        assert len(bound_server.volumes) == 2
        assert isinstance(bound_server.volumes[0], BoundVolume)
        assert bound_server.volumes[0]._client == bound_server._client._client.volumes
        assert bound_server.volumes[0].id == 1
        assert bound_server.volumes[0].complete is False

        assert isinstance(bound_server.volumes[1], BoundVolume)
        assert bound_server.volumes[1]._client == bound_server._client._client.volumes
        assert bound_server.volumes[1].id == 2
        assert bound_server.volumes[1].complete is False

        assert isinstance(bound_server.image, BoundImage)
        assert bound_server.image._client == bound_server._client._client.images
        assert bound_server.image.id == 4711
        assert bound_server.image.name == "ubuntu-20.04"
        assert bound_server.image.complete is True

        assert isinstance(bound_server.iso, BoundIso)
        assert bound_server.iso._client == bound_server._client._client.isos
        assert bound_server.iso.id == 4711
        assert bound_server.iso.name == "FreeBSD-11.0-RELEASE-amd64-dvd1"
        assert bound_server.iso.complete is True

        assert len(bound_server.private_net) == 1
        assert isinstance(bound_server.private_net[0], PrivateNet)
        assert (
            bound_server.private_net[0].network._client
            == bound_server._client._client.networks
        )
        assert bound_server.private_net[0].ip == "10.1.1.5"
        assert bound_server.private_net[0].mac_address == "86:00:ff:2a:7d:e1"
        assert len(bound_server.private_net[0].alias_ips) == 1
        assert bound_server.private_net[0].alias_ips[0] == "10.1.1.8"

        assert isinstance(bound_server.placement_group, BoundPlacementGroup)
        assert (
            bound_server.placement_group._client
            == bound_server._client._client.placement_groups
        )
        assert bound_server.placement_group.id == 897
        assert bound_server.placement_group.name == "my Placement Group"
        assert bound_server.placement_group.complete is True

    @pytest.mark.parametrize(
        "params",
        [
            {
                "status": [Server.STATUS_RUNNING],
                "sort": "status",
                "page": 1,
                "per_page": 10,
            },
            {},
        ],
    )
    def test_get_actions_list(
        self, hetzner_client, bound_server, response_get_actions, params
    ):
        hetzner_client.request.return_value = response_get_actions
        result = bound_server.get_actions_list(**params)
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions", method="GET", params=params
        )

        actions = result.actions
        assert result.meta is None

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == hetzner_client.actions
        assert actions[0].id == 13
        assert actions[0].command == "start_server"

    @pytest.mark.parametrize(
        "params", [{"status": [Server.STATUS_RUNNING], "sort": "status"}, {}]
    )
    def test_get_actions(
        self, hetzner_client, bound_server, response_get_actions, params
    ):
        hetzner_client.request.return_value = response_get_actions
        actions = bound_server.get_actions(**params)

        params.update({"page": 1, "per_page": 50})

        hetzner_client.request.assert_called_with(
            url="/servers/14/actions", method="GET", params=params
        )

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == hetzner_client.actions
        assert actions[0].id == 13
        assert actions[0].command == "start_server"

    def test_update(self, hetzner_client, bound_server, response_update_server):
        hetzner_client.request.return_value = response_update_server
        server = bound_server.update(name="new-name", labels={})
        hetzner_client.request.assert_called_with(
            url="/servers/14", method="PUT", json={"name": "new-name", "labels": {}}
        )

        assert server.id == 14
        assert server.name == "new-name"

    def test_delete(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_server.delete()
        hetzner_client.request.assert_called_with(url="/servers/14", method="DELETE")

        assert action.id == 1
        assert action.progress == 0

    def test_get_metrics(
        self,
        hetzner_client,
        bound_server: BoundServer,
        response_get_metrics,
    ):
        hetzner_client.request.return_value = response_get_metrics
        response = bound_server.get_metrics(
            type=["cpu", "disk"],
            start="2023-12-14T17:40:00+01:00",
            end="2023-12-14T17:50:00+01:00",
        )
        hetzner_client.request.assert_called_with(
            url="/servers/14/metrics",
            method="GET",
            params={
                "type": "cpu,disk",
                "start": "2023-12-14T17:40:00+01:00",
                "end": "2023-12-14T17:50:00+01:00",
            },
        )

        assert "cpu" in response.metrics.time_series
        assert "disk.0.iops.read" in response.metrics.time_series
        assert len(response.metrics.time_series["disk.0.iops.read"]["values"]) == 3

    def test_power_off(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_server.power_off()
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/poweroff", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    def test_power_on(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_server.power_on()
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/poweron", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    def test_reboot(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_server.reboot()
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/reboot", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    def test_reset(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_server.reset()
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/reset", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    def test_shutdown(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_server.shutdown()
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/shutdown", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    def test_reset_password(
        self, hetzner_client, bound_server, response_server_reset_password
    ):
        hetzner_client.request.return_value = response_server_reset_password
        response = bound_server.reset_password()
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/reset_password", method="POST"
        )

        assert response.action.id == 1
        assert response.action.progress == 0
        assert response.root_password == "YItygq1v3GYjjMomLaKc"

    def test_change_type(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_server.change_type(ServerType(name="cx11"), upgrade_disk=True)
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/change_type",
            method="POST",
            json={"server_type": "cx11", "upgrade_disk": True},
        )

        assert action.id == 1
        assert action.progress == 0

    def test_enable_rescue(
        self, hetzner_client, bound_server, response_server_enable_rescue
    ):
        hetzner_client.request.return_value = response_server_enable_rescue
        response = bound_server.enable_rescue(type="linux64")
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/enable_rescue",
            method="POST",
            json={"type": "linux64"},
        )

        assert response.action.id == 1
        assert response.action.progress == 0
        assert response.root_password == "YItygq1v3GYjjMomLaKc"

    def test_disable_rescue(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_server.disable_rescue()
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/disable_rescue", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    def test_create_image(
        self, hetzner_client, bound_server, response_server_create_image
    ):
        hetzner_client.request.return_value = response_server_create_image
        response = bound_server.create_image(description="my image", type="snapshot")
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/create_image",
            method="POST",
            json={"description": "my image", "type": "snapshot"},
        )

        assert response.action.id == 1
        assert response.action.progress == 0
        assert response.image.description == "my image"

    def test_rebuild(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        response = bound_server.rebuild(
            Image(name="ubuntu-20.04"),
            return_response=True,
        )
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/rebuild",
            method="POST",
            json={"image": "ubuntu-20.04"},
        )

        assert response.action.id == 1
        assert response.action.progress == 0
        assert response.root_password is None or isinstance(response.root_password, str)

    def test_enable_backup(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_server.enable_backup()
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/enable_backup", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    def test_disable_backup(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_server.disable_backup()
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/disable_backup", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    def test_attach_iso(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_server.attach_iso(Iso(name="FreeBSD-11.0-RELEASE-amd64-dvd1"))
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/attach_iso",
            method="POST",
            json={"iso": "FreeBSD-11.0-RELEASE-amd64-dvd1"},
        )

        assert action.id == 1
        assert action.progress == 0

    def test_detach_iso(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_server.detach_iso()
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/detach_iso", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    def test_change_dns_ptr(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_server.change_dns_ptr("1.2.3.4", "example.com")
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/change_dns_ptr",
            method="POST",
            json={"ip": "1.2.3.4", "dns_ptr": "example.com"},
        )

        assert action.id == 1
        assert action.progress == 0

    def test_change_protection(self, hetzner_client, bound_server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_server.change_protection(True, True)
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/change_protection",
            method="POST",
            json={"delete": True, "rebuild": True},
        )

        assert action.id == 1
        assert action.progress == 0

    def test_request_console(
        self, hetzner_client, bound_server, response_server_request_console
    ):
        hetzner_client.request.return_value = response_server_request_console
        response = bound_server.request_console()
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/request_console", method="POST"
        )

        assert response.action.id == 1
        assert response.action.progress == 0
        assert (
            response.wss_url
            == "wss://console.hetzner.cloud/?server_id=1&token=3db32d15-af2f-459c-8bf8-dee1fd05f49c"
        )
        assert response.password == "9MQaTg2VAGI0FIpc10k3UpRXcHj2wQ6x"

    @pytest.mark.parametrize(
        "network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))]
    )
    def test_attach_to_network(
        self, hetzner_client, bound_server, network, response_attach_to_network
    ):
        hetzner_client.request.return_value = response_attach_to_network
        action = bound_server.attach_to_network(
            network, "10.0.1.1", ["10.0.1.2", "10.0.1.3"]
        )
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/attach_to_network",
            method="POST",
            json={
                "network": 4711,
                "ip": "10.0.1.1",
                "alias_ips": ["10.0.1.2", "10.0.1.3"],
            },
        )

        assert action.id == 1
        assert action.progress == 0
        assert action.command == "attach_to_network"

    @pytest.mark.parametrize(
        "network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))]
    )
    def test_detach_from_network(
        self, hetzner_client, bound_server, network, response_detach_from_network
    ):
        hetzner_client.request.return_value = response_detach_from_network
        action = bound_server.detach_from_network(network)
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/detach_from_network",
            method="POST",
            json={"network": 4711},
        )

        assert action.id == 1
        assert action.progress == 0
        assert action.command == "detach_from_network"

    @pytest.mark.parametrize(
        "network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))]
    )
    def test_change_alias_ips(
        self, hetzner_client, bound_server, network, response_change_alias_ips
    ):
        hetzner_client.request.return_value = response_change_alias_ips
        action = bound_server.change_alias_ips(network, ["10.0.1.2", "10.0.1.3"])
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/change_alias_ips",
            method="POST",
            json={"network": 4711, "alias_ips": ["10.0.1.2", "10.0.1.3"]},
        )

        assert action.id == 1
        assert action.progress == 0
        assert action.command == "change_alias_ips"

    @pytest.mark.parametrize(
        "placement_group",
        [PlacementGroup(id=897), BoundPlacementGroup(mock.MagicMock, dict(id=897))],
    )
    def test_add_to_placement_group(
        self,
        hetzner_client,
        bound_server,
        placement_group,
        response_add_to_placement_group,
    ):
        hetzner_client.request.return_value = response_add_to_placement_group
        action = bound_server.add_to_placement_group(placement_group)
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/add_to_placement_group",
            method="POST",
            json={"placement_group": "897"},
        )

        assert action.id == 13
        assert action.progress == 0
        assert action.command == "add_to_placement_group"

    def test_remove_from_placement_group(
        self, hetzner_client, bound_server, response_remove_from_placement_group
    ):
        hetzner_client.request.return_value = response_remove_from_placement_group
        action = bound_server.remove_from_placement_group()
        hetzner_client.request.assert_called_with(
            url="/servers/14/actions/remove_from_placement_group", method="POST"
        )

        assert action.id == 13
        assert action.progress == 100
        assert action.command == "remove_from_placement_group"


class TestServersClient:
    @pytest.fixture()
    def servers_client(self):
        return ServersClient(client=mock.MagicMock())

    def test_get_by_id(self, servers_client, response_simple_server):
        servers_client._client.request.return_value = response_simple_server
        bound_server = servers_client.get_by_id(1)
        servers_client._client.request.assert_called_with(
            url="/servers/1", method="GET"
        )
        assert bound_server._client is servers_client
        assert bound_server.id == 1
        assert bound_server.name == "my-server"

    @pytest.mark.parametrize(
        "params",
        [
            {"name": "server1", "label_selector": "label1", "page": 1, "per_page": 10},
            {"name": ""},
            {},
        ],
    )
    def test_get_list(self, servers_client, response_simple_servers, params):
        servers_client._client.request.return_value = response_simple_servers
        result = servers_client.get_list(**params)
        servers_client._client.request.assert_called_with(
            url="/servers", method="GET", params=params
        )

        bound_servers = result.servers
        assert result.meta is None

        assert len(bound_servers) == 2

        bound_server1 = bound_servers[0]
        bound_server2 = bound_servers[1]

        assert bound_server1._client is servers_client
        assert bound_server1.id == 1
        assert bound_server1.name == "my-server"

        assert bound_server2._client is servers_client
        assert bound_server2.id == 2
        assert bound_server2.name == "my-server2"

    @pytest.mark.parametrize(
        "params", [{"name": "server1", "label_selector": "label1"}, {}]
    )
    def test_get_all(self, servers_client, response_simple_servers, params):
        servers_client._client.request.return_value = response_simple_servers
        bound_servers = servers_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        servers_client._client.request.assert_called_with(
            url="/servers", method="GET", params=params
        )

        assert len(bound_servers) == 2

        bound_server1 = bound_servers[0]
        bound_server2 = bound_servers[1]

        assert bound_server1._client is servers_client
        assert bound_server1.id == 1
        assert bound_server1.name == "my-server"

        assert bound_server2._client is servers_client
        assert bound_server2.id == 2
        assert bound_server2.name == "my-server2"

    def test_get_by_name(self, servers_client, response_simple_servers):
        servers_client._client.request.return_value = response_simple_servers
        bound_server = servers_client.get_by_name("my-server")

        params = {"name": "my-server"}

        servers_client._client.request.assert_called_with(
            url="/servers", method="GET", params=params
        )

        assert bound_server._client is servers_client
        assert bound_server.id == 1
        assert bound_server.name == "my-server"

    def test_create_with_datacenter(
        self, servers_client, response_create_simple_server
    ):
        servers_client._client.request.return_value = response_create_simple_server
        response = servers_client.create(
            "my-server",
            server_type=ServerType(name="cx11"),
            image=Image(id=4711),
            datacenter=Datacenter(id=1),
        )
        servers_client._client.request.assert_called_with(
            url="/servers",
            method="POST",
            json={
                "name": "my-server",
                "server_type": "cx11",
                "image": 4711,
                "datacenter": 1,
                "start_after_create": True,
            },
        )

        bound_server = response.server
        bound_action = response.action

        assert bound_server._client is servers_client
        assert bound_server.id == 1
        assert bound_server.name == "my-server"

        assert isinstance(bound_action, BoundAction)
        assert bound_action._client == servers_client._client.actions
        assert bound_action.id == 1
        assert bound_action.command == "create_server"

    def test_create_with_location(self, servers_client, response_create_simple_server):
        servers_client._client.request.return_value = response_create_simple_server
        response = servers_client.create(
            "my-server",
            server_type=ServerType(name="cx11"),
            image=Image(name="ubuntu-20.04"),
            location=Location(name="fsn1"),
        )
        servers_client._client.request.assert_called_with(
            url="/servers",
            method="POST",
            json={
                "name": "my-server",
                "server_type": "cx11",
                "image": "ubuntu-20.04",
                "location": "fsn1",
                "start_after_create": True,
            },
        )

        bound_server = response.server
        bound_action = response.action

        assert bound_server._client is servers_client
        assert bound_server.id == 1
        assert bound_server.name == "my-server"

        assert isinstance(bound_action, BoundAction)
        assert bound_action._client == servers_client._client.actions
        assert bound_action.id == 1
        assert bound_action.command == "create_server"

    def test_create_with_volumes(self, servers_client, response_create_simple_server):
        servers_client._client.request.return_value = response_create_simple_server
        volumes = [Volume(id=1), BoundVolume(mock.MagicMock(), dict(id=2))]
        response = servers_client.create(
            "my-server",
            server_type=ServerType(name="cx11"),
            image=Image(id=4711),
            volumes=volumes,
            start_after_create=False,
        )
        servers_client._client.request.assert_called_with(
            url="/servers",
            method="POST",
            json={
                "name": "my-server",
                "server_type": "cx11",
                "image": 4711,
                "volumes": [1, 2],
                "start_after_create": False,
            },
        )

        bound_server = response.server
        bound_action = response.action
        next_actions = response.next_actions
        root_password = response.root_password

        assert root_password == "YItygq1v3GYjjMomLaKc"

        assert bound_server._client is servers_client
        assert bound_server.id == 1
        assert bound_server.name == "my-server"

        assert isinstance(bound_action, BoundAction)
        assert bound_action._client == servers_client._client.actions
        assert bound_action.id == 1
        assert bound_action.command == "create_server"

        assert next_actions[0].id == 13

    def test_create_with_networks(self, servers_client, response_create_simple_server):
        servers_client._client.request.return_value = response_create_simple_server
        networks = [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=2))]
        response = servers_client.create(
            "my-server",
            server_type=ServerType(name="cx11"),
            image=Image(id=4711),
            networks=networks,
            start_after_create=False,
        )
        servers_client._client.request.assert_called_with(
            url="/servers",
            method="POST",
            json={
                "name": "my-server",
                "server_type": "cx11",
                "image": 4711,
                "networks": [1, 2],
                "start_after_create": False,
            },
        )

        bound_server = response.server
        bound_action = response.action
        next_actions = response.next_actions
        root_password = response.root_password

        assert root_password == "YItygq1v3GYjjMomLaKc"

        assert bound_server._client is servers_client
        assert bound_server.id == 1
        assert bound_server.name == "my-server"

        assert isinstance(bound_action, BoundAction)
        assert bound_action._client == servers_client._client.actions
        assert bound_action.id == 1
        assert bound_action.command == "create_server"

        assert next_actions[0].id == 13

    def test_create_with_firewalls(self, servers_client, response_create_simple_server):
        servers_client._client.request.return_value = response_create_simple_server
        firewalls = [Firewall(id=1), BoundFirewall(mock.MagicMock(), dict(id=2))]
        response = servers_client.create(
            "my-server",
            server_type=ServerType(name="cx11"),
            image=Image(id=4711),
            firewalls=firewalls,
            start_after_create=False,
        )
        servers_client._client.request.assert_called_with(
            url="/servers",
            method="POST",
            json={
                "name": "my-server",
                "server_type": "cx11",
                "image": 4711,
                "firewalls": [{"firewall": 1}, {"firewall": 2}],
                "start_after_create": False,
            },
        )

        bound_server = response.server
        bound_action = response.action
        next_actions = response.next_actions
        root_password = response.root_password

        assert root_password == "YItygq1v3GYjjMomLaKc"

        assert bound_server._client is servers_client
        assert bound_server.id == 1
        assert bound_server.name == "my-server"

        assert isinstance(bound_action, BoundAction)
        assert bound_action._client == servers_client._client.actions
        assert bound_action.id == 1
        assert bound_action.command == "create_server"

        assert next_actions[0].id == 13

    def test_create_with_placement_group(
        self, servers_client, response_create_simple_server
    ):
        servers_client._client.request.return_value = response_create_simple_server
        placement_group = PlacementGroup(id=1)
        response = servers_client.create(
            "my-server",
            server_type=ServerType(name="cx11"),
            image=Image(id=4711),
            start_after_create=False,
            placement_group=placement_group,
        )

        servers_client._client.request.assert_called_with(
            url="/servers",
            method="POST",
            json={
                "name": "my-server",
                "server_type": "cx11",
                "image": 4711,
                "placement_group": 1,
                "start_after_create": False,
            },
        )

        bound_server = response.server
        bound_action = response.action
        next_actions = response.next_actions
        root_password = response.root_password

        assert root_password == "YItygq1v3GYjjMomLaKc"

        assert bound_server._client is servers_client
        assert bound_server.id == 1
        assert bound_server.name == "my-server"

        assert isinstance(bound_action, BoundAction)
        assert bound_action._client == servers_client._client.actions
        assert bound_action.id == 1
        assert bound_action.command == "create_server"

        assert next_actions[0].id == 13

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_get_actions_list(self, servers_client, server, response_get_actions):
        servers_client._client.request.return_value = response_get_actions
        result = servers_client.get_actions_list(server)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions", method="GET", params={}
        )

        actions = result.actions
        assert result.meta is None

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)

        assert actions[0]._client == servers_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "start_server"

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_update(self, servers_client, server, response_update_server):
        servers_client._client.request.return_value = response_update_server
        server = servers_client.update(server, name="new-name", labels={})
        servers_client._client.request.assert_called_with(
            url="/servers/1", method="PUT", json={"name": "new-name", "labels": {}}
        )

        assert server.id == 14
        assert server.name == "new-name"

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(self, servers_client, server, generic_action):
        servers_client._client.request.return_value = generic_action
        action = servers_client.delete(server)
        servers_client._client.request.assert_called_with(
            url="/servers/1", method="DELETE"
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_power_off(self, servers_client, server, generic_action):
        servers_client._client.request.return_value = generic_action
        action = servers_client.power_off(server)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/poweroff", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_power_on(self, servers_client, server, generic_action):
        servers_client._client.request.return_value = generic_action
        action = servers_client.power_on(server)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/poweron", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_reboot(self, servers_client, server, generic_action):
        servers_client._client.request.return_value = generic_action
        action = servers_client.reboot(server)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/reboot", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_reset(self, servers_client, server, generic_action):
        servers_client._client.request.return_value = generic_action
        action = servers_client.reset(server)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/reset", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_shutdown(self, servers_client, server, generic_action):
        servers_client._client.request.return_value = generic_action
        action = servers_client.shutdown(server)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/shutdown", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_reset_password(
        self, servers_client, server, response_server_reset_password
    ):
        servers_client._client.request.return_value = response_server_reset_password
        response = servers_client.reset_password(server)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/reset_password", method="POST"
        )

        assert response.action.id == 1
        assert response.action.progress == 0
        assert response.root_password == "YItygq1v3GYjjMomLaKc"

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_change_type_with_server_type_name(
        self, servers_client, server, generic_action
    ):
        servers_client._client.request.return_value = generic_action
        action = servers_client.change_type(
            server, ServerType(name="cx11"), upgrade_disk=True
        )
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/change_type",
            method="POST",
            json={"server_type": "cx11", "upgrade_disk": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_change_type_with_server_type_id(
        self, servers_client, server, generic_action
    ):
        servers_client._client.request.return_value = generic_action
        action = servers_client.change_type(server, ServerType(id=1), upgrade_disk=True)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/change_type",
            method="POST",
            json={"server_type": 1, "upgrade_disk": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_change_type_with_blank_server_type(self, servers_client, server):
        with pytest.raises(ValueError) as e:
            servers_client.change_type(server, ServerType(), upgrade_disk=True)
        assert str(e.value) == "id or name must be set"
        servers_client._client.request.assert_not_called()

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_enable_rescue(self, servers_client, server, response_server_enable_rescue):
        servers_client._client.request.return_value = response_server_enable_rescue
        response = servers_client.enable_rescue(server, "linux64", [2323])
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/enable_rescue",
            method="POST",
            json={"type": "linux64", "ssh_keys": [2323]},
        )

        assert response.action.id == 1
        assert response.action.progress == 0
        assert response.root_password == "YItygq1v3GYjjMomLaKc"

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_disable_rescue(self, servers_client, server, generic_action):
        servers_client._client.request.return_value = generic_action
        action = servers_client.disable_rescue(server)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/disable_rescue", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_create_image(self, servers_client, server, response_server_create_image):
        servers_client._client.request.return_value = response_server_create_image
        response = servers_client.create_image(
            server, description="my image", type="snapshot", labels={"key": "value"}
        )
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/create_image",
            method="POST",
            json={
                "description": "my image",
                "type": "snapshot",
                "labels": {"key": "value"},
            },
        )

        assert response.action.id == 1
        assert response.action.progress == 0
        assert response.image.description == "my image"

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_rebuild(self, servers_client, server, generic_action):
        servers_client._client.request.return_value = generic_action
        response = servers_client.rebuild(
            server,
            Image(name="ubuntu-20.04"),
            return_response=True,
        )
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/rebuild",
            method="POST",
            json={"image": "ubuntu-20.04"},
        )

        assert response.action.id == 1
        assert response.action.progress == 0
        assert response.root_password is None or isinstance(response.root_password, str)

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_enable_backup(self, servers_client, server, generic_action):
        servers_client._client.request.return_value = generic_action
        action = servers_client.enable_backup(server)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/enable_backup", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_disable_backup(self, servers_client, server, generic_action):
        servers_client._client.request.return_value = generic_action
        action = servers_client.disable_backup(server)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/disable_backup", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_attach_iso(self, servers_client, server, generic_action):
        servers_client._client.request.return_value = generic_action
        action = servers_client.attach_iso(
            server, Iso(name="FreeBSD-11.0-RELEASE-amd64-dvd1")
        )
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/attach_iso",
            method="POST",
            json={"iso": "FreeBSD-11.0-RELEASE-amd64-dvd1"},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_detach_iso(self, servers_client, server, generic_action):
        servers_client._client.request.return_value = generic_action
        action = servers_client.detach_iso(server)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/detach_iso", method="POST"
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_change_dns_ptr(self, servers_client, server, generic_action):
        servers_client._client.request.return_value = generic_action
        action = servers_client.change_dns_ptr(server, "1.2.3.4", "example.com")
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/change_dns_ptr",
            method="POST",
            json={"ip": "1.2.3.4", "dns_ptr": "example.com"},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_change_protection(self, servers_client, server, generic_action):
        servers_client._client.request.return_value = generic_action
        action = servers_client.change_protection(server, True, True)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/change_protection",
            method="POST",
            json={"delete": True, "rebuild": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_request_console(
        self, servers_client, server, response_server_request_console
    ):
        servers_client._client.request.return_value = response_server_request_console
        response = servers_client.request_console(server)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/request_console", method="POST"
        )

        assert response.action.id == 1
        assert response.action.progress == 0
        assert (
            response.wss_url
            == "wss://console.hetzner.cloud/?server_id=1&token=3db32d15-af2f-459c-8bf8-dee1fd05f49c"
        )
        assert response.password == "9MQaTg2VAGI0FIpc10k3UpRXcHj2wQ6x"

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    @pytest.mark.parametrize(
        "network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))]
    )
    def test_attach_to_network(
        self, servers_client, server, network, response_attach_to_network
    ):
        servers_client._client.request.return_value = response_attach_to_network
        action = servers_client.attach_to_network(
            server, network, "10.0.1.1", ["10.0.1.2", "10.0.1.3"]
        )
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/attach_to_network",
            method="POST",
            json={
                "network": 4711,
                "ip": "10.0.1.1",
                "alias_ips": ["10.0.1.2", "10.0.1.3"],
            },
        )

        assert action.id == 1
        assert action.progress == 0
        assert action.command == "attach_to_network"

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    @pytest.mark.parametrize(
        "network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))]
    )
    def test_detach_from_network(
        self, servers_client, server, network, response_detach_from_network
    ):
        servers_client._client.request.return_value = response_detach_from_network
        action = servers_client.detach_from_network(server, network)
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/detach_from_network",
            method="POST",
            json={"network": 4711},
        )

        assert action.id == 1
        assert action.progress == 0
        assert action.command == "detach_from_network"

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    @pytest.mark.parametrize(
        "network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))]
    )
    def test_change_alias_ips(
        self, servers_client, server, network, response_change_alias_ips
    ):
        servers_client._client.request.return_value = response_change_alias_ips
        action = servers_client.change_alias_ips(
            server, network, ["10.0.1.2", "10.0.1.3"]
        )
        servers_client._client.request.assert_called_with(
            url="/servers/1/actions/change_alias_ips",
            method="POST",
            json={"network": 4711, "alias_ips": ["10.0.1.2", "10.0.1.3"]},
        )

        assert action.id == 1
        assert action.progress == 0
        assert action.command == "change_alias_ips"

    def test_actions_get_by_id(self, servers_client, response_get_actions):
        servers_client._client.request.return_value = {
            "action": response_get_actions["actions"][0]
        }
        action = servers_client.actions.get_by_id(13)

        servers_client._client.request.assert_called_with(
            url="/servers/actions/13", method="GET"
        )

        assert isinstance(action, BoundAction)
        assert action._client == servers_client._client.actions
        assert action.id == 13
        assert action.command == "start_server"

    def test_actions_get_list(self, servers_client, response_get_actions):
        servers_client._client.request.return_value = response_get_actions
        result = servers_client.actions.get_list()

        servers_client._client.request.assert_called_with(
            url="/servers/actions",
            method="GET",
            params={},
        )

        actions = result.actions
        assert result.meta is None

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == servers_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "start_server"

    def test_actions_get_all(self, servers_client, response_get_actions):
        servers_client._client.request.return_value = response_get_actions
        actions = servers_client.actions.get_all()

        servers_client._client.request.assert_called_with(
            url="/servers/actions",
            method="GET",
            params={"page": 1, "per_page": 50},
        )

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == servers_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "start_server"
