# pylint: disable=protected-access

from __future__ import annotations

from unittest import mock

import pytest
from dateutil.parser import isoparse

from hcloud import Client
from hcloud.locations import Location
from hcloud.storage_box_types import StorageBoxType
from hcloud.storage_boxes import (
    BoundStorageBox,
    StorageBox,
    StorageBoxesClient,
)
from hcloud.storage_boxes.domain import StorageBoxAccessSettings

from ..conftest import BoundModelTestCase, assert_bound_action1


def assert_bound_model(
    o: BoundStorageBox,
    resource_client: StorageBoxesClient,
):
    assert isinstance(o, BoundStorageBox)
    assert o._client is resource_client
    assert o.id == 42
    assert o.name == "storage-box1"


class TestBoundStorageBox(BoundModelTestCase):
    methods = []

    @pytest.fixture()
    def resource_client(self, client: Client) -> StorageBoxesClient:
        return client.storage_boxes

    @pytest.fixture()
    def bound_model(
        self, resource_client: StorageBoxesClient, storage_box1
    ) -> BoundStorageBox:
        return BoundStorageBox(resource_client, data=storage_box1)

    def test_init(self, bound_model, resource_client):
        o = bound_model

        assert_bound_model(o, resource_client)
        # TODO: test all properties


class TestStorageBoxClient:
    @pytest.fixture()
    def resource_client(self, client: Client) -> StorageBoxesClient:
        return client.storage_boxes

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box1,
    ):
        request_mock.return_value = {"storage_box": storage_box1}

        result = resource_client.get_by_id(42)

        request_mock.assert_called_with(
            method="GET",
            url="/storage_boxes/42",
        )

        assert_bound_model(result, resource_client)
        assert result.storage_box_type.id == 42
        assert result.storage_box_type.name == "bx11"
        assert result.location.id == 1
        assert result.location.name == "fsn1"
        assert result.system == "FSN1-BX355"
        assert result.server == "u1337.your-storagebox.de"
        assert result.username == "u12345"
        assert result.labels == {"key": "value"}
        assert result.protection == {"delete": False}
        assert result.snapshot_plan.max_snapshots == 20
        assert result.snapshot_plan.minute == 0
        assert result.snapshot_plan.hour == 7
        assert result.snapshot_plan.day_of_week == 7
        assert result.snapshot_plan.day_of_month is None
        assert result.access_settings.reachable_externally is False
        assert result.access_settings.samba_enabled is False
        assert result.access_settings.ssh_enabled is False
        assert result.access_settings.webdav_enabled is False
        assert result.access_settings.zfs_enabled is False
        assert result.stats.size == 2342236717056
        assert result.stats.size_data == 2102612983808
        assert result.stats.size_snapshots == 239623733248
        assert result.status == "active"
        assert result.created == isoparse("2025-01-30T23:55:00Z")

    @pytest.mark.parametrize(
        "params",
        [
            {"name": "storage-box1", "page": 1, "per_page": 10},
            {},
        ],
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box1,
        storage_box2,
        params,
    ):
        request_mock.return_value = {"storage_boxes": [storage_box1, storage_box2]}

        result = resource_client.get_list(**params)

        request_mock.assert_called_with(
            url="/storage_boxes",
            method="GET",
            params=params,
        )

        assert result.meta is not None
        assert len(result.storage_boxes) == 2

        result1 = result.storage_boxes[0]
        result2 = result.storage_boxes[1]

        assert result1._client is resource_client
        assert result1.id == 42
        assert result1.name == "storage-box1"

        assert result2._client is resource_client
        assert result2.id == 43
        assert result2.name == "storage-box2"

    @pytest.mark.parametrize(
        "params",
        [
            {"name": "bx11"},
            {},
        ],
    )
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box1,
        storage_box2,
        params,
    ):
        request_mock.return_value = {"storage_boxes": [storage_box1, storage_box2]}

        result = resource_client.get_all(**params)

        request_mock.assert_called_with(
            url="/storage_boxes",
            method="GET",
            params={**params, "page": 1, "per_page": 50},
        )

        assert len(result) == 2

        result1 = result[0]
        result2 = result[1]

        assert result1._client is resource_client
        assert result1.id == 42
        assert result1.name == "storage-box1"

        assert result2._client is resource_client
        assert result2.id == 43
        assert result2.name == "storage-box2"

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box1,
    ):
        request_mock.return_value = {"storage_boxes": [storage_box1]}

        result = resource_client.get_by_name("bx11")

        params = {"name": "bx11"}

        request_mock.assert_called_with(
            method="GET",
            url="/storage_boxes",
            params=params,
        )

        assert_bound_model(result, resource_client)

    def test_create(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box1,
        action1_running,
    ):
        request_mock.return_value = {
            "storage_box": storage_box1,
            "action": action1_running,
        }

        result = resource_client.create(
            name="storage-box1",
            password="secret-password",
            location=Location(name="fsn1"),
            storage_box_type=StorageBoxType(name="bx11"),
            ssh_keys=[],
            access_settings=StorageBoxAccessSettings(
                reachable_externally=True,
                ssh_enabled=True,
                samba_enabled=False,
            ),
            labels={"key": "value"},
        )

        request_mock.assert_called_with(
            method="POST",
            url="/storage_boxes",
            json={
                "name": "storage-box1",
                "password": "secret-password",
                "location": "fsn1",
                "storage_box_type": "bx11",
                "ssh_keys": [],
                "access_settings": {
                    "reachable_externally": True,
                    "samba_enabled": False,
                    "ssh_enabled": True,
                },
                "labels": {"key": "value"},
            },
        )

        assert_bound_model(result.storage_box, resource_client)

    def test_update(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box1,
    ):
        request_mock.return_value = {
            "storage_box": storage_box1,
        }

        result = resource_client.update(
            StorageBox(id=42),
            name="name",
            labels={"key": "value"},
        )

        request_mock.assert_called_with(
            method="PUT",
            url="/storage_boxes/42",
            json={
                "name": "name",
                "labels": {"key": "value"},
            },
        )

        assert_bound_model(result, resource_client)

    def test_delete(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        action1_running,
    ):
        request_mock.return_value = {
            "action": action1_running,
        }

        result = resource_client.delete(StorageBox(id=42))

        request_mock.assert_called_with(
            method="DELETE",
            url="/storage_boxes/42",
        )

        assert_bound_action1(result.action, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "params",
        [
            {"path": "dir1/path"},
            {},
        ],
    )
    def test_get_folders(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        params,
    ):
        request_mock.return_value = {
            "folders": ["dir1", "dir2"],
        }

        result = resource_client.get_folders(StorageBox(id=42), **params)

        request_mock.assert_called_with(
            method="GET", url="/storage_boxes/42/folders", params=params
        )

        assert result.folders == ["dir1", "dir2"]

    def test_change_protection(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.change_protection(StorageBox(id=42), delete=True)

        request_mock.assert_called_with(
            method="POST",
            url="/storage_boxes/42/actions/change_protection",
            json={"delete": True},
        )

        assert_bound_action1(action, resource_client._parent.actions)

    def test_change_type(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.change_type(
            StorageBox(id=42),
            StorageBoxType(name="bx21"),
        )

        request_mock.assert_called_with(
            method="POST",
            url="/storage_boxes/42/actions/change_type",
            json={"storage_box_type": "bx21"},
        )

        assert_bound_action1(action, resource_client._parent.actions)
