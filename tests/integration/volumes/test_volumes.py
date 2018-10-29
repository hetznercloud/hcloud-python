import pytest
import mock

from hcloud.servers.client import BoundServer
from hcloud.servers.domain import Server
from hcloud.volumes.client import BoundVolume
from hcloud.volumes.domain import Volume


class TestBoundVolume(object):

    @pytest.fixture()
    def bound_volume(self, hetzner_client):
        return BoundVolume(client=hetzner_client.volumes, data=dict(id=4711))

    @pytest.mark.parametrize("server",
                             (Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))))
    def test_attach(self, hetzner_client, bound_volume, server):
        action = bound_volume.attach(server)
        assert action.id == 13
        assert action.progress == 0
        assert action.command == "attach_volume"

    def test_detach(self, hetzner_client, bound_volume):
        action = bound_volume.detach()
        assert action.id == 13
        assert action.progress == 0
        assert action.command == "detach_volume"


class TestVolumesClient(object):

    def test_get_by_id(self, hetzner_client):
        bound_volume = hetzner_client.volumes.get_by_id(4711)
        assert bound_volume.id == 4711
        assert bound_volume.name == "database-storage"
        assert bound_volume.size == 42

    def test_get_all(self, hetzner_client):
        bound_volumes = hetzner_client.volumes.get_all()
        assert bound_volumes[0].id == 4711
        assert bound_volumes[0].name == "database-storage"
        assert bound_volumes[0].size == 42

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_create(self, hetzner_client, server):
        response = hetzner_client.volumes.create(
            42,
            "test-database",
            location="nbg1",
        )

        volume = response.volume
        action = response.action
        next_actions = response.next_actions

        assert volume.id == 4711
        assert volume.name == "database-storage"
        assert volume.size == 42

        assert action.id == 13
        assert action.command == "create_volume"

        assert len(next_actions) == 1
        assert next_actions[0].id == 13
        assert next_actions[0].command == "start_server"

    @pytest.mark.parametrize("server,volume",
                             [(Server(id=43), Volume(id=4711)),
                              (BoundServer(mock.MagicMock(), dict(id=43)), BoundVolume(mock.MagicMock(), dict(id=4711)))])
    def test_attach(self, hetzner_client, server, volume):
        action = hetzner_client.volumes.attach(server, volume)
        assert action.id == 13
        assert action.progress == 0
        assert action.command == "attach_volume"

    @pytest.mark.parametrize("volume", [Volume(id=4711), BoundVolume(mock.MagicMock(), dict(id=4711))])
    def test_detach(self, hetzner_client, volume):
        action = hetzner_client.volumes.detach(volume)
        assert action.id == 13
        assert action.progress == 0
        assert action.command == "detach_volume"
