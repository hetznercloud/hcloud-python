import mock
import pytest

from hcloud import HcloudClient
from hcloud.servers.client import ServersClient, BoundServer

from hcloud.servers.domain import Server
from hcloud.volumes.client import BoundVolume
from hcloud.volumes.domain import Volume
from tests.unit.actions.fixtures import generic_action
from tests.unit.servers.fixtures import response_simple_server, response_simple_servers, response_full_server, response_create_simple_server


class TestBoundServer(object):

    @pytest.fixture()
    def hetzner_client(self):
        client = HcloudClient(token="token")
        patcher = mock.patch.object(client, "request")
        patcher.start()
        yield client
        patcher.stop()

    @pytest.fixture()
    def bound_server(self, hetzner_client):
        return BoundServer(client=hetzner_client.servers, data=dict(id=14))

    def test_bound_server_init(self):
        bound_server = BoundServer(
            client=mock.MagicMock(),
            data=response_full_server['server']
        )

        assert bound_server.id == 42
        assert bound_server.name == "my-server"
        assert bound_server.public_net["floating_ips"] == [478]
        assert bound_server.server_type == response_full_server['server']['server_type']
        assert bound_server.datacenter == response_full_server['server']['datacenter']
        assert bound_server.image == response_full_server['server']['image']
        assert bound_server.iso == response_full_server['server']['iso']

        assert len(bound_server.volumes) == 2

        assert isinstance(bound_server.volumes[0], BoundVolume)
        assert bound_server.volumes[0]._client == bound_server._client._client.volumes
        assert bound_server.volumes[0].id == 1
        assert bound_server.volumes[0].complete is False

        assert isinstance(bound_server.volumes[1], BoundVolume)
        assert bound_server.volumes[1]._client == bound_server._client._client.volumes
        assert bound_server.volumes[1].id == 2
        assert bound_server.volumes[1].complete is False

    def test_power_off(self, hetzner_client, bound_server):
        hetzner_client.request.return_value = generic_action
        action = bound_server.power_off()
        hetzner_client.request.assert_called_with(url="/servers/14/actions/poweroff", method="POST")

        assert action.id == 1
        assert action.progress == 0

    def test_power_on(self, hetzner_client, bound_server):
        hetzner_client.request.return_value = generic_action
        action = bound_server.power_on()
        hetzner_client.request.assert_called_with(url="/servers/14/actions/poweron", method="POST")

        assert action.id == 1
        assert action.progress == 0

    def test_reboot(self, hetzner_client, bound_server):
        hetzner_client.request.return_value = generic_action
        action = bound_server.reboot()
        hetzner_client.request.assert_called_with(url="/servers/14/actions/reboot", method="POST")

        assert action.id == 1
        assert action.progress == 0


class TestServersClient(object):

    @pytest.fixture()
    def servers_client(self):
        return ServersClient(client=mock.MagicMock())

    def test_get_by_id(self, servers_client):
        servers_client._client.request.return_value = response_simple_server
        bound_server = servers_client.get_by_id(1)
        servers_client._client.request.assert_called_with(url="/servers/1", method="GET")
        assert bound_server._client is servers_client
        assert bound_server.id == 1
        assert bound_server.name == "my-server"

    def test_get_all_no_params(self, servers_client):
        servers_client._client.request.return_value = response_simple_servers
        bound_servers = servers_client.get_all()
        servers_client._client.request.assert_called_with(url="/servers", method="GET", params={})

        assert len(bound_servers) == 2

        bound_server1 = bound_servers[0]
        bound_server2 = bound_servers[1]

        assert bound_server1._client is servers_client
        assert bound_server1.id == 1
        assert bound_server1.name == "my-server"

        assert bound_server2._client is servers_client
        assert bound_server2.id == 2
        assert bound_server2.name == "my-server2"

    @pytest.mark.parametrize("params", [{'name': "server1"}, {'name': "server1", 'label_selector': "label1"}, {'label_selector': "label1"}])
    def test_get_all_with_params(self, servers_client, params):
        servers_client.get_all(**params)
        servers_client._client.request.assert_called_with(url="/servers", method="GET", params=params)

    def test_create(self, servers_client):
        servers_client._client.request.return_value = response_create_simple_server
        response = servers_client.create(
            "my-server",
            "cx11",
            4711,
            datacenter="datacenter1"
        )
        servers_client._client.request.assert_called_with(
            url="/servers",
            method="POST",
            json={
                'name': "my-server",
                'server_type': "cx11",
                'image': 4711,
                'datacenter': 'datacenter1',
                "start_after_create": True
            }
        )

        bound_server = response.server

        assert bound_server._client is servers_client
        assert bound_server.id == 1
        assert bound_server.name == "my-server"

    def test_create_with_volumes(self, servers_client):
        servers_client._client.request.return_value = response_create_simple_server
        volumes = [Volume(id=1), BoundVolume(mock.MagicMock(), dict(id=2))]
        response = servers_client.create(
            "my-server",
            "cx11",
            4711,
            volumes=volumes,
            start_after_create=False
        )
        servers_client._client.request.assert_called_with(
            url="/servers",
            method="POST",
            json={
                'name': "my-server",
                'server_type': "cx11",
                'image': 4711,
                'volumes': ['1', '2'],
                "start_after_create": False
            }
        )

        bound_server = response.server
        action = response.action
        next_actions = response.next_actions
        root_password = response.root_password

        assert bound_server._client is servers_client
        assert bound_server.id == 1
        assert bound_server.name == "my-server"

        assert action.id == 1
        assert action.command == "create_server"

        assert next_actions[0].id == 13

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_power_off(self, servers_client, server):
        servers_client._client.request.return_value = generic_action
        action = servers_client.power_off(server)
        servers_client._client.request.assert_called_with(url="/servers/1/actions/poweroff", method="POST")

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_power_on(self, servers_client, server):
        servers_client._client.request.return_value = generic_action
        action = servers_client.power_on(server)
        servers_client._client.request.assert_called_with(url="/servers/1/actions/poweron", method="POST")

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_reboot(self, servers_client, server):
        servers_client._client.request.return_value = generic_action
        action = servers_client.reboot(server)
        servers_client._client.request.assert_called_with(url="/servers/1/actions/reboot", method="POST")

        assert action.id == 1
        assert action.progress == 0
