import mock
import pytest

from hcloud.networks.client import BoundNetwork
from hcloud.networks.domain import Network
from hcloud.servers.client import BoundServer
from hcloud.servers.domain import Server
from hcloud.ssh_keys.domain import SSHKey
from hcloud.volumes.domain import Volume
from hcloud.images.domain import Image
from hcloud.isos.domain import Iso
from hcloud.server_types.domain import ServerType
from hcloud.locations.domain import Location


class TestBoundServer(object):

    @pytest.fixture()
    def bound_server(self, hetzner_client):
        return BoundServer(client=hetzner_client.servers, data=dict(id=42))

    def test_get_actions_list(self, bound_server):
        result = bound_server.get_actions_list()
        actions = result.actions

        assert len(actions) == 1
        assert actions[0].id == 13
        assert actions[0].command == "start_server"

    def test_update(self, bound_server):
        server = bound_server.update(name="new-name", labels={})
        assert server.id == 42
        assert server.name == "new-name"

    def test_delete(self, bound_server):
        action = bound_server.delete()
        assert action.id == 13
        assert action.command == "delete_server"

    def test_power_off(self, bound_server):
        action = bound_server.power_off()
        assert action.id == 13
        assert action.command == "stop_server"

    def test_power_on(self, bound_server):
        action = bound_server.power_on()

        assert action.id == 13
        assert action.command == "start_server"

    def test_reboot(self, bound_server):
        action = bound_server.reboot()

        assert action.id == 13
        assert action.command == "reboot_server"

    def test_reset(self, bound_server):
        action = bound_server.reset()

        assert action.id == 13
        assert action.command == "reset_server"

    def test_reset_password(self, bound_server):
        response = bound_server.reset_password()

        assert response.action.id == 13
        assert response.action.command == "reset_password"
        assert response.root_password == "zCWbFhnu950dUTko5f40"

    def test_change_type(self, bound_server):
        action = bound_server.change_type(ServerType(name="cx11"), upgrade_disk=True)
        assert action.id == 13
        assert action.command == "change_server_type"

    def test_enable_rescue(self, bound_server):
        response = bound_server.enable_rescue(type="linux64", ssh_keys=[2323])

        assert response.action.id == 13
        assert response.action.command == "enable_rescue"
        assert response.root_password == "zCWbFhnu950dUTko5f40"

    def test_disable_rescue(self, bound_server):
        action = bound_server.disable_rescue()

        assert action.id == 13
        assert action.command == "disable_rescue"

    def test_create_image(self, bound_server):
        response = bound_server.create_image(description="my image", type="snapshot")

        assert response.action.id == 13
        assert response.action.command == "create_image"
        assert response.image.description == "my image"

    def test_rebuild(self, bound_server):
        action = bound_server.rebuild(Image(name="ubuntu-20.04"))

        assert action.id == 13
        assert action.command == "rebuild_server"

    def test_enable_backup(self, bound_server):
        action = bound_server.enable_backup()

        assert action.id == 13
        assert action.command == "enable_backup"

    def test_disable_backup(self, bound_server):
        action = bound_server.disable_backup()

        assert action.id == 13
        assert action.command == "disable_backup"

    def test_attach_iso(self, bound_server):
        action = bound_server.attach_iso(Iso(name="FreeBSD-11.0-RELEASE-amd64-dvd1"))

        assert action.id == 13
        assert action.command == "attach_iso"

    def test_detach_iso(self, bound_server):
        action = bound_server.detach_iso()

        assert action.id == 13
        assert action.command == "detach_iso"

    def test_change_dns_ptr(self, bound_server):
        action = bound_server.change_dns_ptr(ip="1.2.3.4", dns_ptr="example.com")

        assert action.id == 13
        assert action.command == "change_dns_ptr"

    def test_change_protection(self, bound_server):
        action = bound_server.change_protection(True, True)

        assert action.id == 13
        assert action.command == "change_protection"

    def test_request_console(self, bound_server):
        response = bound_server.request_console()

        assert response.action.id == 13
        assert response.action.command == "request_console"
        assert response.wss_url == "wss://console.hetzner.cloud/?server_id=1&token=3db32d15-af2f-459c-8bf8-dee1fd05f49c"
        assert response.password == "9MQaTg2VAGI0FIpc10k3UpRXcHj2wQ6x"

    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_attach_to_network(self, bound_server, network):
        action = bound_server.attach_to_network(network, ip="10.0.1.1", alias_ips=["10.0.1.2"])

        assert action.id == 13
        assert action.command == "attach_to_network"

    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_detach_from_network(self, bound_server, network):
        action = bound_server.detach_from_network(network)

        assert action.id == 13
        assert action.command == "detach_from_network"

    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_change_alias_ips(self, bound_server, network):
        action = bound_server.change_alias_ips(network, alias_ips=["10.0.1.2"])

        assert action.id == 13
        assert action.command == "change_alias_ips"


class TestServersClient(object):

    def test_get_by_id(self, hetzner_client):
        server = hetzner_client.servers.get_by_id(42)
        assert server.id == 42
        assert server.volumes == []
        assert server.server_type.id == 1
        assert server.datacenter.id == 1
        assert server.image.id == 4711

    def test_get_by_name(self, hetzner_client):
        server = hetzner_client.servers.get_by_name("my-server")
        assert server.id == 42
        assert server.name == "my-server"
        assert server.volumes == []
        assert server.server_type.id == 1
        assert server.datacenter.id == 1
        assert server.image.id == 4711

    def test_get_list(self, hetzner_client):
        result = hetzner_client.servers.get_list()
        servers = result.servers
        assert servers[0].id == 42
        assert servers[0].volumes == []
        assert servers[0].server_type.id == 1
        assert servers[0].datacenter.id == 1
        assert servers[0].image.id == 4711

    def test_create(self, hetzner_client):
        response = hetzner_client.servers.create(
            "my-server",
            server_type=ServerType(name="cx11"),
            image=Image(name="ubuntu-20.04"),
            ssh_keys=[SSHKey(name="my-ssh-key")],
            volumes=[Volume(id=1)],
            networks=[Network(id=1)],
            user_data="#cloud-config\\nruncmd:\\n- [touch, /root/cloud-init-worked]\\n",
            location=Location(name="nbg1"),
            automount=False

        )
        server = response.server
        action = response.action
        next_actions = response.next_actions
        root_password = response.root_password

        assert server.id == 42
        assert server.volumes == []
        assert server.server_type.id == 1
        assert server.datacenter.id == 1
        assert server.image.id == 4711

        assert action.id == 1
        assert action.command == "create_server"

        assert len(next_actions) == 1
        assert next_actions[0].id == 13
        assert next_actions[0].command == "start_server"

        assert root_password == "YItygq1v3GYjjMomLaKc"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_get_actions_list(self, hetzner_client, server):
        result = hetzner_client.servers.get_actions_list(server)
        actions = result.actions

        assert len(actions) == 1
        assert actions[0].id == 13
        assert actions[0].command == "start_server"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_update(self, hetzner_client, server):
        server = hetzner_client.servers.update(server, name="new-name", labels={})

        assert server.id == 42
        assert server.name == "new-name"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_delete(self, hetzner_client, server):
        action = hetzner_client.servers.delete(server)

        assert action.id == 13
        assert action.command == "delete_server"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_power_off(self, hetzner_client, server):
        action = hetzner_client.servers.power_off(server)

        assert action.id == 13
        assert action.command == "stop_server"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_power_on(self, hetzner_client, server):
        action = hetzner_client.servers.power_on(server)

        assert action.id == 13
        assert action.command == "start_server"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_reboot(self, hetzner_client, server):
        action = hetzner_client.servers.reboot(server)

        assert action.id == 13
        assert action.command == "reboot_server"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_reset(self, hetzner_client, server):
        action = hetzner_client.servers.reset(server)

        assert action.id == 13
        assert action.command == "reset_server"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_shutdown(self, hetzner_client, server):
        action = hetzner_client.servers.shutdown(server)

        assert action.id == 13
        assert action.command == "shutdown_server"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_reset_password(self, hetzner_client, server):
        response = hetzner_client.servers.reset_password(server)

        assert response.action.id == 13
        assert response.action.command == "reset_password"
        assert response.root_password == "zCWbFhnu950dUTko5f40"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_change_type(self, hetzner_client, server):
        action = hetzner_client.servers.change_type(server, ServerType(name="cx11"), upgrade_disk=True)

        assert action.id == 13
        assert action.command == "change_server_type"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_enable_rescue(self, hetzner_client, server):
        response = hetzner_client.servers.enable_rescue(server, type="linux64", ssh_keys=[2323])

        assert response.action.id == 13
        assert response.action.command == "enable_rescue"
        assert response.root_password == "zCWbFhnu950dUTko5f40"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_disable_rescue(self, hetzner_client, server):
        action = hetzner_client.servers.disable_rescue(server)

        assert action.id == 13
        assert action.command == "disable_rescue"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_create_image(self, hetzner_client, server):
        response = hetzner_client.servers.create_image(server, description="my image", type="snapshot")

        assert response.action.id == 13
        assert response.action.command == "create_image"
        assert response.image.description == "my image"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_rebuild(self, hetzner_client, server):
        action = hetzner_client.servers.rebuild(server, Image(name="ubuntu-20.04"))

        assert action.id == 13
        assert action.command == "rebuild_server"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_enable_backup(self, hetzner_client, server):
        action = hetzner_client.servers.enable_backup(server)

        assert action.id == 13
        assert action.command == "enable_backup"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_disable_backup(self, hetzner_client, server):
        action = hetzner_client.servers.disable_backup(server)

        assert action.id == 13
        assert action.command == "disable_backup"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_attach_iso(self, hetzner_client, server):
        action = hetzner_client.servers.attach_iso(server, Iso(name="FreeBSD-11.0-RELEASE-amd64-dvd1"))

        assert action.id == 13
        assert action.command == "attach_iso"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_detach_iso(self, hetzner_client, server):
        action = hetzner_client.servers.detach_iso(server)

        assert action.id == 13
        assert action.command == "detach_iso"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_change_dns_ptr(self, hetzner_client, server):
        action = hetzner_client.servers.change_dns_ptr(server, "1.2.3.4", "example.com")

        assert action.id == 13
        assert action.command == "change_dns_ptr"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_change_protection(self, hetzner_client, server):
        action = hetzner_client.servers.change_protection(server, delete=True, rebuild=True)

        assert action.id == 13
        assert action.command == "change_protection"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_request_console(self, hetzner_client, server):
        response = hetzner_client.servers.request_console(server)

        assert response.action.id == 13
        assert response.action.command == "request_console"
        assert response.wss_url == "wss://console.hetzner.cloud/?server_id=1&token=3db32d15-af2f-459c-8bf8-dee1fd05f49c"
        assert response.password == "9MQaTg2VAGI0FIpc10k3UpRXcHj2wQ6x"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_attach_to_network(self, hetzner_client, server, network):
        action = hetzner_client.servers.attach_to_network(server, network, ip="10.0.1.1", alias_ips=["10.0.1.2"])

        assert action.id == 13
        assert action.command == "attach_to_network"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_detach_from_network(self, hetzner_client, server, network):
        action = hetzner_client.servers.detach_from_network(server, network)

        assert action.id == 13
        assert action.command == "detach_from_network"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    @pytest.mark.parametrize("network", [Network(id=4711), BoundNetwork(mock.MagicMock(), dict(id=4711))])
    def test_change_alias_ips(self, hetzner_client, server, network):
        action = hetzner_client.servers.change_alias_ips(server, network, alias_ips=["10.0.1.2"])

        assert action.id == 13
        assert action.command == "change_alias_ips"
