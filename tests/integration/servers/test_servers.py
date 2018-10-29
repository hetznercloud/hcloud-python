import mock
import pytest

from hcloud.servers.client import BoundServer
from hcloud.servers.domain import Server
from hcloud.volumes.domain import Volume


class TestBoundServer(object):

    @pytest.fixture()
    def bound_server(self, hetzner_client):
        return BoundServer(client=hetzner_client.servers, data=dict(id=42))

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


class TestServersClient(object):

    def test_get_by_id(self, hetzner_client):
        server = hetzner_client.servers.get_by_id(42)
        assert server.id == 42
        assert server.volumes == []
        assert server.server_type['id'] == 1
        assert server.datacenter['id'] == 1
        assert server.image['id'] == 4711

    def test_get_all(self, hetzner_client):
        servers = hetzner_client.servers.get_all(42)
        assert servers[0].id == 42
        assert servers[0].volumes == []
        assert servers[0].server_type['id'] == 1
        assert servers[0].datacenter['id'] == 1
        assert servers[0].image['id'] == 4711

    def test_create(self, hetzner_client):

        response = hetzner_client.servers.create(
            "my-server",
            "cx11",
            "ubuntu-16.04",
            ssh_keys=["my-ssh-key"],
            volumes=[Volume(id=1)],
            user_data="#cloud-config\\nruncmd:\\n- [touch, /root/cloud-init-worked]\\n",
            location="nbg1"

        )
        server = response.server
        action = response.action
        next_actions = response.next_actions
        root_password = response.root_password

        assert server.id == 42
        assert server.volumes == []
        assert server.server_type['id'] == 1
        assert server.datacenter['id'] == 1
        assert server.image['id'] == 4711

        assert action.id == 1
        assert action.command == "create_server"

        assert len(next_actions) == 1
        assert next_actions[0].id == 13
        assert next_actions[0].command == "start_server"

        assert root_password == "YItygq1v3GYjjMomLaKc"

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
