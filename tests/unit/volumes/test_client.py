from __future__ import annotations

from unittest import mock

import pytest
from dateutil.parser import isoparse

from hcloud.actions import BoundAction
from hcloud.locations import BoundLocation, Location
from hcloud.servers import BoundServer, Server
from hcloud.volumes import BoundVolume, Volume, VolumesClient


class TestBoundVolume:
    @pytest.fixture()
    def bound_volume(self, hetzner_client):
        return BoundVolume(client=hetzner_client.volumes, data=dict(id=14))

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

    def test_get_actions(self, hetzner_client, bound_volume, response_get_actions):
        hetzner_client.request.return_value = response_get_actions
        actions = bound_volume.get_actions(sort="id")
        hetzner_client.request.assert_called_with(
            url="/volumes/14/actions",
            method="GET",
            params={"page": 1, "per_page": 50, "sort": "id"},
        )

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == hetzner_client.actions
        assert actions[0].id == 13
        assert actions[0].command == "attach_volume"

    def test_update(self, hetzner_client, bound_volume, response_update_volume):
        hetzner_client.request.return_value = response_update_volume
        volume = bound_volume.update(name="new-name")
        hetzner_client.request.assert_called_with(
            url="/volumes/14", method="PUT", json={"name": "new-name"}
        )

        assert volume.id == 4711
        assert volume.name == "new-name"

    def test_delete(self, hetzner_client, bound_volume, generic_action):
        hetzner_client.request.return_value = generic_action
        delete_success = bound_volume.delete()
        hetzner_client.request.assert_called_with(url="/volumes/14", method="DELETE")

        assert delete_success is True

    def test_change_protection(self, hetzner_client, bound_volume, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_volume.change_protection(True)
        hetzner_client.request.assert_called_with(
            url="/volumes/14/actions/change_protection",
            method="POST",
            json={"delete": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", (Server(id=1), BoundServer(mock.MagicMock(), dict(id=1)))
    )
    def test_attach(self, hetzner_client, bound_volume, server, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_volume.attach(server)
        hetzner_client.request.assert_called_with(
            url="/volumes/14/actions/attach", method="POST", json={"server": 1}
        )
        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "server", (Server(id=1), BoundServer(mock.MagicMock(), dict(id=1)))
    )
    def test_attach_with_automount(
        self, hetzner_client, bound_volume, server, generic_action
    ):
        hetzner_client.request.return_value = generic_action
        action = bound_volume.attach(server, False)
        hetzner_client.request.assert_called_with(
            url="/volumes/14/actions/attach",
            method="POST",
            json={"server": 1, "automount": False},
        )
        assert action.id == 1
        assert action.progress == 0

    def test_detach(self, hetzner_client, bound_volume, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_volume.detach()
        hetzner_client.request.assert_called_with(
            url="/volumes/14/actions/detach", method="POST"
        )
        assert action.id == 1
        assert action.progress == 0

    def test_resize(self, hetzner_client, bound_volume, generic_action):
        hetzner_client.request.return_value = generic_action
        action = bound_volume.resize(50)
        hetzner_client.request.assert_called_with(
            url="/volumes/14/actions/resize", method="POST", json={"size": 50}
        )
        assert action.id == 1
        assert action.progress == 0


class TestVolumesClient:
    @pytest.fixture()
    def volumes_client(self):
        return VolumesClient(client=mock.MagicMock())

    def test_get_by_id(self, volumes_client, volume_response):
        volumes_client._client.request.return_value = volume_response
        bound_volume = volumes_client.get_by_id(1)
        volumes_client._client.request.assert_called_with(
            url="/volumes/1", method="GET"
        )
        assert bound_volume._client is volumes_client
        assert bound_volume.id == 1
        assert bound_volume.name == "database-storage"

    @pytest.mark.parametrize(
        "params",
        [{"label_selector": "label1", "page": 1, "per_page": 10}, {"name": ""}, {}],
    )
    def test_get_list(self, volumes_client, two_volumes_response, params):
        volumes_client._client.request.return_value = two_volumes_response
        result = volumes_client.get_list(**params)
        volumes_client._client.request.assert_called_with(
            url="/volumes", method="GET", params=params
        )

        bound_volumes = result.volumes
        assert result.meta is None

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
    def test_get_all(self, volumes_client, two_volumes_response, params):
        volumes_client._client.request.return_value = two_volumes_response
        bound_volumes = volumes_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        volumes_client._client.request.assert_called_with(
            url="/volumes", method="GET", params=params
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

    def test_get_by_name(self, volumes_client, one_volumes_response):
        volumes_client._client.request.return_value = one_volumes_response
        bound_volume = volumes_client.get_by_name("database-storage")

        params = {"name": "database-storage"}

        volumes_client._client.request.assert_called_with(
            url="/volumes", method="GET", params=params
        )

        assert bound_volume._client is volumes_client
        assert bound_volume.id == 1
        assert bound_volume.name == "database-storage"

    def test_create_with_location(self, volumes_client, volume_create_response):
        volumes_client._client.request.return_value = volume_create_response
        response = volumes_client.create(
            100,
            "database-storage",
            location=Location(name="location"),
            automount=False,
            format="xfs",
        )
        volumes_client._client.request.assert_called_with(
            url="/volumes",
            method="POST",
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
    def test_create_with_server(self, volumes_client, server, volume_create_response):
        volumes_client._client.request.return_value = volume_create_response
        volumes_client.create(
            100, "database-storage", server=server, automount=False, format="xfs"
        )
        volumes_client._client.request.assert_called_with(
            url="/volumes",
            method="POST",
            json={
                "name": "database-storage",
                "size": 100,
                "server": 1,
                "automount": False,
                "format": "xfs",
            },
        )

    def test_create_negative_size(self, volumes_client):
        with pytest.raises(ValueError) as e:
            volumes_client.create(
                -100, "database-storage", location=Location(name="location")
            )
        assert str(e.value) == "size must be greater than 0"
        volumes_client._client.request.assert_not_called()

    @pytest.mark.parametrize(
        "location,server", [(None, None), ("location", Server(id=1))]
    )
    def test_create_wrong_location_server_combination(
        self, volumes_client, location, server
    ):
        with pytest.raises(ValueError) as e:
            volumes_client.create(
                100, "database-storage", location=location, server=server
            )
        assert str(e.value) == "only one of server or location must be provided"
        volumes_client._client.request.assert_not_called()

    @pytest.mark.parametrize(
        "volume", [Volume(id=1), BoundVolume(mock.MagicMock(), dict(id=1))]
    )
    def test_get_actions_list(self, volumes_client, volume, response_get_actions):
        volumes_client._client.request.return_value = response_get_actions
        result = volumes_client.get_actions_list(volume, sort="id")
        volumes_client._client.request.assert_called_with(
            url="/volumes/1/actions", method="GET", params={"sort": "id"}
        )

        actions = result.actions
        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)

        assert actions[0]._client == volumes_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "attach_volume"

    @pytest.mark.parametrize(
        "volume", [Volume(id=1), BoundVolume(mock.MagicMock(), dict(id=1))]
    )
    def test_update(self, volumes_client, volume, response_update_volume):
        volumes_client._client.request.return_value = response_update_volume
        volume = volumes_client.update(volume, name="new-name")
        volumes_client._client.request.assert_called_with(
            url="/volumes/1", method="PUT", json={"name": "new-name"}
        )

        assert volume.id == 4711
        assert volume.name == "new-name"

    @pytest.mark.parametrize(
        "volume", [Volume(id=1), BoundVolume(mock.MagicMock(), dict(id=1))]
    )
    def test_change_protection(self, volumes_client, volume, generic_action):
        volumes_client._client.request.return_value = generic_action
        action = volumes_client.change_protection(volume, True)
        volumes_client._client.request.assert_called_with(
            url="/volumes/1/actions/change_protection",
            method="POST",
            json={"delete": True},
        )

        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "volume", [Volume(id=1), BoundVolume(mock.MagicMock(), dict(id=1))]
    )
    def test_delete(self, volumes_client, volume, generic_action):
        volumes_client._client.request.return_value = generic_action
        delete_success = volumes_client.delete(volume)
        volumes_client._client.request.assert_called_with(
            url="/volumes/1", method="DELETE"
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
    def test_attach(self, volumes_client, server, volume, generic_action):
        volumes_client._client.request.return_value = generic_action
        action = volumes_client.attach(volume, server)
        volumes_client._client.request.assert_called_with(
            url="/volumes/12/actions/attach", method="POST", json={"server": 1}
        )
        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "volume", [Volume(id=12), BoundVolume(mock.MagicMock(), dict(id=12))]
    )
    def test_detach(self, volumes_client, volume, generic_action):
        volumes_client._client.request.return_value = generic_action
        action = volumes_client.detach(volume)
        volumes_client._client.request.assert_called_with(
            url="/volumes/12/actions/detach", method="POST"
        )
        assert action.id == 1
        assert action.progress == 0

    @pytest.mark.parametrize(
        "volume", [Volume(id=12), BoundVolume(mock.MagicMock(), dict(id=12))]
    )
    def test_resize(self, volumes_client, volume, generic_action):
        volumes_client._client.request.return_value = generic_action
        action = volumes_client.resize(volume, 50)
        volumes_client._client.request.assert_called_with(
            url="/volumes/12/actions/resize", method="POST", json={"size": 50}
        )
        assert action.id == 1
        assert action.progress == 0

    def test_actions_get_by_id(self, volumes_client, response_get_actions):
        volumes_client._client.request.return_value = {
            "action": response_get_actions["actions"][0]
        }
        action = volumes_client.actions.get_by_id(13)

        volumes_client._client.request.assert_called_with(
            url="/volumes/actions/13", method="GET"
        )

        assert isinstance(action, BoundAction)
        assert action._client == volumes_client._client.actions
        assert action.id == 13
        assert action.command == "attach_volume"

    def test_actions_get_list(self, volumes_client, response_get_actions):
        volumes_client._client.request.return_value = response_get_actions
        result = volumes_client.actions.get_list()

        volumes_client._client.request.assert_called_with(
            url="/volumes/actions",
            method="GET",
            params={},
        )

        actions = result.actions
        assert result.meta is None

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == volumes_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "attach_volume"

    def test_actions_get_all(self, volumes_client, response_get_actions):
        volumes_client._client.request.return_value = response_get_actions
        actions = volumes_client.actions.get_all()

        volumes_client._client.request.assert_called_with(
            url="/volumes/actions",
            method="GET",
            params={"page": 1, "per_page": 50},
        )

        assert len(actions) == 1
        assert isinstance(actions[0], BoundAction)
        assert actions[0]._client == volumes_client._client.actions
        assert actions[0].id == 13
        assert actions[0].command == "attach_volume"
