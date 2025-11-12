from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

from ..actions import ActionsPageResult, BoundAction, ResourceActionsClient
from ..core import BoundModelBase, Meta, ResourceClientBase
from ..locations import BoundLocation, Location
from ..storage_box_types import BoundStorageBoxType, StorageBoxType
from .domain import (
    CreateStorageBoxResponse,
    CreateStorageBoxSnapshotResponse,
    DeleteStorageBoxResponse,
    DeleteStorageBoxSnapshotResponse,
    StorageBox,
    StorageBoxAccessSettings,
    StorageBoxFoldersResponse,
    StorageBoxSnapshot,
    StorageBoxSnapshotPlan,
    StorageBoxSnapshotStats,
    StorageBoxStats,
)

if TYPE_CHECKING:
    from .._client import Client


class BoundStorageBox(BoundModelBase, StorageBox):
    _client: StorageBoxesClient

    model = StorageBox

    def __init__(
        self,
        client: StorageBoxesClient,
        data: dict[str, Any],
        complete: bool = True,
    ):
        raw = data.get("storage_box_type")
        if raw is not None:
            data["storage_box_type"] = BoundStorageBoxType(
                client._parent.storage_box_types, raw
            )

        raw = data.get("location")
        if raw is not None:
            data["location"] = BoundLocation(client._parent.locations, raw)

        raw = data.get("snapshot_plan")
        if raw is not None:
            data["snapshot_plan"] = StorageBoxSnapshotPlan.from_dict(raw)

        raw = data.get("access_settings")
        if raw is not None:
            data["access_settings"] = StorageBoxAccessSettings.from_dict(raw)

        raw = data.get("stats")
        if raw is not None:
            data["stats"] = StorageBoxStats.from_dict(raw)

        super().__init__(client, data, complete)

    def get_actions_list(
        self,
        *,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """
        Returns all Actions for the Storage Box for a specific page.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-list-actions

        :param status: Filter the actions by status. The response will only contain actions matching the specified statuses.
        :param sort: Sort resources by field and direction.
        :param page: Page number to return.
        :param per_page: Maximum number of entries returned per page.
        """
        return self._client.get_actions_list(
            self,
            status=status,
            sort=sort,
            page=page,
            per_page=per_page,
        )

    def get_actions(
        self,
        *,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """
        Returns all Actions for the Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-list-actions

        :param status: Filter the actions by status. The response will only contain actions matching the specified statuses.
        :param sort: Sort resources by field and direction.
        """
        return self._client.get_actions(
            self,
            status=status,
            sort=sort,
        )

    # TODO: implement bound methods


class BoundStorageBoxSnapshot(BoundModelBase, StorageBoxSnapshot):
    _client: StorageBoxesClient

    model = StorageBoxSnapshot

    def __init__(
        self,
        client: StorageBoxesClient,
        data: dict[str, Any],
        complete: bool = True,
    ):
        raw = data.get("storage_box")
        if raw is not None:
            data["storage_box"] = BoundStorageBox(
                client, data={"id": raw}, complete=False
            )

        raw = data.get("stats")
        if raw is not None:
            data["stats"] = StorageBoxSnapshotStats.from_dict(raw)

        super().__init__(client, data, complete)

    # TODO: implement bound methods


class StorageBoxesPageResult(NamedTuple):
    storage_boxes: list[BoundStorageBox]
    meta: Meta


class StorageBoxSnapshotsPageResult(NamedTuple):
    snapshots: list[BoundStorageBoxSnapshot]
    meta: Meta


class StorageBoxesClient(ResourceClientBase):
    """
    A client for the Storage Boxes API.

    See https://docs.hetzner.cloud/reference/hetzner#storage-boxes.
    """

    _base_url = "/storage_boxes"

    actions: ResourceActionsClient
    """Storage Boxes scoped actions client

    :type: :class:`ResourceActionsClient <hcloud.actions.client.ResourceActionsClient>`
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self._client = client._client_hetzner
        self.actions = ResourceActionsClient(self, self._base_url)

    def get_by_id(self, id: int) -> BoundStorageBox:
        """
        Returns a specific Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-get-a-storage-box

        :param id: ID of the Storage Box.
        """
        response = self._client.request(
            method="GET",
            url=f"{self._base_url}/{id}",
        )
        return BoundStorageBox(self, response["storage_box"])

    def get_by_name(self, name: str) -> BoundStorageBox | None:
        """
        Returns a specific Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-list-storage-boxes

        :param name: Name of the Storage Box.
        """
        return self._get_first_by(self.get_list, name=name)

    def get_list(
        self,
        name: str | None = None,
        label_selector: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> StorageBoxesPageResult:
        """
        Returns a list of Storage Boxes for a specific page.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-list-storage-boxes

        :param name: Name of the Storage Box.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param page: Page number to return.
        :param per_page: Maximum number of entries returned per page.
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if label_selector is not None:
            params["label_selector"] = label_selector
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(
            method="GET",
            url=f"{self._base_url}",
            params=params,
        )
        return StorageBoxesPageResult(
            storage_boxes=[BoundStorageBox(self, o) for o in response["storage_boxes"]],
            meta=Meta.parse_meta(response),
        )

    def get_all(
        self,
        name: str | None = None,
        label_selector: str | None = None,
    ) -> list[BoundStorageBox]:
        """
        Returns all Storage Boxes.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-list-storage-boxes

        :param name: Name of the Storage Box.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        """
        return self._iter_pages(
            self.get_list,
            name=name,
            label_selector=label_selector,
        )

    def create(
        self,
        *,
        name: str,
        password: str,
        location: BoundLocation | Location,
        storage_box_type: BoundStorageBoxType | StorageBoxType,
        ssh_keys: list[str] | None = None,
        access_settings: StorageBoxAccessSettings | None = None,
        labels: dict[str, str] | None = None,
    ) -> CreateStorageBoxResponse:
        """
        Creates a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-create-a-storage-box

        :param name: Name of the Storage Box.
        :param password: Password of the Storage Box.
        :param location: Location of the Storage Box.
        :param storage_box_type: Type of the Storage Box.
        :param ssh_keys: SSH public keys of the Storage Box.
        :param access_settings: Access settings of the Storage Box.
        :param labels: User-defined labels (key/value pairs) for the Storage Box.
        """
        data: dict[str, Any] = {
            "name": name,
            "password": password,
            "location": location.id_or_name,
            "storage_box_type": storage_box_type.id_or_name,
        }
        if ssh_keys is not None:
            data["ssh_keys"] = ssh_keys
        if access_settings is not None:
            data["access_settings"] = access_settings.to_payload()
        if labels is not None:
            data["labels"] = labels

        response = self._client.request(
            method="POST",
            url="/storage_boxes",
            json=data,
        )

        return CreateStorageBoxResponse(
            storage_box=BoundStorageBox(self, response["storage_box"]),
            action=BoundAction(self._parent.actions, response["action"]),
        )

    def update(
        self,
        storage_box: BoundStorageBox | StorageBox,
        *,
        name: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundStorageBox:
        """
        Updates a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-update-a-storage-box

        :param storage_box: Storage Box to update.
        :param name: Name of the Storage Box.
        :param labels: User-defined labels (key/value pairs) for the Storage Box.
        """
        data: dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if labels is not None:
            data["labels"] = labels

        response = self._client.request(
            method="PUT",
            url=f"{self._base_url}/{storage_box.id}",
            json=data,
        )

        return BoundStorageBox(self, response["storage_box"])

    def delete(
        self,
        storage_box: BoundStorageBox | StorageBox,
    ) -> DeleteStorageBoxResponse:
        """
        Deletes a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-delete-a-storage-box

        :param storage_box: Storage Box to delete.
        """
        response = self._client.request(
            method="DELETE",
            url=f"{self._base_url}/{storage_box.id}",
        )

        return DeleteStorageBoxResponse(
            action=BoundAction(self._parent.actions, response["action"])
        )

    def get_folders(
        self,
        storage_box: BoundStorageBox | StorageBox,
        path: str | None = None,
    ) -> StorageBoxFoldersResponse:
        """
        Lists the (sub)folders contained in a Storage Box.

        Files are not part of the response.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-list-folders-of-a-storage-box

        :param storage_box: Storage Box to list the folders from.
        :param path: Relative path to list the folders from.
        """
        params: dict[str, Any] = {}
        if path is not None:
            params["path"] = path

        response = self._client.request(
            method="GET",
            url=f"{self._base_url}/{storage_box.id}/folders",
            params=params,
        )

        return StorageBoxFoldersResponse(folders=response["folders"])

    def get_actions_list(
        self,
        storage_box: StorageBox | BoundStorageBox,
        *,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """
        Returns all Actions for a Storage Box for a specific page.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-list-actions-for-a-storage-box

        :param storage_box: Storage Box to fetch the Actions from.
        :param status: Filter the actions by status. The response will only contain actions matching the specified statuses.
        :param sort: Sort resources by field and direction.
        :param page: Page number to return.
        :param per_page: Maximum number of entries returned per page.
        """
        params: dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(
            method="GET",
            url=f"/storage_boxes/{storage_box.id}/actions",
            params=params,
        )
        return ActionsPageResult(
            actions=[BoundAction(self._parent.actions, o) for o in response["actions"]],
            meta=Meta.parse_meta(response),
        )

    def get_actions(
        self,
        storage_box: StorageBox | BoundStorageBox,
        *,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """
        Returns all Actions for a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-list-actions-for-a-storage-box

        :param storage_box: Storage Box to fetch the Actions from.
        :param status: Filter the actions by status. The response will only contain actions matching the specified statuses.
        :param sort: Sort resources by field and direction.
        """
        return self._iter_pages(
            self.get_actions_list,
            storage_box,
            status=status,
            sort=sort,
        )

    def change_protection(
        self,
        storage_box: StorageBox | BoundStorageBox,
        *,
        delete: bool | None = None,
    ) -> BoundAction:
        """
        Changes the protection of a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-change-protection

        :param storage_box: Storage Box to update.
        :param delete: Prevents the Storage Box from being deleted.
        """
        data: dict[str, Any] = {}
        if delete is not None:
            data["delete"] = delete

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{storage_box.id}/actions/change_protection",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def change_type(
        self,
        storage_box: StorageBox | BoundStorageBox,
        storage_box_type: StorageBoxType | BoundStorageBoxType,
    ) -> BoundAction:
        """
        Changes the type of a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-change-type

        :param storage_box: Storage Box to update.
        :param storage_box_type: Storage Box Type to change to.
        """
        data: dict[str, Any] = {
            "storage_box_type": storage_box_type.id_or_name,
        }

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{storage_box.id}/actions/change_type",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def reset_password(
        self,
        storage_box: StorageBox | BoundStorageBox,
        *,
        password: str,
    ) -> BoundAction:
        """
        Reset the password of a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-reset-password

        :param storage_box: Storage Box to update.
        :param password: New password.
        """
        data: dict[str, Any] = {
            "password": password,
        }

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{storage_box.id}/actions/reset_password",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def update_access_settings(
        self,
        storage_box: StorageBox | BoundStorageBox,
        access_settings: StorageBoxAccessSettings,
    ) -> BoundAction:
        """
        Reset the password of a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-update-access-settings

        :param storage_box: Storage Box to update.
        :param access_settings: New access settings for the Storage Box.
        """
        data: dict[str, Any] = access_settings.to_payload()

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{storage_box.id}/actions/update_access_settings",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def rollback_snapshot(
        self,
        storage_box: StorageBox | BoundStorageBox,
        snapshot: StorageBoxSnapshot,  # TODO: Add BoundStorageBoxSnapshot
    ) -> BoundAction:
        """
        Rollback the Storage Box to the given snapshot.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-rollback-snapshot

        :param storage_box: Storage Box to update.
        :param snapshot: Snapshot to rollback to.
        """
        data: dict[str, Any] = {
            "snapshot": snapshot.id_or_name,
        }

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{storage_box.id}/actions/rollback_snapshot",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def disable_snapshot_plan(
        self,
        storage_box: StorageBox | BoundStorageBox,
    ) -> BoundAction:
        """
        Disable the snapshot plan a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-disable-snapshot-plan

        :param storage_box: Storage Box to update.
        """
        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{storage_box.id}/actions/disable_snapshot_plan",
        )
        return BoundAction(self._parent.actions, response["action"])

    def enable_snapshot_plan(
        self,
        storage_box: StorageBox | BoundStorageBox,
        snapshot_plan: StorageBoxSnapshotPlan,
    ) -> BoundAction:
        """
        Enable the snapshot plan a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-enable-snapshot-plan

        :param storage_box: Storage Box to update.
        :param snapshot_plan: Snapshot Plan to enable.
        """
        data: dict[str, Any] = snapshot_plan.to_payload()

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{storage_box.id}/actions/enable_snapshot_plan",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    # Snapshots
    ###########################################################################

    def get_snapshot_by_id(
        self,
        storage_box: StorageBox | BoundStorageBox,
        id: int,
    ) -> BoundStorageBoxSnapshot:
        """
        Returns a single Snapshot from a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-get-a-snapshot

        :param storage_box: Storage Box to get the Snapshot from.
        :param id: ID of the Snapshot.
        """
        response = self._client.request(
            method="GET",
            url=f"{self._base_url}/{storage_box.id}/snapshots/{id}",
        )
        return BoundStorageBoxSnapshot(self, response["snapshot"])

    def get_snapshot_by_name(
        self,
        storage_box: StorageBox | BoundStorageBox,
        name: str,
    ) -> BoundStorageBoxSnapshot:
        """
        Returns a single Snapshot from a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-list-snapshots

        :param storage_box: Storage Box to get the Snapshot from.
        :param name: Name of the Snapshot.
        """
        return self._get_first_by(self.get_snapshot_list, storage_box, name=name)

    def get_snapshot_list(
        self,
        storage_box: StorageBox | BoundStorageBox,
        *,
        name: str | None = None,
        is_automatic: bool | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
    ) -> StorageBoxSnapshotsPageResult:
        """
        Returns all Snapshots for a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-list-snapshots

        :param storage_box: Storage Box to get the Snapshots from.
        :param name: Filter resources by their name. The response will only contain the resources matching exactly the specified name.
        :param is_automatic: Filter wether the snapshot was made by a Snapshot Plan.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if is_automatic is not None:
            params["is_automatic"] = is_automatic
        if label_selector is not None:
            params["label_selector"] = label_selector
        if sort is not None:
            params["sort"] = sort

        response = self._client.request(
            method="GET",
            url=f"{self._base_url}/{storage_box.id}/snapshots",
            params=params,
        )
        return StorageBoxSnapshotsPageResult(
            snapshots=[
                BoundStorageBoxSnapshot(self, item) for item in response["snapshots"]
            ],
            meta=Meta.parse_meta(response),
        )

    def get_snapshot_all(
        self,
        storage_box: StorageBox | BoundStorageBox,
        *,
        name: str | None = None,
        is_automatic: bool | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundStorageBoxSnapshot]:
        """
        Returns all Snapshots for a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-list-snapshots

        :param storage_box: Storage Box to get the Snapshots from.
        :param name: Filter resources by their name. The response will only contain the resources matching exactly the specified name.
        :param is_automatic: Filter wether the snapshot was made by a Snapshot Plan.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.
        """
        # The endpoint does not have pagination, forward to the list method.
        result, _ = self.get_snapshot_list(
            storage_box,
            name=name,
            is_automatic=is_automatic,
            label_selector=label_selector,
            sort=sort,
        )
        return result

    def create_snapshot(
        self,
        storage_box: StorageBox | BoundStorageBox,
        *,
        description: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> CreateStorageBoxSnapshotResponse:
        """
        Creates a Snapshot of the Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-create-a-snapshot

        :param storage_box: Storage Box to create a Snapshot from.
        :param description: Description of the Snapshot.
        :param labels: User-defined labels (key/value pairs) for the Resource.
        """
        data: dict[str, Any] = {}
        if description is not None:
            data["description"] = description
        if labels is not None:
            data["labels"] = labels

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{storage_box.id}/snapshots",
            json=data,
        )
        return CreateStorageBoxSnapshotResponse(
            snapshot=BoundStorageBoxSnapshot(self, response["snapshot"]),
            action=BoundAction(self._parent.actions, response["action"]),
        )

    def update_snapshot(
        self,
        snapshot: StorageBoxSnapshot | BoundStorageBoxSnapshot,
        *,
        description: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundStorageBoxSnapshot:
        """
        Updates a Storage Box Snapshot.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-update-a-snapshot

        :param snapshot: Storage Box Snapshot to update.
        :param labels: User-defined labels (key/value pairs) for the Resource.
        """
        if snapshot.storage_box is None:
            raise ValueError("snapshot storage_box property is none")

        data: dict[str, Any] = {}
        if description is not None:
            data["description"] = description
        if labels is not None:
            data["labels"] = labels

        response = self._client.request(
            method="PUT",
            url=f"{self._base_url}/{snapshot.storage_box.id}/snapshots/{snapshot.id}",
            json=data,
        )
        return BoundStorageBoxSnapshot(self, response["snapshot"])

    def delete_snapshot(
        self,
        snapshot: StorageBoxSnapshot | BoundStorageBoxSnapshot,
    ) -> DeleteStorageBoxSnapshotResponse:
        """
        Deletes a Storage Box Snapshot.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-delete-a-snapshot

        :param snapshot: Storage Box Snapshot to delete.
        """
        if snapshot.storage_box is None:
            raise ValueError("snapshot storage_box property is none")

        response = self._client.request(
            method="DELETE",
            url=f"{self._base_url}/{snapshot.storage_box.id}/snapshots/{snapshot.id}",
        )
        return DeleteStorageBoxSnapshotResponse(
            action=BoundAction(self._parent.actions, response["action"]),
        )
