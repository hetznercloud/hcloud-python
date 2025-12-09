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
    BoundStorageBoxSnapshot,
    BoundStorageBoxSubaccount,
    StorageBox,
    StorageBoxAccessSettings,
    StorageBoxesClient,
    StorageBoxSnapshot,
    StorageBoxSnapshotPlan,
    StorageBoxSubaccount,
    StorageBoxSubaccountAccessSettings,
)

from ..conftest import BoundModelTestCase, assert_bound_action1


def assert_bound_storage_box(
    o: BoundStorageBox,
    resource_client: StorageBoxesClient,
):
    assert isinstance(o, BoundStorageBox)
    assert o._client is resource_client
    assert o.id == 42
    assert o.name == "storage-box1"


def assert_bound_storage_box_snapshot(
    o: BoundStorageBoxSnapshot,
    resource_client: StorageBoxesClient,
):
    assert isinstance(o, BoundStorageBoxSnapshot)
    assert o._client is resource_client
    assert o.id == 34
    assert o.name == "storage-box-snapshot1"


def assert_bound_storage_box_subaccount(
    o: BoundStorageBoxSubaccount,
    resource_client: StorageBoxesClient,
):
    assert isinstance(o, BoundStorageBoxSubaccount)
    assert o._client is resource_client
    assert o.id == 45
    assert o.username == "u42-sub1"


class TestBoundStorageBox(BoundModelTestCase):
    methods = [
        BoundStorageBox.update,
        BoundStorageBox.delete,
        BoundStorageBox.get_folders,
        BoundStorageBox.change_protection,
        BoundStorageBox.change_type,
        BoundStorageBox.disable_snapshot_plan,
        BoundStorageBox.enable_snapshot_plan,
        BoundStorageBox.reset_password,
        BoundStorageBox.rollback_snapshot,
        BoundStorageBox.update_access_settings,
        # Snapshots
        BoundStorageBox.create_snapshot,
        BoundStorageBox.get_snapshot_all,
        BoundStorageBox.get_snapshot_by_id,
        BoundStorageBox.get_snapshot_by_name,
        BoundStorageBox.get_snapshot_list,
        # Subaccounts
        BoundStorageBox.create_subaccount,
        BoundStorageBox.get_subaccount_all,
        BoundStorageBox.get_subaccount_by_id,
        BoundStorageBox.get_subaccount_by_username,
        BoundStorageBox.get_subaccount_list,
    ]

    @pytest.fixture()
    def resource_client(self, client: Client) -> StorageBoxesClient:
        return client.storage_boxes

    @pytest.fixture()
    def bound_model(
        self,
        resource_client: StorageBoxesClient,
        storage_box1,
    ) -> BoundStorageBox:
        return BoundStorageBox(resource_client, data=storage_box1)

    def test_init(self, bound_model: BoundStorageBox, resource_client):
        o = bound_model

        assert_bound_storage_box(o, resource_client)

        assert o.storage_box_type.id == 42
        assert o.storage_box_type.name == "bx11"
        assert o.location.id == 1
        assert o.location.name == "fsn1"
        assert o.system == "FSN1-BX355"
        assert o.server == "u1337.your-storagebox.de"
        assert o.username == "u12345"
        assert o.labels == {"key": "value"}
        assert o.protection == {"delete": False}
        assert o.snapshot_plan.max_snapshots == 20
        assert o.snapshot_plan.minute == 0
        assert o.snapshot_plan.hour == 7
        assert o.snapshot_plan.day_of_week == 7
        assert o.snapshot_plan.day_of_month is None
        assert o.access_settings.reachable_externally is False
        assert o.access_settings.samba_enabled is False
        assert o.access_settings.ssh_enabled is False
        assert o.access_settings.webdav_enabled is False
        assert o.access_settings.zfs_enabled is False
        assert o.stats.size == 2342236717056
        assert o.stats.size_data == 2102612983808
        assert o.stats.size_snapshots == 239623733248
        assert o.status == "active"
        assert o.created == isoparse("2025-01-30T23:55:00Z")


class TestBoundStorageBoxSnapshot(BoundModelTestCase):
    methods = [
        (BoundStorageBoxSnapshot.update, {"client_method": "update_snapshot"}),
        (BoundStorageBoxSnapshot.delete, {"client_method": "delete_snapshot"}),
    ]

    @pytest.fixture()
    def resource_client(self, client: Client) -> StorageBoxesClient:
        return client.storage_boxes

    @pytest.fixture()
    def bound_model(
        self,
        resource_client: StorageBoxesClient,
        storage_box_snapshot1,
    ) -> BoundStorageBoxSnapshot:
        return BoundStorageBoxSnapshot(resource_client, data=storage_box_snapshot1)

    def test_init(self, bound_model: BoundStorageBoxSnapshot, resource_client):
        o = bound_model

        assert_bound_storage_box_snapshot(o, resource_client)

        assert isinstance(o.storage_box, BoundStorageBox)
        assert o.storage_box.id == 42

        assert o.description == ""
        assert o.is_automatic is False
        assert o.labels == {"key": "value"}
        assert o.stats.size == 394957594
        assert o.stats.size_filesystem == 3949572745
        assert o.created == isoparse("2025-11-10T19:16:57Z")

    def test_reload(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box_snapshot1,
    ):
        o = BoundStorageBoxSnapshot(resource_client, data={"id": 34, "storage_box": 42})

        request_mock.return_value = {"snapshot": storage_box_snapshot1}

        o.reload()

        request_mock.assert_called_with(
            method="GET",
            url="/storage_boxes/42/snapshots/34",
        )

        assert o.labels is not None


class TestBoundStorageBoxSubaccount(BoundModelTestCase):
    methods = [
        (
            BoundStorageBoxSubaccount.update,
            {"client_method": "update_subaccount"},
        ),
        (
            BoundStorageBoxSubaccount.delete,
            {"client_method": "delete_subaccount"},
        ),
        (
            BoundStorageBoxSubaccount.change_home_directory,
            {"client_method": "change_subaccount_home_directory"},
        ),
        (
            BoundStorageBoxSubaccount.reset_password,
            {"client_method": "reset_subaccount_password"},
        ),
        (
            BoundStorageBoxSubaccount.update_access_settings,
            {"client_method": "update_subaccount_access_settings"},
        ),
    ]

    @pytest.fixture()
    def resource_client(self, client: Client) -> StorageBoxesClient:
        return client.storage_boxes

    @pytest.fixture()
    def bound_model(
        self,
        resource_client: StorageBoxesClient,
        storage_box_subaccount1,
    ) -> BoundStorageBoxSubaccount:
        return BoundStorageBoxSubaccount(resource_client, data=storage_box_subaccount1)

    def test_init(self, bound_model: BoundStorageBoxSubaccount, resource_client):
        o = bound_model

        assert_bound_storage_box_subaccount(o, resource_client)

        assert isinstance(o.storage_box, BoundStorageBox)
        assert o.storage_box.id == 42

        assert o.username == "u42-sub1"
        assert o.description == "Required by foo"
        assert o.server == "u42-sub1.your-storagebox.de"
        assert o.home_directory == "tmp/"
        assert o.access_settings.reachable_externally is True
        assert o.access_settings.samba_enabled is False
        assert o.access_settings.ssh_enabled is True
        assert o.access_settings.webdav_enabled is False
        assert o.access_settings.readonly is False
        assert o.labels == {"key": "value"}
        assert o.created == isoparse("2025-11-10T19:18:57Z")

    def test_reload(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box_subaccount1,
    ):
        o = BoundStorageBoxSubaccount(
            resource_client, data={"id": 45, "storage_box": 42}
        )

        request_mock.return_value = {"subaccount": storage_box_subaccount1}

        o.reload()

        request_mock.assert_called_with(
            method="GET",
            url="/storage_boxes/42/subaccounts/45",
        )

        assert o.labels is not None


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

        assert_bound_storage_box(result, resource_client)

    @pytest.mark.parametrize(
        "params",
        [
            {"name": "storage-box1"},
            {"label_selector": "key=value"},
            {"page": 1, "per_page": 10},
            {"sort": ["id:asc"]},
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
            {"name": "storage-box1"},
            {"label_selector": "key=value"},
            {"sort": ["id:asc"]},
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

        assert_bound_storage_box(result, resource_client)

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

        assert_bound_storage_box(result.storage_box, resource_client)

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

        assert_bound_storage_box(result, resource_client)

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

    def test_reset_password(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.reset_password(
            StorageBox(id=42),
            password="password",
        )

        request_mock.assert_called_with(
            method="POST",
            url="/storage_boxes/42/actions/reset_password",
            json={"password": "password"},
        )

        assert_bound_action1(action, resource_client._parent.actions)

    def test_update_access_settings(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.update_access_settings(
            StorageBox(id=42),
            StorageBoxAccessSettings(
                reachable_externally=True,
                ssh_enabled=True,
                webdav_enabled=False,
            ),
        )

        request_mock.assert_called_with(
            method="POST",
            url="/storage_boxes/42/actions/update_access_settings",
            json={
                "reachable_externally": True,
                "ssh_enabled": True,
                "webdav_enabled": False,
            },
        )

        assert_bound_action1(action, resource_client._parent.actions)

    def test_rollback_snapshot(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.rollback_snapshot(
            StorageBox(id=42),
            StorageBoxSnapshot(id=32),
        )

        request_mock.assert_called_with(
            method="POST",
            url="/storage_boxes/42/actions/rollback_snapshot",
            json={"snapshot": 32},
        )

        assert_bound_action1(action, resource_client._parent.actions)

    def test_disable_snapshot_plan(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.disable_snapshot_plan(
            StorageBox(id=42),
        )

        request_mock.assert_called_with(
            method="POST",
            url="/storage_boxes/42/actions/disable_snapshot_plan",
        )

        assert_bound_action1(action, resource_client._parent.actions)

    def test_enable_snapshot_plan(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.enable_snapshot_plan(
            StorageBox(id=42),
            StorageBoxSnapshotPlan(
                max_snapshots=10,
                hour=3,
                minute=30,
                day_of_week=None,
            ),
        )

        request_mock.assert_called_with(
            method="POST",
            url="/storage_boxes/42/actions/enable_snapshot_plan",
            json={
                "max_snapshots": 10,
                "hour": 3,
                "minute": 30,
                "day_of_week": None,
                "day_of_month": None,
            },
        )

        assert_bound_action1(action, resource_client._parent.actions)

    # Snapshots
    ###########################################################################

    def test_get_snapshot_by_id(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box_snapshot1,
    ):
        request_mock.return_value = {"snapshot": storage_box_snapshot1}

        result = resource_client.get_snapshot_by_id(StorageBox(42), 34)

        request_mock.assert_called_with(
            method="GET",
            url="/storage_boxes/42/snapshots/34",
        )

        assert_bound_storage_box_snapshot(result, resource_client)

    @pytest.mark.parametrize(
        "params",
        [
            {"name": "storage-box-snapshot1"},
            {"is_automatic": True},
            {"label_selector": "key=value"},
            # {"page": 1, "per_page": 10}  # No pagination
            {"sort": ["id:asc"]},
            {},
        ],
    )
    def test_get_snapshot_list(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box_snapshot1,
        storage_box_snapshot2,
        params,
    ):
        request_mock.return_value = {
            "snapshots": [storage_box_snapshot1, storage_box_snapshot2]
        }

        result = resource_client.get_snapshot_list(StorageBox(42), **params)

        request_mock.assert_called_with(
            url="/storage_boxes/42/snapshots",
            method="GET",
            params=params,
        )

        assert result.meta is not None
        assert len(result.snapshots) == 2

        result1 = result.snapshots[0]
        result2 = result.snapshots[1]

        assert result1._client is resource_client
        assert result1.id == 34
        assert result1.name == "storage-box-snapshot1"
        assert isinstance(result1.storage_box, BoundStorageBox)
        assert result1.storage_box.id == 42

        assert result2._client is resource_client
        assert result2.id == 35
        assert result2.name == "storage-box-snapshot2"
        assert isinstance(result2.storage_box, BoundStorageBox)
        assert result2.storage_box.id == 42

    @pytest.mark.parametrize(
        "params",
        [
            {"name": "storage-box-snapshot1"},
            {"is_automatic": True},
            {"label_selector": "key=value"},
            {"sort": ["id:asc"]},
            {},
        ],
    )
    def test_get_snapshot_all(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box_snapshot1,
        storage_box_snapshot2,
        params,
    ):
        request_mock.return_value = {
            "snapshots": [storage_box_snapshot1, storage_box_snapshot2]
        }

        result = resource_client.get_snapshot_all(StorageBox(42), **params)

        request_mock.assert_called_with(
            url="/storage_boxes/42/snapshots",
            method="GET",
            params=params,
        )

        assert len(result) == 2

        result1 = result[0]
        result2 = result[1]

        assert result1._client is resource_client
        assert result1.id == 34
        assert result1.name == "storage-box-snapshot1"
        assert isinstance(result1.storage_box, BoundStorageBox)
        assert result1.storage_box.id == 42

        assert result2._client is resource_client
        assert result2.id == 35
        assert result2.name == "storage-box-snapshot2"
        assert isinstance(result2.storage_box, BoundStorageBox)
        assert result2.storage_box.id == 42

    def test_get_snapshot_by_name(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box_snapshot1,
    ):
        request_mock.return_value = {"snapshots": [storage_box_snapshot1]}

        result = resource_client.get_snapshot_by_name(
            StorageBox(42), "storage-box-snapshot1"
        )

        request_mock.assert_called_with(
            method="GET",
            url="/storage_boxes/42/snapshots",
            params={"name": "storage-box-snapshot1"},
        )

        assert_bound_storage_box_snapshot(result, resource_client)

    def test_create_snapshot(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box_snapshot1: dict,
        action1_running,
    ):
        request_mock.return_value = {
            "snapshot": {
                # Only a partial object is returned
                key: storage_box_snapshot1[key]
                for key in ["id", "storage_box"]
            },
            "action": action1_running,
        }

        result = resource_client.create_snapshot(
            StorageBox(42),
            description="something",
            labels={"key": "value"},
        )

        request_mock.assert_called_with(
            method="POST",
            url="/storage_boxes/42/snapshots",
            json={
                "description": "something",
                "labels": {"key": "value"},
            },
        )

        assert isinstance(result.snapshot, BoundStorageBoxSnapshot)
        assert result.snapshot._client is resource_client
        assert result.snapshot.id == 34

        assert_bound_action1(result.action, resource_client._parent.actions)

    def test_update_snapshot(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box_snapshot1,
    ):
        request_mock.return_value = {
            "snapshot": storage_box_snapshot1,
        }

        result = resource_client.update_snapshot(
            StorageBoxSnapshot(id=34, storage_box=StorageBox(42)),
            description="something",
            labels={"key": "value"},
        )

        request_mock.assert_called_with(
            method="PUT",
            url="/storage_boxes/42/snapshots/34",
            json={
                "description": "something",
                "labels": {"key": "value"},
            },
        )

        assert_bound_storage_box_snapshot(result, resource_client)

    def test_delete_snapshot(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        action1_running,
    ):
        request_mock.return_value = {
            "action": action1_running,
        }

        result = resource_client.delete_snapshot(
            StorageBoxSnapshot(id=34, storage_box=StorageBox(42))
        )

        request_mock.assert_called_with(
            method="DELETE",
            url="/storage_boxes/42/snapshots/34",
        )

        assert_bound_action1(result.action, resource_client._parent.actions)

    # Subaccounts
    ###########################################################################

    def test_get_subaccount_by_id(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box_subaccount1,
    ):
        request_mock.return_value = {"subaccount": storage_box_subaccount1}

        result = resource_client.get_subaccount_by_id(StorageBox(42), 45)

        request_mock.assert_called_with(
            method="GET",
            url="/storage_boxes/42/subaccounts/45",
        )

        assert_bound_storage_box_subaccount(result, resource_client)

    @pytest.mark.parametrize(
        "params",
        [
            {"username": "u42-sub1"},
            {"label_selector": "key=value"},
            # {"page": 1, "per_page": 10}  # No pagination
            {"sort": ["id:asc"]},
            {},
        ],
    )
    def test_get_subaccount_list(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box_subaccount1,
        storage_box_subaccount2,
        params,
    ):
        request_mock.return_value = {
            "subaccounts": [storage_box_subaccount1, storage_box_subaccount2]
        }

        result = resource_client.get_subaccount_list(StorageBox(42), **params)

        request_mock.assert_called_with(
            url="/storage_boxes/42/subaccounts",
            method="GET",
            params=params,
        )

        assert result.meta is not None
        assert len(result.subaccounts) == 2

        result1 = result.subaccounts[0]
        result2 = result.subaccounts[1]

        assert result1._client is resource_client
        assert result1.id == 45
        assert result1.username == "u42-sub1"
        assert isinstance(result1.storage_box, BoundStorageBox)
        assert result1.storage_box.id == 42

        assert result2._client is resource_client
        assert result2.id == 46
        assert result2.username == "u42-sub2"
        assert isinstance(result2.storage_box, BoundStorageBox)
        assert result2.storage_box.id == 42

    @pytest.mark.parametrize(
        "params",
        [
            {"username": "u42-sub1"},
            {"label_selector": "key=value"},
            {"sort": ["id:asc"]},
            {},
        ],
    )
    def test_get_subaccount_all(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box_subaccount1,
        storage_box_subaccount2,
        params,
    ):
        request_mock.return_value = {
            "subaccounts": [storage_box_subaccount1, storage_box_subaccount2]
        }

        result = resource_client.get_subaccount_all(StorageBox(42), **params)

        request_mock.assert_called_with(
            url="/storage_boxes/42/subaccounts",
            method="GET",
            params=params,
        )

        assert len(result) == 2

        result1 = result[0]
        result2 = result[1]

        assert result1._client is resource_client
        assert result1.id == 45
        assert result1.username == "u42-sub1"
        assert isinstance(result1.storage_box, BoundStorageBox)
        assert result1.storage_box.id == 42

        assert result2._client is resource_client
        assert result2.id == 46
        assert result2.username == "u42-sub2"
        assert isinstance(result2.storage_box, BoundStorageBox)
        assert result2.storage_box.id == 42

    def test_get_subaccount_by_username(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box_subaccount1,
    ):
        request_mock.return_value = {"subaccounts": [storage_box_subaccount1]}

        result = resource_client.get_subaccount_by_username(StorageBox(42), "u42-sub1")

        request_mock.assert_called_with(
            method="GET",
            url="/storage_boxes/42/subaccounts",
            params={"username": "u42-sub1"},
        )

        assert_bound_storage_box_subaccount(result, resource_client)

    def test_create_subaccount(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box_subaccount1: dict,
        action1_running,
    ):
        request_mock.return_value = {
            "subaccount": {
                # Only a partial object is returned
                key: storage_box_subaccount1[key]
                for key in ["id", "storage_box"]
            },
            "action": action1_running,
        }

        result = resource_client.create_subaccount(
            StorageBox(42),
            home_directory="tmp",
            password="secret",
            access_settings=StorageBoxSubaccountAccessSettings(
                reachable_externally=True,
                ssh_enabled=True,
                readonly=False,
            ),
            description="something",
            labels={"key": "value"},
        )

        request_mock.assert_called_with(
            method="POST",
            url="/storage_boxes/42/subaccounts",
            json={
                "home_directory": "tmp",
                "password": "secret",
                "access_settings": {
                    "reachable_externally": True,
                    "ssh_enabled": True,
                    "readonly": False,
                },
                "description": "something",
                "labels": {"key": "value"},
            },
        )

        assert isinstance(result.subaccount, BoundStorageBoxSubaccount)
        assert result.subaccount._client is resource_client
        assert result.subaccount.id == 45

        assert_bound_action1(result.action, resource_client._parent.actions)

    def test_update_subaccount(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        storage_box_subaccount1,
    ):
        request_mock.return_value = {
            "subaccount": storage_box_subaccount1,
        }

        result = resource_client.update_subaccount(
            StorageBoxSubaccount(id=45, storage_box=StorageBox(42)),
            description="something",
            labels={"key": "value"},
        )

        request_mock.assert_called_with(
            method="PUT",
            url="/storage_boxes/42/subaccounts/45",
            json={
                "description": "something",
                "labels": {"key": "value"},
            },
        )

        assert_bound_storage_box_subaccount(result, resource_client)

    def test_delete_subaccount(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        action1_running,
    ):
        request_mock.return_value = {
            "action": action1_running,
        }

        result = resource_client.delete_subaccount(
            StorageBoxSubaccount(id=45, storage_box=StorageBox(42)),
        )

        request_mock.assert_called_with(
            method="DELETE",
            url="/storage_boxes/42/subaccounts/45",
        )

        assert_bound_action1(result.action, resource_client._parent.actions)

    def test_change_subaccount_home_directory(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.change_subaccount_home_directory(
            StorageBoxSubaccount(id=45, storage_box=StorageBox(42)),
            home_directory="path",
        )

        request_mock.assert_called_with(
            method="POST",
            url="/storage_boxes/42/subaccounts/45/actions/change_home_directory",
            json={
                "home_directory": "path",
            },
        )

        assert_bound_action1(action, resource_client._parent.actions)

    def test_reset_subaccount_password(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.reset_subaccount_password(
            StorageBoxSubaccount(id=45, storage_box=StorageBox(42)),
            password="password",
        )

        request_mock.assert_called_with(
            method="POST",
            url="/storage_boxes/42/subaccounts/45/actions/reset_subaccount_password",
            json={
                "password": "password",
            },
        )

        assert_bound_action1(action, resource_client._parent.actions)

    def test_update_subaccount_access_settings(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxesClient,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.update_subaccount_access_settings(
            StorageBoxSubaccount(id=45, storage_box=StorageBox(42)),
            access_settings=StorageBoxSubaccountAccessSettings(
                reachable_externally=True,
                ssh_enabled=True,
                samba_enabled=False,
            ),
        )

        request_mock.assert_called_with(
            method="POST",
            url="/storage_boxes/42/subaccounts/45/actions/update_access_settings",
            json={
                "reachable_externally": True,
                "ssh_enabled": True,
                "samba_enabled": False,
            },
        )

        assert_bound_action1(action, resource_client._parent.actions)
