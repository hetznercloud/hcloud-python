from __future__ import annotations

from unittest import mock

import pytest
from dateutil.parser import isoparse

from hcloud import Client
from hcloud.locations import BoundLocation, Location
from hcloud.servers import BoundServer, Server
from hcloud.volumes import BoundVolume, Volume, VolumesClient

from ..conftest import BoundModelTestCase


class TestBoundVolume(BoundModelTestCase):
    methods = [
        BoundVolume.update,
        BoundVolume.delete,
        BoundVolume.change_protection,
        BoundVolume.attach,
        BoundVolume.detach,
        BoundVolume.resize,
    ]

    @pytest.fixture()
    def resource_client(self, client: Client):
        return client.volumes

    @pytest.fixture()
    def bound_model(self, resource_client):
        return BoundVolume(resource_client, data=dict(id=14))

    def test_bound_volume_init(self, volume_response):
        bound_volume = BoundVolume(
            client=mock.MagicMock(), data=volume_response["volume"]
        )

        assert bound_volume.id == 1
        assert bound_volume.created == isoparse("2016-01-30T23:50:11+00:00")
        assert bound_volume.name == "database-storage"
        assert isinstance(bound_volume.server, BoundServer)
        assert bound_volume.server.id == 12
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


class TestVolumesClient:
    @pytest.fixture()
    def volumes_client(self, client: Client):
        return VolumesClient(client)

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        volumes_client: VolumesClient,
        volume_response,
    ):
        request_mock.return_value = volume_response

        bound_volume = volumes_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/volumes/1",
        )
        assert bound_volume._client is volumes_client
        assert bound_volume.id == 1
        assert bound_volume.name == "database-storage"

    @pytest.mark.parametrize(
        "params",
        [{"label_selector": "label1", "page": 1, "per_page": 10}, {"name": ""}, {}],
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        volumes_client: VolumesClient,
        two_volumes_response,
        params,
    ):
        request_mock.return_value = two_volumes_response

        result = volumes_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/volumes",
            params=params,
        )

        bound_volumes = result.volumes
        assert result.meta is not None

        assert len(bound_volumes) == 2

        bound_volume1 = bound_volumes[0]
        bound_volume2 = bound_volumes[1]

        assert bound_volume1._client is volumes_client
        assert bound_volume1.id == 1
        assert bound_volume1.name == "database-storage"

        assert bound_volume2._client is volumes_client
        assert bound_volume2.id == 2
        assert bound_volume2.name == "vault-storage"

    @pytest.mark.parametrize("params", [{"label_selector": "label1"}])
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        volumes_client: VolumesClient,
        two_volumes_response,
        params,
    ):
        request_mock.return_value = two_volumes_response

        bound_volumes = volumes_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/volumes",
            params=params,
        )

        assert len(bound_volumes) == 2

        bound_volume1 = bound_volumes[0]
        bound_volume2 = bound_volumes[1]

        assert bound_volume1._client is volumes_client
        assert bound_volume1.id == 1
        assert bound_volume1.name == "database-storage"

        assert bound_volume2._client is volumes_client
        assert bound_volume2.id == 2
        assert bound_volume2.name == "vault-storage"

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        volumes_client: VolumesClient,
        one_volumes_response,
    ):
        request_mock.return_value = one_volumes_response

        bound_volume = volumes_client.get_by_name("database-storage")

        params = {"name": "database-storage"}

        request_mock.assert_called_with(
            method="GET",
            url="/volumes",
            params=params,
        )

        assert bound_volume._client is volumes_client
        assert bound_volume.id == 1
        assert bound_volume.name == "database-storage"

    def test_create_with_location(
        self,
        request_mock: mock.MagicMock,
        volumes_client: VolumesClient,
        volume_create_response,
    ):
        request_mock.return_value = volume_create_response

        response = volumes_client.create(
            100,
            "database-storage",
            location=Location(name="location"),
            automount=False,
            format="xfs",
        )

        request_mock.assert_called_with(
            method="POST",
            url="/volumes",
            json={
                "name": "database-storage",
                "size": 100,
                "location": "location",
                "automount": False,
                "format": "xfs",
            },
        )

        bound_volume = response.volume
        action = response.action
        next_actions = response.next_actions

        assert bound_volume._client is volumes_client
        assert bound_volume.id == 4711
        assert bound_volume.name == "database-storage"

        assert action.id == 13
        assert next_actions[0].command == "start_server"

    @pytest.mark.parametrize(
        "server", [Server(id=1), BoundServer(mock.MagicMock(), dict(id=1))]
    )
    def test_create_with_server(
        self,
        request_mock: mock.MagicMock,
        volumes_client: VolumesClient,
        server,
        volume_create_response,
    ):
        request_mock.return_value = volume_create_response

        volumes_client.create(
            size=100,
            name="database-storage",
            server=server,
            automount=False,
            format="xfs",
        )

        request_mock.assert_called_with(
            method="POST",
            url="/volumes",
            json={
                "name": "database-storage",
                "size": 100,
                "server": 1,
                "automount": False,
                "format": "xfs",
            },
        )

    def test_create_negative_size(
        self,
        request_mock: mock.MagicMock,
        volumes_client,
    ):
        with pytest.raises(ValueError) as e:
            volumes_client.create(
                -100, "database-storage", location=Location(name="location")
            )
        assert str(e.value) == "size must be greater than 0"

        request_mock.assert_not_called()

    @pytest.mark.parametrize(
        "location,server", [(None, None), ("location", Server(id=1))]
    )
    def test_create_wrong_location_server_combination(
        self,
        request_mock: mock.MagicMock,
        volumes_client: VolumesClient,
        location,
        server,
    ):
        with pytest.raises(ValueError) as e:
            volumes_client.create(
                100, "database-storage", location=location, server=server
            )
        assert str(e.value) == "only one of server or location must be provided"

        request_mock.assert_not_called()

    @pytest.mark.parametrize(
        "volume", [Volume(id=1), BoundVolume(mock.MagicMock(), dict(id=1))]
    )
    def test_update(
        self,
        request_mock: mock.MagicMock,
        volumes_client: VolumesClient,
        volume,
        response_update_volume,
    ):
        request_mock.return_value = response_update_volume

        volume = volumes_client.update(volume, name="new-name")

        request_mock.assert_called_with(
            method="PUT",
            url="/volumes/1",
            json={"name": "new-name"},
        )

        assert volume.id == 4711
        assert volume.name == "new-name"

    @pytest.mark.parametrize(
        "volume", [Volume(id=1), BoundVolume(mock.MagicMock(), dict(id=1))]
    )
    def test_change_protection(
        self,
        request_mock: mock.MagicMock,
        volumes_client: VolumesClient,
        volume,
        action_response,
    ):
        request_mock.return_value = action_response

        action = volumes_client.change_protection(volume, True)

        request_mock.assert_called_with(
            method="POST",
            url="/volumes/1/actions/change_protection",
            json={"delete": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "volume", [Volume(id=1), BoundVolume(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(
        self,
        request_mock: mock.MagicMock,
        volumes_client: VolumesClient,
        volume,
        action_response,
    ):
        request_mock.return_value = action_response

        delete_success = volumes_client.delete(volume)

        request_mock.assert_called_with(
            method="DELETE",
            url="/volumes/1",
        )

        assert delete_success is True

    @pytest.mark.parametrize(
        "server,volume",
        [
            (Server(id=1), Volume(id=12)),
            (
                BoundServer(mock.MagicMock(), dict(id=1)),
                BoundVolume(mock.MagicMock(), dict(id=12)),
            ),
        ],
    )
    def test_attach(
        self,
        request_mock: mock.MagicMock,
        volumes_client: VolumesClient,
        server,
        volume,
        action_response,
    ):
        request_mock.return_value = action_response

        action = volumes_client.attach(volume, server, True)

        request_mock.assert_called_with(
            method="POST",
            url="/volumes/12/actions/attach",
            json={"server": 1, "automount": True},
        )
        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "volume", [Volume(id=12), BoundVolume(mock.MagicMock(), dict(id=12))]
    )
    def test_detach(
        self,
        request_mock: mock.MagicMock,
        volumes_client: VolumesClient,
        volume,
        action_response,
    ):
        request_mock.return_value = action_response

        action = volumes_client.detach(volume)

        request_mock.assert_called_with(
            method="POST",
            url="/volumes/12/actions/detach",
        )
        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "volume", [Volume(id=12), BoundVolume(mock.MagicMock(), dict(id=12))]
    )
    def test_resize(
        self,
        request_mock: mock.MagicMock,
        volumes_client: VolumesClient,
        volume,
        action_response,
    ):
        request_mock.return_value = action_response

        action = volumes_client.resize(volume, 50)

        request_mock.assert_called_with(
            method="POST",
            url="/volumes/12/actions/resize",
            json={"size": 50},
        )
        assert action.id == 1
        assert action.progress == 0
