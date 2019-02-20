import pytest
import mock

from hcloud.servers.client import BoundServer
from hcloud.servers.domain import Server
from hcloud.volumes.client import BoundVolume
from hcloud.volumes.domain import Volume
from hcloud.locations.domain import Location


class TestBoundVolume(object):

    @pytest.fixture()
    def bound_volume(self, hetzner_client):
        return BoundVolume(client=hetzner_client.volumes, data=dict(id=4711))

    def test_get_actions(self, bound_volume):
        actions = bound_volume.get_actions()

        assert len(actions) == 1
        assert actions[0].id == 13
        assert actions[0].command == "attach_volume"

    def test_update(self, bound_volume):
        volume = bound_volume.update(name="new-name", labels={})
        assert volume.id == 4711
        assert volume.name == "new-name"

    def test_delete(self, bound_volume):
        delete_success = bound_volume.delete()
        assert delete_success is True

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

    def test_resize(self, hetzner_client, bound_volume):
        action = bound_volume.resize(50)
        assert action.id == 13
        assert action.progress == 0
        assert action.command == "resize_volume"


class TestVolumesClient(object):

    def test_get_by_id(self, hetzner_client):
        bound_volume = hetzner_client.volumes.get_by_id(4711)
        assert bound_volume.id == 4711
        assert bound_volume.name == "database-storage"
        assert bound_volume.size == 42

    def test_get_by_name(self, hetzner_client):
        bound_volume = hetzner_client.volumes.get_by_name("database-storage")
        assert bound_volume.id == 4711
        assert bound_volume.name == "database-storage"
        assert bound_volume.size == 42

    def test_get_list(self, hetzner_client):
        result = hetzner_client.volumes.get_list()
        bound_volumes = result.volumes
        assert bound_volumes[0].id == 4711
        assert bound_volumes[0].name == "database-storage"
        assert bound_volumes[0].size == 42

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_create(self, hetzner_client, server):
        response = hetzner_client.volumes.create(
            42,
            "test-database",
            location=Location(name="nbg1"),
            automount=False,
            format="xfs"
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

    @pytest.mark.parametrize("volume", [Volume(id=1), BoundVolume(mock.MagicMock(), dict(id=1))])
    def test_get_actions(self, hetzner_client, volume):
        actions = hetzner_client.volumes.get_actions(volume)

        assert len(actions) == 1
        assert actions[0].id == 13
        assert actions[0].command == "attach_volume"

    @pytest.mark.parametrize("volume", [Volume(id=1), BoundVolume(mock.MagicMock(), dict(id=1))])
    def test_update(self, hetzner_client, volume):
        volume = hetzner_client.volumes.update(volume, name="new-name", labels={})

        assert volume.id == 4711
        assert volume.name == "new-name"

    @pytest.mark.parametrize("volume", [Volume(id=1), BoundVolume(mock.MagicMock(), dict(id=1))])
    def test_delete(self, hetzner_client, volume):
        delete_success = hetzner_client.volumes.delete(volume)

        assert delete_success is True

    @pytest.mark.parametrize("server,volume",
                             [(Server(id=43), Volume(id=4711)),
                              (BoundServer(mock.MagicMock(), dict(id=43)), BoundVolume(mock.MagicMock(), dict(id=4711)))])
    def test_attach(self, hetzner_client, server, volume):
        action = hetzner_client.volumes.attach(volume, server)
        assert action.id == 13
        assert action.progress == 0
        assert action.command == "attach_volume"

    @pytest.mark.parametrize("volume", [Volume(id=4711), BoundVolume(mock.MagicMock(), dict(id=4711))])
    def test_detach(self, hetzner_client, volume):
        action = hetzner_client.volumes.detach(volume)
        assert action.id == 13
        assert action.progress == 0
        assert action.command == "detach_volume"

    @pytest.mark.parametrize("volume", [Volume(id=4711), BoundVolume(mock.MagicMock(), dict(id=4711))])
    def test_resize(self, hetzner_client, volume):
        action = hetzner_client.volumes.resize(volume, 50)
        assert action.id == 13
        assert action.progress == 0
        assert action.command == "resize_volume"
