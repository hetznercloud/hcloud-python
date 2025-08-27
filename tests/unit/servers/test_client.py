from __future__ import annotations

from unittest import mock

import pytest

from hcloud import Client
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

from ..conftest import BoundModelTestCase


class TestBoundServer(BoundModelTestCase):
    methods = [
        BoundServer.update,
        BoundServer.delete,
        BoundServer.add_to_placement_group,
        BoundServer.remove_from_placement_group,
        BoundServer.attach_iso,
        BoundServer.detach_iso,
        BoundServer.attach_to_network,
        BoundServer.detach_from_network,
        BoundServer.change_alias_ips,
        BoundServer.change_dns_ptr,
        BoundServer.change_protection,
        BoundServer.change_type,
        BoundServer.create_image,
        BoundServer.disable_backup,
        BoundServer.enable_backup,
        BoundServer.disable_rescue,
        BoundServer.enable_rescue,
        BoundServer.get_metrics,
        BoundServer.power_off,
        BoundServer.power_on,
        BoundServer.reboot,
        BoundServer.rebuild,
        BoundServer.shutdown,
        BoundServer.reset,
        BoundServer.request_console,
        BoundServer.reset_password,
    ]

    @pytest.fixture()
    def resource_client(self, client: Client):
        return client.servers

    @pytest.fixture()
    def bound_model(self, resource_client: ServersClient):
        return BoundServer(resource_client, data=dict(id=14))

    def test_init(self, response_full_server):
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
            bound_server.datacenter._client == bound_server._client._parent.datacenters
        )
        assert bound_server.datacenter.id == 1
        assert bound_server.datacenter.complete is True

        assert isinstance(bound_server.server_type, BoundServerType)
        assert (
            bound_server.server_type._client
            == bound_server._client._parent.server_types
        )
        assert bound_server.server_type.id == 1
        assert bound_server.server_type.complete is True

        assert len(bound_server.volumes) == 2
        assert isinstance(bound_server.volumes[0], BoundVolume)
        assert bound_server.volumes[0]._client == bound_server._client._parent.volumes
        assert bound_server.volumes[0].id == 1
        assert bound_server.volumes[0].complete is False

        assert isinstance(bound_server.volumes[1], BoundVolume)
        assert bound_server.volumes[1]._client == bound_server._client._parent.volumes
        assert bound_server.volumes[1].id == 2
        assert bound_server.volumes[1].complete is False

        assert isinstance(bound_server.image, BoundImage)
        assert bound_server.image._client == bound_server._client._parent.images
        assert bound_server.image.id == 4711
        assert bound_server.image.name == "ubuntu-20.04"
        assert bound_server.image.complete is True

        assert isinstance(bound_server.iso, BoundIso)
        assert bound_server.iso._client == bound_server._client._parent.isos
        assert bound_server.iso.id == 4711
        assert bound_server.iso.name == "FreeBSD-11.0-RELEASE-amd64-dvd1"
        assert bound_server.iso.complete is True

        assert len(bound_server.private_net) == 1
        assert isinstance(bound_server.private_net[0], PrivateNet)
        assert (
            bound_server.private_net[0].network._client
            == bound_server._client._parent.networks
        )
        assert bound_server.private_net[0].ip == "10.1.1.5"
        assert bound_server.private_net[0].mac_address == "86:00:ff:2a:7d:e1"
        assert len(bound_server.private_net[0].alias_ips) == 1
        assert bound_server.private_net[0].alias_ips[0] == "10.1.1.8"

        assert isinstance(bound_server.placement_group, BoundPlacementGroup)
        assert (
            bound_server.placement_group._client
            == bound_server._client._parent.placement_groups
        )
        assert bound_server.placement_group.id == 897
        assert bound_server.placement_group.name == "my Placement Group"
        assert bound_server.placement_group.complete is True


class TestServersClient:
    @pytest.fixture()
    def servers_client(self, client: Client):
        return ServersClient(client)

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        response_simple_server,
    ):
        request_mock.return_value = response_simple_server

        bound_server = servers_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/servers/1",
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
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        response_simple_servers,
        params,
    ):
        request_mock.return_value = response_simple_servers

        result = servers_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/servers",
            params=params,
        )

        bound_servers = result.servers
        assert result.meta is not None

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
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        response_simple_servers,
        params,
    ):
        request_mock.return_value = response_simple_servers

        bound_servers = servers_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/servers",
            params=params,
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

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        response_simple_servers,
    ):
        request_mock.return_value = response_simple_servers

        bound_server = servers_client.get_by_name("my-server")

        params = {"name": "my-server"}

        request_mock.assert_called_with(
            method="GET",
            url="/servers",
            params=params,
        )

        assert bound_server._client is servers_client
        assert bound_server.id == 1
        assert bound_server.name == "my-server"

    def test_create_with_datacenter(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        response_create_simple_server,
    ):
        request_mock.return_value = response_create_simple_server

        response = servers_client.create(
            "my-server",
            server_type=ServerType(name="cx11"),
            image=Image(id=4711),
            datacenter=Datacenter(id=1),
        )

        request_mock.assert_called_with(
            method="POST",
            url="/servers",
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
        assert bound_action._client == servers_client._parent.actions
        assert bound_action.id == 1
        assert bound_action.command == "create_server"

    def test_create_with_location(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        response_create_simple_server,
    ):
        request_mock.return_value = response_create_simple_server

        response = servers_client.create(
            "my-server",
            server_type=ServerType(name="cx11"),
            image=Image(name="ubuntu-20.04"),
            location=Location(name="fsn1"),
        )

        request_mock.assert_called_with(
            method="POST",
            url="/servers",
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
        assert bound_action._client == servers_client._parent.actions
        assert bound_action.id == 1
        assert bound_action.command == "create_server"

    def test_create_with_volumes(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        response_create_simple_server,
    ):
        request_mock.return_value = response_create_simple_server

        volumes = [Volume(id=1), BoundVolume(mock.MagicMock(), dict(id=2))]
        response = servers_client.create(
            "my-server",
            server_type=ServerType(name="cx11"),
            image=Image(id=4711),
            volumes=volumes,
            start_after_create=False,
        )

        request_mock.assert_called_with(
            method="POST",
            url="/servers",
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
        assert bound_action._client == servers_client._parent.actions
        assert bound_action.id == 1
        assert bound_action.command == "create_server"

        assert next_actions[0].id == 13

    def test_create_with_networks(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        response_create_simple_server,
    ):
        request_mock.return_value = response_create_simple_server

        networks = [Network(id=1), BoundNetwork(mock.MagicMock(), dict(id=2))]
        response = servers_client.create(
            "my-server",
            server_type=ServerType(name="cx11"),
            image=Image(id=4711),
            networks=networks,
            start_after_create=False,
        )

        request_mock.assert_called_with(
            method="POST",
            url="/servers",
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
        assert bound_action._client == servers_client._parent.actions
        assert bound_action.id == 1
        assert bound_action.command == "create_server"

        assert next_actions[0].id == 13

    def test_create_with_firewalls(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        response_create_simple_server,
    ):
        request_mock.return_value = response_create_simple_server

        firewalls = [Firewall(id=1), BoundFirewall(mock.MagicMock(), dict(id=2))]
        response = servers_client.create(
            "my-server",
            server_type=ServerType(name="cx11"),
            image=Image(id=4711),
            firewalls=firewalls,
            start_after_create=False,
        )

        request_mock.assert_called_with(
            method="POST",
            url="/servers",
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
        assert bound_action._client == servers_client._parent.actions
        assert bound_action.id == 1
        assert bound_action.command == "create_server"

        assert next_actions[0].id == 13

    def test_create_with_placement_group(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        response_create_simple_server,
    ):
        request_mock.return_value = response_create_simple_server

        placement_group = PlacementGroup(id=1)
        response = servers_client.create(
            "my-server",
            server_type=ServerType(name="cx11"),
            image=Image(id=4711),
            start_after_create=False,
            placement_group=placement_group,
        )

        request_mock.assert_called_with(
            method="POST",
            url="/servers",
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
        assert bound_action._client == servers_client._parent.actions
        assert bound_action.id == 1
        assert bound_action.command == "create_server"

        assert next_actions[0].id == 13

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_update(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        response_update_server,
    ):
        request_mock.return_value = response_update_server

        server = servers_client.update(server, name="new-name", labels={})

        request_mock.assert_called_with(
            method="PUT",
            url="/servers/1",
            json={"name": "new-name", "labels": {}},
        )

        assert server.id == 14
        assert server.name == "new-name"

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.delete(server)

        request_mock.assert_called_with(
            method="DELETE",
            url="/servers/1",
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_power_off(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.power_off(server)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/poweroff",
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_power_on(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.power_on(server)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/poweron",
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_reboot(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.reboot(server)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/reboot",
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_reset(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.reset(server)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/reset",
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_shutdown(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.shutdown(server)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/shutdown",
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_reset_password(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        response_server_reset_password,
    ):
        request_mock.return_value = response_server_reset_password

        response = servers_client.reset_password(server)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/reset_password",
        )

        assert response.action.id == 1
        assert response.action.progress == 0
        assert response.root_password == "YItygq1v3GYjjMomLaKc"

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_change_type_with_server_type_name(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.change_type(
            server, ServerType(name="cx11"), upgrade_disk=True
        )

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/change_type",
            json={"server_type": "cx11", "upgrade_disk": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_change_type_with_server_type_id(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.change_type(server, ServerType(id=1), upgrade_disk=True)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/change_type",
            json={"server_type": 1, "upgrade_disk": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_change_type_with_blank_server_type(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
    ):
        with pytest.raises(ValueError) as e:
            servers_client.change_type(server, ServerType(), upgrade_disk=True)
        assert str(e.value) == "id or name must be set"

        request_mock.assert_not_called()

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_enable_rescue(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        response_server_enable_rescue,
    ):
        request_mock.return_value = response_server_enable_rescue

        response = servers_client.enable_rescue(server, "linux64", [2323])

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/enable_rescue",
            json={"type": "linux64", "ssh_keys": [2323]},
        )

        assert response.action.id == 1
        assert response.action.progress == 0
        assert response.root_password == "YItygq1v3GYjjMomLaKc"

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_disable_rescue(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.disable_rescue(server)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/disable_rescue",
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_create_image(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        response_server_create_image,
    ):
        request_mock.return_value = response_server_create_image

        response = servers_client.create_image(
            server, description="my image", type="snapshot", labels={"key": "value"}
        )

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/create_image",
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
    def test_rebuild(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        response = servers_client.rebuild(
            server,
            Image(name="ubuntu-20.04"),
            return_response=True,
        )

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/rebuild",
            json={"image": "ubuntu-20.04"},
        )

        assert response.action.id == 1
        assert response.action.progress == 0
        assert response.root_password is None or isinstance(response.root_password, str)

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_enable_backup(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.enable_backup(server)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/enable_backup",
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_disable_backup(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.disable_backup(server)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/disable_backup",
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_attach_iso(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.attach_iso(
            server, Iso(name="FreeBSD-11.0-RELEASE-amd64-dvd1")
        )

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/attach_iso",
            json={"iso": "FreeBSD-11.0-RELEASE-amd64-dvd1"},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_detach_iso(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.detach_iso(server)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/detach_iso",
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_change_dns_ptr(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.change_dns_ptr(server, "1.2.3.4", "example.com")

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/change_dns_ptr",
            json={"ip": "1.2.3.4", "dns_ptr": "example.com"},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_change_protection(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        action_response,
    ):
        request_mock.return_value = action_response

        action = servers_client.change_protection(server, True, True)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/change_protection",
            json={"delete": True, "rebuild": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_request_console(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        response_server_request_console,
    ):
        request_mock.return_value = response_server_request_console

        response = servers_client.request_console(server)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/request_console",
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
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        network,
        response_attach_to_network,
    ):
        request_mock.return_value = response_attach_to_network

        action = servers_client.attach_to_network(
            server, network, "10.0.1.1", ["10.0.1.2", "10.0.1.3"]
        )

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/attach_to_network",
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
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        network,
        response_detach_from_network,
    ):
        request_mock.return_value = response_detach_from_network

        action = servers_client.detach_from_network(server, network)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/detach_from_network",
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
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        network,
        response_change_alias_ips,
    ):
        request_mock.return_value = response_change_alias_ips

        action = servers_client.change_alias_ips(
            server, network, ["10.0.1.2", "10.0.1.3"]
        )

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/change_alias_ips",
            json={"network": 4711, "alias_ips": ["10.0.1.2", "10.0.1.3"]},
        )

        assert action.id == 1
        assert action.progress == 0
        assert action.command == "change_alias_ips"

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    @pytest.mark.parametrize(
        "placement_group",
        [PlacementGroup(id=897), BoundPlacementGroup(mock.MagicMock, dict(id=897))],
    )
    def test_add_to_placement_group(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        placement_group,
        response_add_to_placement_group,
    ):
        request_mock.return_value = response_add_to_placement_group

        action = servers_client.add_to_placement_group(server, placement_group)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/add_to_placement_group",
            json={"placement_group": 897},
        )

        assert action.id == 13

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_remove_from_placement_group(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        response_remove_from_placement_group,
    ):
        request_mock.return_value = response_remove_from_placement_group

        action = servers_client.remove_from_placement_group(server)

        request_mock.assert_called_with(
            method="POST",
            url="/servers/1/actions/remove_from_placement_group",
        )

        assert action.id == 13

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_get_metrics(
        self,
        request_mock: mock.MagicMock,
        servers_client: ServersClient,
        server,
        response_get_metrics,
    ):
        request_mock.return_value = response_get_metrics

        response = servers_client.get_metrics(
            server,
            type=["cpu", "disk"],
            start="2023-12-14T17:40:00+01:00",
            end="2023-12-14T17:50:00+01:00",
        )

        request_mock.assert_called_with(
            method="GET",
            url="/servers/1/metrics",
            params={
                "type": "cpu,disk",
                "start": "2023-12-14T17:40:00+01:00",
                "end": "2023-12-14T17:50:00+01:00",
            },
        )

        assert "cpu" in response.metrics.time_series
        assert "disk.0.iops.read" in response.metrics.time_series
        assert len(response.metrics.time_series["disk.0.iops.read"]["values"]) == 3
