import pytest
import arrow
import mock

from hcloud.servers.client import BoundServer
from hcloud.servers.domain import Server
from hcloud.volumes.client import VolumesClient, BoundVolume
from hcloud.volumes.domain import Volume
from hcloud.locations.client import BoundLocation
from hcloud.locations.domain import Location


class TestBoundVolume(object):

    @pytest.fixture()
    def bound_volume(self, hetzner_client):
        return BoundVolume(client=hetzner_client.volumes, data=dict(id=14))

    def test_bound_volume_init(self, volume_response):
        bound_volume = BoundVolume(
            client=mock.MagicMock(),
            data=volume_response['volume']
        )

        assert bound_volume.id == 1
        assert bound_volume.created == arrow.get("2016-01-30T23:50:11+00:00").datetime
        assert bound_volume.name == "database-storage"
        assert bound_volume.server == 12
        assert bound_volume.size == 42
        assert bound_volume.linux_device == "/dev/disk/by-id/scsi-0HC_Volume_4711"
        assert bound_volume.protection == {"delete": False}
        assert bound_volume.labels == {}
        assert bound_volume.status == "available"

        assert isinstance(bound_volume.location, BoundLocation)
        assert bound_volume.location.id == 1
        assert bound_volume.location.name == "fsn1"
        assert bound_volume.location.description == "Falkenstein DC Park 1"
        assert bound_volume.location.country == "DE"
        assert bound_volume.location.city == "Falkenstein"
        assert bound_volume.location.latitude == 50.47612
        assert bound_volume.location.longitude == 12.370071

    @pytest.mark.parametrize("server",
                             (Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))))
    def test_attach(self, hetzner_client, bound_volume, server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_volume.attach(server)
        hetzner_client.request.assert_called_with(
            url="/volumes/14/actions/attach",
            method="POST",
            json={"server": 1}
        )
        assert action.id == 1
        assert action.progress == 0

    def test_detach(self, hetzner_client, bound_volume, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_volume.detach()
        hetzner_client.request.assert_called_with(
            url="/volumes/14/actions/detach",
            method="POST"
        )
        assert action.id == 1
        assert action.progress == 0


class TestVolumesClient(object):

    @pytest.fixture()
    def volumes_client(self):
        return VolumesClient(client=mock.MagicMock())

    def test_get_by_id(self, volumes_client, volume_response):
        volumes_client._client.request.return_value = volume_response
        bound_volume = volumes_client.get_by_id(1)
        volumes_client._client.request.assert_called_with(url="/volumes/1", method="GET")
        assert bound_volume._client is volumes_client
        assert bound_volume.id == 1
        assert bound_volume.name == "database-storage"

    def test_get_all_no_params(self, volumes_client, two_volumes_response):
        volumes_client._client.request.return_value = two_volumes_response
        bound_volumes = volumes_client.get_all()
        volumes_client._client.request.assert_called_with(url="/volumes", method="GET", params={})

        assert len(bound_volumes) == 2

        bound_volume1 = bound_volumes[0]
        bound_volume2 = bound_volumes[1]

        assert bound_volume1._client is volumes_client
        assert bound_volume1.id == 1
        assert bound_volume1.name == "database-storage"

        assert bound_volume2._client is volumes_client
        assert bound_volume2.id == 2
        assert bound_volume2.name == "vault-storage"

    @pytest.mark.parametrize("params", [{'label_selector': "label1"}])
    def test_get_all_with_params(self, volumes_client, params):
        volumes_client.get_all(**params)
        volumes_client._client.request.assert_called_with(url="/volumes", method="GET", params=params)

    def test_create_with_location(self, volumes_client, volume_create_response):
        volumes_client._client.request.return_value = volume_create_response
        response = volumes_client.create(
            100,
            "database-storage",
            location=Location(name="location"),
            automount=False,
            format="xfs"
        )
        volumes_client._client.request.assert_called_with(
            url="/volumes",
            method="POST",
            json={
                'name': "database-storage",
                'size': 100,
                'location': "location",
                'automount': False,
                'format': "xfs"
            }
        )

        bound_volume = response.volume
        action = response.action
        next_actions = response.next_actions

        assert bound_volume._client is volumes_client
        assert bound_volume.id == 4711
        assert bound_volume.name == "database-storage"

        assert action.id == 13
        assert next_actions[0].command == "start_server"

    @pytest.mark.parametrize("server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))])
    def test_create_with_server(self, volumes_client, server, volume_create_response):
        volumes_client._client.request.return_value = volume_create_response
        volumes_client.create(
            100,
            "database-storage",
            server=server,
            automount=False,
            format="xfs"
        )
        volumes_client._client.request.assert_called_with(
            url="/volumes",
            method="POST",
            json={
                'name': "database-storage",
                'size': 100,
                'server': 1,
                'automount': False,
                'format': "xfs"
            }
        )

    def test_create_negative_size(self, volumes_client):
        with pytest.raises(ValueError) as e:
            volumes_client.create(
                -100,
                "database-storage",
                location=Location(name="location")
            )
        assert str(e.value) == "size must be greater than 0"
        volumes_client._client.request.assert_not_called()

    @pytest.mark.parametrize("location,server", [(None, None), ("location", Server(id=1))])
    def test_create_wrong_location_server_combination(self, volumes_client, location, server):
        with pytest.raises(ValueError) as e:
            volumes_client.create(
                100,
                "database-storage",
                location=location,
                server=server
            )
        assert str(e.value) == "only one of server or location must be provided"
        volumes_client._client.request.assert_not_called()

    @pytest.mark.parametrize("server,volume",
                             [(Server(id=1), Volume(id=12)),
                              (BoundServer(mock.MagicMock(), dict(id=1)), BoundVolume(mock.MagicMock(), dict(id=12)))])
    def test_attach(self, volumes_client, server, volume, generic_action):
        volumes_client._client.request.return_value = generic_action
        action = volumes_client.attach(server, volume)
        volumes_client._client.request.assert_called_with(
            url="/volumes/12/actions/attach",
            method="POST",
            json={"server": 1}
        )
        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize("volume", [Volume(id=12), BoundVolume(mock.MagicMock(), dict(id=12))])
    def test_detach(self, volumes_client, volume, generic_action):
        volumes_client._client.request.return_value = generic_action
        action = volumes_client.detach(volume)
        volumes_client._client.request.assert_called_with(
            url="/volumes/12/actions/detach",
            method="POST"
        )
        assert action.id == 1
        assert action.progress == 0
