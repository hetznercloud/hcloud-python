from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

from ..actions import (
    ActionSort,
    ActionsPageResult,
    ActionStatus,
    BoundAction,
    ResourceActionsClient,
)
from ..actions.client import ResourceClientBaseActionsMixin
from ..core import BoundModelBase, Meta, ResourceClientBase
from ..locations import BoundLocation, Location
from ..ssh_keys import BoundSSHKey, SSHKey
from ..storage_box_types import BoundStorageBoxType, StorageBoxType
from .domain import (
    CreateStorageBoxResponse,
    CreateStorageBoxSnapshotResponse,
    CreateStorageBoxSubaccountResponse,
    DeleteStorageBoxResponse,
    DeleteStorageBoxSnapshotResponse,
    DeleteStorageBoxSubaccountResponse,
    StorageBox,
    StorageBoxAccessSettings,
    StorageBoxFoldersResponse,
    StorageBoxSnapshot,
    StorageBoxSnapshotPlan,
    StorageBoxSnapshotStats,
    StorageBoxStats,
    StorageBoxSubaccount,
    StorageBoxSubaccountAccessSettings,
)

if TYPE_CHECKING:
    from .._client import Client

__all__ = [
    "BoundStorageBox",
    "BoundStorageBoxSnapshot",
    "BoundStorageBoxSubaccount",
    "StorageBoxesPageResult",
    "StorageBoxSnapshotsPageResult",
    "StorageBoxSubaccountsPageResult",
    "StorageBoxesClient",
]


class BoundStorageBox(BoundModelBase[StorageBox], StorageBox):
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
        status: list[ActionStatus] | None = None,
        sort: list[ActionSort] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """
        Returns a paginated list of Actions for a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-list-actions-for-a-storage-box

        :param status: Filter the Actions by status.
        :param sort: Sort Actions by field and direction.
        :param page: Page number to get.
        :param per_page: Maximum number of Actions returned per page.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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
        status: list[ActionStatus] | None = None,
        sort: list[ActionSort] | None = None,
    ) -> list[BoundAction]:
        """
        Returns all Actions for a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-list-actions-for-a-storage-box

        :param status: Filter the actions by status. The response will only contain actions matching the specified statuses.
        :param sort: Sort resources by field and direction.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.get_actions(
            self,
            status=status,
            sort=sort,
        )

    def update(
        self,
        *,
        name: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundStorageBox:
        """
        Updates a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-update-a-storage-box

        :param name: Name of the Storage Box.
        :param labels: User-defined labels (key/value pairs) for the Storage Box.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.update(
            self,
            name=name,
            labels=labels,
        )

    def delete(self) -> DeleteStorageBoxResponse:
        """
        Deletes a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-delete-a-storage-box

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.delete(self)

    def get_folders(
        self,
        *,
        path: str | None = None,
    ) -> StorageBoxFoldersResponse:
        """
        Lists the (sub)folders contained in a Storage Box.

        Files are not part of the response.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-list-folders-of-a-storage-box

        :param path: Relative path to list the folders from.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.get_folders(
            self,
            path=path,
        )

    def change_protection(
        self,
        *,
        delete: bool | None = None,
    ) -> BoundAction:
        """
        Changes the protection of a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-change-protection

        :param delete: Prevents the Storage Box from being deleted.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.change_protection(
            self,
            delete=delete,
        )

    def change_type(
        self,
        storage_box_type: StorageBoxType | BoundStorageBoxType,
    ) -> BoundAction:
        """
        Changes the type of a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-change-type

        :param storage_box_type: Storage Box Type to change to.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.change_type(
            self,
            storage_box_type=storage_box_type,
        )

    def reset_password(
        self,
        password: str,
    ) -> BoundAction:
        """
        Reset the password of a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-reset-password

        :param password: New password.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.reset_password(
            self,
            password=password,
        )

    def update_access_settings(
        self,
        access_settings: StorageBoxAccessSettings,
    ) -> BoundAction:
        """
        Update the access settings of a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-update-access-settings

        :param access_settings: New access settings for the Storage Box.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.update_access_settings(
            self,
            access_settings=access_settings,
        )

    def rollback_snapshot(
        self,
        snapshot: StorageBoxSnapshot | BoundStorageBoxSnapshot,
    ) -> BoundAction:
        """
        Rollback the Storage Box to the given snapshot.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-rollback-snapshot

        :param snapshot: Snapshot to rollback to.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.rollback_snapshot(
            self,
            snapshot=snapshot,
        )

    def disable_snapshot_plan(
        self,
    ) -> BoundAction:
        """
        Disable the snapshot plan of a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-disable-snapshot-plan

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.disable_snapshot_plan(self)

    def enable_snapshot_plan(
        self,
        snapshot_plan: StorageBoxSnapshotPlan,
    ) -> BoundAction:
        """
        Enable the snapshot plan of a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-enable-snapshot-plan

        :param snapshot_plan: Snapshot Plan to enable.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.enable_snapshot_plan(
            self,
            snapshot_plan=snapshot_plan,
        )

    # Snapshots
    ###########################################################################

    def get_snapshot_by_id(
        self,
        id: int,
    ) -> BoundStorageBoxSnapshot:
        """
        Returns a single Snapshot from a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-get-a-snapshot

        :param id: ID of the Snapshot.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.get_snapshot_by_id(self, id=id)

    def get_snapshot_by_name(
        self,
        name: str,
    ) -> BoundStorageBoxSnapshot | None:
        """
        Returns a single Snapshot from a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-list-snapshots

        :param name: Name of the Snapshot.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.get_snapshot_by_name(self, name=name)

    def get_snapshot_list(
        self,
        *,
        name: str | None = None,
        is_automatic: bool | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
    ) -> StorageBoxSnapshotsPageResult:
        """
        Returns all Snapshots for a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-list-snapshots

        :param name: Filter resources by their name. The response will only contain the resources matching exactly the specified name.
        :param is_automatic: Filter wether the snapshot was made by a Snapshot Plan.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.get_snapshot_list(
            self,
            name=name,
            is_automatic=is_automatic,
            label_selector=label_selector,
            sort=sort,
        )

    def get_snapshot_all(
        self,
        *,
        name: str | None = None,
        is_automatic: bool | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundStorageBoxSnapshot]:
        """
        Returns all Snapshots for a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-list-snapshots

        :param name: Filter resources by their name. The response will only contain the resources matching exactly the specified name.
        :param is_automatic: Filter whether the snapshot was made by a Snapshot Plan.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.get_snapshot_all(
            self,
            name=name,
            is_automatic=is_automatic,
            label_selector=label_selector,
            sort=sort,
        )

    def create_snapshot(
        self,
        *,
        description: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> CreateStorageBoxSnapshotResponse:
        """
        Creates a Snapshot of the Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-create-a-snapshot

        :param description: Description of the Snapshot.
        :param labels: User-defined labels (key/value pairs) for the Snapshot.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.create_snapshot(
            self,
            description=description,
            labels=labels,
        )

    # Subaccounts
    ###########################################################################

    def get_subaccount_by_id(
        self,
        id: int,
    ) -> BoundStorageBoxSubaccount:
        """
        Returns a single Subaccount from a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccounts-get-a-subaccount

        :param id: ID of the Subaccount.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.get_subaccount_by_id(self, id=id)

    def get_subaccount_by_username(
        self,
        username: str,
    ) -> BoundStorageBoxSubaccount | None:
        """
        Returns a single Subaccount from a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccounts-list-subaccounts

        :param username: User name of the Subaccount.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.get_subaccount_by_username(self, username=username)

    def get_subaccount_list(
        self,
        *,
        username: str | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
    ) -> StorageBoxSubaccountsPageResult:
        """
        Returns all Subaccounts for a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccounts-list-subaccounts

        :param username: Filter resources by their username. The response will only contain the resources matching exactly the specified username.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.get_subaccount_list(
            self,
            username=username,
            label_selector=label_selector,
            sort=sort,
        )

    def get_subaccount_all(
        self,
        *,
        username: str | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundStorageBoxSubaccount]:
        """
        Returns all Subaccounts for a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccounts-list-subaccounts

        :param username: Filter resources by their username. The response will only contain the resources matching exactly the specified username.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.get_subaccount_all(
            self,
            username=username,
            label_selector=label_selector,
            sort=sort,
        )

    def create_subaccount(
        self,
        *,
        home_directory: str,
        password: str,
        access_settings: StorageBoxSubaccountAccessSettings | None = None,
        description: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> CreateStorageBoxSubaccountResponse:
        """
        Creates a Subaccount for the Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccounts-create-a-subaccount

        :param storage_box: Storage Box to create a Subaccount for.
        :param home_directory: Home directory of the Subaccount.
        :param password: Password of the Subaccount.
        :param access_settings: Access settings of the Subaccount.
        :param description: Description of the Subaccount.
        :param labels: User-defined labels (key/value pairs) for the Subaccount.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.create_subaccount(
            self,
            home_directory=home_directory,
            password=password,
            access_settings=access_settings,
            description=description,
            labels=labels,
        )


class BoundStorageBoxSnapshot(BoundModelBase[StorageBoxSnapshot], StorageBoxSnapshot):
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

    def _get_self(self) -> BoundStorageBoxSnapshot:
        assert self.data_model.storage_box is not None
        assert self.data_model.id is not None
        return self._client.get_snapshot_by_id(
            self.data_model.storage_box,
            self.data_model.id,
        )

    def update(
        self,
        *,
        description: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundStorageBoxSnapshot:
        """
        Updates a Storage Box Snapshot.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-update-a-snapshot

        :param description: Description of the Snapshot.
        :param labels: User-defined labels (key/value pairs) for the Snapshot.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.update_snapshot(
            self,
            description=description,
            labels=labels,
        )

    def delete(
        self,
    ) -> DeleteStorageBoxSnapshotResponse:
        """
        Deletes a Storage Box Snapshot.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-delete-a-snapshot

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.delete_snapshot(self)


class BoundStorageBoxSubaccount(
    BoundModelBase[StorageBoxSubaccount], StorageBoxSubaccount
):
    _client: StorageBoxesClient

    model = StorageBoxSubaccount

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

        raw = data.get("access_settings")
        if raw is not None:
            data["access_settings"] = StorageBoxSubaccountAccessSettings.from_dict(raw)

        super().__init__(client, data, complete)

    def _get_self(self) -> BoundStorageBoxSubaccount:
        assert self.data_model.storage_box is not None
        assert self.data_model.id is not None
        return self._client.get_subaccount_by_id(
            self.data_model.storage_box,
            self.data_model.id,
        )

    def update(
        self,
        *,
        description: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundStorageBoxSubaccount:
        """
        Updates a Storage Box Subaccount.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccounts-update-a-subaccount

        :param description: Description of the Subaccount.
        :param labels: User-defined labels (key/value pairs) for the Subaccount.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.update_subaccount(
            self,
            description=description,
            labels=labels,
        )

    def delete(
        self,
    ) -> DeleteStorageBoxSubaccountResponse:
        """
        Deletes a Storage Box Subaccount.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccounts-delete-a-subaccount

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.delete_subaccount(self)

    def change_home_directory(
        self,
        home_directory: str,
    ) -> BoundAction:
        """
        Change the home directory of a Storage Box Subaccount.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccount-actions-change-home-directory

        :param home_directory: Home directory for the Subaccount.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.change_subaccount_home_directory(
            self, home_directory=home_directory
        )

    def reset_password(
        self,
        password: str,
    ) -> BoundAction:
        """
        Reset the password of a Storage Box Subaccount.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccount-actions-reset-password

        :param password: Password for the Subaccount.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.reset_subaccount_password(self, password=password)

    def update_access_settings(
        self,
        access_settings: StorageBoxSubaccountAccessSettings,
    ) -> BoundAction:
        """
        Update the access settings of a Storage Box Subaccount.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccount-actions-update-access-settings

        :param access_settings: Access settings for the Subaccount.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._client.update_subaccount_access_settings(
            self,
            access_settings=access_settings,
        )


class StorageBoxesPageResult(NamedTuple):
    storage_boxes: list[BoundStorageBox]
    meta: Meta


class StorageBoxSnapshotsPageResult(NamedTuple):
    snapshots: list[BoundStorageBoxSnapshot]
    meta: Meta


class StorageBoxSubaccountsPageResult(NamedTuple):
    subaccounts: list[BoundStorageBoxSubaccount]
    meta: Meta


class StorageBoxesClient(
    ResourceClientBaseActionsMixin,
    ResourceClientBase,
):
    """
    A client for the Storage Boxes API.

    See https://docs.hetzner.cloud/reference/hetzner#storage-boxes.

    Experimental:
        Storage Box support is experimental, breaking changes may occur within minor releases.
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

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._get_first_by(self.get_list, name=name)

    def get_list(
        self,
        *,
        name: str | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> StorageBoxesPageResult:
        """
        Returns a paginated list of Storage Boxes for a specific page.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-list-storage-boxes

        :param name: Name of the Storage Box.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.
        :param page: Page number to return.
        :param per_page: Maximum number of entries returned per page.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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
        if sort is not None:
            params["sort"] = sort

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
        *,
        name: str | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundStorageBox]:
        """
        Returns all Storage Boxes.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-list-storage-boxes

        :param name: Name of the Storage Box.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._iter_pages(
            self.get_list,
            name=name,
            label_selector=label_selector,
            sort=sort,
        )

    def create(
        self,
        *,
        name: str,
        password: str,
        location: BoundLocation | Location,
        storage_box_type: BoundStorageBoxType | StorageBoxType,
        ssh_keys: list[str | SSHKey | BoundSSHKey] | None = None,
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

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        data: dict[str, Any] = {
            "name": name,
            "password": password,
            "location": location.id_or_name,
            "storage_box_type": storage_box_type.id_or_name,
        }
        if ssh_keys is not None:
            data["ssh_keys"] = [
                o.public_key if isinstance(o, (SSHKey, BoundSSHKey)) else o
                for o in ssh_keys
            ]
        if access_settings is not None:
            data["access_settings"] = access_settings.to_payload()
        if labels is not None:
            data["labels"] = labels

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}",
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

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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
        *,
        path: str | None = None,
    ) -> StorageBoxFoldersResponse:
        """
        Lists the (sub)folders contained in a Storage Box.

        Files are not part of the response.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-list-folders-of-a-storage-box

        :param storage_box: Storage Box to list the folders from.
        :param path: Relative path to list the folders from.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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
        status: list[ActionStatus] | None = None,
        sort: list[ActionSort] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """
        Returns a paginated list of Actions for a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-list-actions-for-a-storage-box

        :param storage_box: Storage Box to get the Actions for.
        :param status: Filter the Actions by status.
        :param sort: Sort Actions by field and direction.
        :param page: Page number to get.
        :param per_page: Maximum number of Actions returned per page.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._get_actions_list(
            f"{self._base_url}/{storage_box.id}",
            status=status,
            sort=sort,
            page=page,
            per_page=per_page,
        )

    def get_actions(
        self,
        storage_box: StorageBox | BoundStorageBox,
        *,
        status: list[ActionStatus] | None = None,
        sort: list[ActionSort] | None = None,
    ) -> list[BoundAction]:
        """
        Returns all Actions for a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-list-actions-for-a-storage-box

        :param storage_box: Storage Box to get the Actions for.
        :param status: Filter the actions by status. The response will only contain actions matching the specified statuses.
        :param sort: Sort resources by field and direction.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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
        password: str,
    ) -> BoundAction:
        """
        Reset the password of a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-reset-password

        :param storage_box: Storage Box to update.
        :param password: New password.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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
        Update the access settings of a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-update-access-settings

        :param storage_box: Storage Box to update.
        :param access_settings: New access settings for the Storage Box.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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
        snapshot: StorageBoxSnapshot | BoundStorageBoxSnapshot,
    ) -> BoundAction:
        """
        Rollback the Storage Box to the given snapshot.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-rollback-snapshot

        :param storage_box: Storage Box to update.
        :param snapshot: Snapshot to rollback to.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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
        Disable the snapshot plan of a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-disable-snapshot-plan

        :param storage_box: Storage Box to update.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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
        Enable the snapshot plan of a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-actions-enable-snapshot-plan

        :param storage_box: Storage Box to update.
        :param snapshot_plan: Snapshot Plan to enable.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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
    ) -> BoundStorageBoxSnapshot | None:
        """
        Returns a single Snapshot from a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-snapshots-list-snapshots

        :param storage_box: Storage Box to get the Snapshot from.
        :param name: Name of the Snapshot.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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
        :param is_automatic: Filter whether the snapshot was made by a Snapshot Plan.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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
        :param is_automatic: Filter whether the snapshot was made by a Snapshot Plan.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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
        :param labels: User-defined labels (key/value pairs) for the Snapshot.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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
            snapshot=BoundStorageBoxSnapshot(
                self,
                response["snapshot"],
                # API only returns a partial object.
                complete=False,
            ),
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
        :param description: Description of the Snapshot.
        :param labels: User-defined labels (key/value pairs) for the Snapshot.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
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

    # Subaccounts
    ###########################################################################

    def get_subaccount_by_id(
        self,
        storage_box: StorageBox | BoundStorageBox,
        id: int,
    ) -> BoundStorageBoxSubaccount:
        """
        Returns a single Subaccount from a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccounts-get-a-subaccount

        :param storage_box: Storage Box to get the Subaccount from.
        :param id: ID of the Subaccount.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        response = self._client.request(
            method="GET",
            url=f"{self._base_url}/{storage_box.id}/subaccounts/{id}",
        )
        return BoundStorageBoxSubaccount(self, response["subaccount"])

    def get_subaccount_by_username(
        self,
        storage_box: StorageBox | BoundStorageBox,
        username: str,
    ) -> BoundStorageBoxSubaccount | None:
        """
        Returns a single Subaccount from a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccounts-list-subaccounts

        :param storage_box: Storage Box to get the Subaccount from.
        :param username: User name of the Subaccount.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._get_first_by(
            self.get_subaccount_list,
            storage_box,
            username=username,
        )

    def get_subaccount_list(
        self,
        storage_box: StorageBox | BoundStorageBox,
        *,
        username: str | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
    ) -> StorageBoxSubaccountsPageResult:
        """
        Returns all Subaccounts for a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccounts-list-subaccounts

        :param storage_box: Storage Box to get the Subaccount from.
        :param username: Filter resources by their username. The response will only contain the resources matching exactly the specified username.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        params: dict[str, Any] = {}
        if username is not None:
            params["username"] = username
        if label_selector is not None:
            params["label_selector"] = label_selector
        if sort is not None:
            params["sort"] = sort

        response = self._client.request(
            method="GET",
            url=f"{self._base_url}/{storage_box.id}/subaccounts",
            params=params,
        )
        return StorageBoxSubaccountsPageResult(
            subaccounts=[
                BoundStorageBoxSubaccount(self, item)
                for item in response["subaccounts"]
            ],
            meta=Meta.parse_meta(response),
        )

    def get_subaccount_all(
        self,
        storage_box: StorageBox | BoundStorageBox,
        *,
        username: str | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundStorageBoxSubaccount]:
        """
        Returns all Subaccounts for a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccounts-list-subaccounts

        :param storage_box: Storage Box to get the Subaccount from.
        :param username: Filter resources by their username. The response will only contain the resources matching exactly the specified username.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        # The endpoint does not have pagination, forward to the list method.
        result, _ = self.get_subaccount_list(
            storage_box,
            username=username,
            label_selector=label_selector,
            sort=sort,
        )
        return result

    def create_subaccount(
        self,
        storage_box: StorageBox | BoundStorageBox,
        *,
        home_directory: str,
        password: str,
        access_settings: StorageBoxSubaccountAccessSettings | None = None,
        description: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> CreateStorageBoxSubaccountResponse:
        """
        Creates a Subaccount for the Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccounts-create-a-subaccount

        :param storage_box: Storage Box to create a Subaccount for.
        :param home_directory: Home directory of the Subaccount.
        :param password: Password of the Subaccount.
        :param access_settings: Access settings of the Subaccount.
        :param description: Description of the Subaccount.
        :param labels: User-defined labels (key/value pairs) for the Subaccount.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        data: dict[str, Any] = {
            "home_directory": home_directory,
            "password": password,
        }
        if access_settings is not None:
            data["access_settings"] = access_settings.to_payload()
        if description is not None:
            data["description"] = description
        if labels is not None:
            data["labels"] = labels

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{storage_box.id}/subaccounts",
            json=data,
        )
        return CreateStorageBoxSubaccountResponse(
            subaccount=BoundStorageBoxSubaccount(
                self,
                response["subaccount"],
                # API only returns a partial object.
                complete=False,
            ),
            action=BoundAction(self._parent.actions, response["action"]),
        )

    def update_subaccount(
        self,
        subaccount: StorageBoxSubaccount | BoundStorageBoxSubaccount,
        *,
        description: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundStorageBoxSubaccount:
        """
        Updates a Storage Box Subaccount.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccounts-update-a-subaccount

        :param subaccount: Storage Box Subaccount to update.
        :param description: Description of the Subaccount.
        :param labels: User-defined labels (key/value pairs) for the Subaccount.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        if subaccount.storage_box is None:
            raise ValueError("subaccount storage_box property is none")

        data: dict[str, Any] = {}
        if description is not None:
            data["description"] = description
        if labels is not None:
            data["labels"] = labels

        response = self._client.request(
            method="PUT",
            url=f"{self._base_url}/{subaccount.storage_box.id}/subaccounts/{subaccount.id}",
            json=data,
        )
        return BoundStorageBoxSubaccount(self, response["subaccount"])

    def delete_subaccount(
        self,
        subaccount: StorageBoxSubaccount | BoundStorageBoxSubaccount,
    ) -> DeleteStorageBoxSubaccountResponse:
        """
        Deletes a Storage Box Subaccount.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccounts-delete-a-subaccount

        :param subaccount: Storage Box Subaccount to delete.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        if subaccount.storage_box is None:
            raise ValueError("subaccount storage_box property is none")

        response = self._client.request(
            method="DELETE",
            url=f"{self._base_url}/{subaccount.storage_box.id}/subaccounts/{subaccount.id}",
        )
        return DeleteStorageBoxSubaccountResponse(
            action=BoundAction(self._parent.actions, response["action"]),
        )

    def change_subaccount_home_directory(
        self,
        subaccount: StorageBoxSubaccount | BoundStorageBoxSubaccount,
        home_directory: str,
    ) -> BoundAction:
        """
        Change the home directory of a Storage Box Subaccount.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccount-actions-change-home-directory

        :param subaccount: Storage Box Subaccount to update.
        :param home_directory: Home directory for the Subaccount.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        if subaccount.storage_box is None:
            raise ValueError("subaccount storage_box property is none")

        data: dict[str, Any] = {
            "home_directory": home_directory,
        }

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{subaccount.storage_box.id}/subaccounts/{subaccount.id}/actions/change_home_directory",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def reset_subaccount_password(
        self,
        subaccount: StorageBoxSubaccount | BoundStorageBoxSubaccount,
        password: str,
    ) -> BoundAction:
        """
        Reset the password of a Storage Box Subaccount.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccount-actions-reset-password

        :param subaccount: Storage Box Subaccount to update.
        :param password: Password for the Subaccount.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        if subaccount.storage_box is None:
            raise ValueError("subaccount storage_box property is none")

        data: dict[str, Any] = {
            "password": password,
        }

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{subaccount.storage_box.id}/subaccounts/{subaccount.id}/actions/reset_subaccount_password",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def update_subaccount_access_settings(
        self,
        subaccount: StorageBoxSubaccount | BoundStorageBoxSubaccount,
        access_settings: StorageBoxSubaccountAccessSettings,
    ) -> BoundAction:
        """
        Update the access settings of a Storage Box Subaccount.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-subaccount-actions-update-access-settings

        :param subaccount: Storage Box Subaccount to update.
        :param access_settings: Access settings for the Subaccount.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        if subaccount.storage_box is None:
            raise ValueError("subaccount storage_box property is none")

        data: dict[str, Any] = access_settings.to_payload()

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{subaccount.storage_box.id}/subaccounts/{subaccount.id}/actions/update_access_settings",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])
