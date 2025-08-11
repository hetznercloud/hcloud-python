from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

from ..actions import BoundAction
from ..core import BoundModelBase, ClientEntityBase, Meta
from ..locations import BoundLocation, Location
from ..storage_box_types import BoundStorageBoxType, StorageBoxType
from .domain import (
    CreateStorageBoxResponse,
    DeleteStorageBoxResponse,
    StorageBox,
    StorageBoxAccessSettings,
    StorageBoxFoldersResponse,
    StorageBoxSnapshotPlan,
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
                client._client.storage_box_types, raw
            )

        raw = data.get("location")
        if raw is not None:
            data["location"] = BoundLocation(client._client.locations, raw)

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

    # TODO: implement bound methods


class StorageBoxesPageResult(NamedTuple):
    storage_boxes: list[BoundStorageBox]
    meta: Meta


class StorageBoxesClient(ClientEntityBase):
    """
    A client for the Storage Boxes API.

    See https://docs.hetzner.cloud/reference/hetzner#storage-boxes.
    """

    _client: Client

    def get_by_id(self, id: int) -> BoundStorageBox:
        """
        Returns a specific Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-get-a-storage-box

        :param id: ID of the Storage Box.
        """
        response = self._client._request_hetzner(  # pylint: disable=protected-access
            method="GET",
            url=f"/storage_boxes/{id}",
        )
        return BoundStorageBox(self, response["storage_box"])

    def get_by_name(self, name: str) -> BoundStorageBox | None:
        """
        Returns a specific Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-list-storage-boxes

        :param name: Name of the Storage Box.
        """
        return self._get_first_by(name=name)

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

        response = self._client._request_hetzner(  # pylint: disable=protected-access
            method="GET",
            url="/storage_boxes",
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
            "location": location.name,  # TODO: ID or name ?
            "storage_box_type": storage_box_type.id_or_name,
        }
        if ssh_keys is not None:
            data["ssh_keys"] = ssh_keys
        if access_settings is not None:
            data["access_settings"] = access_settings.to_payload()
        if labels is not None:
            data["labels"] = labels

        response = self._client._request_hetzner(  # pylint: disable=protected-access
            method="POST",
            url="/storage_boxes",
            json=data,
        )

        return CreateStorageBoxResponse(
            storage_box=BoundStorageBox(self, response["storage_box"]),
            action=BoundAction(self._client.actions, response["action"]),
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

        response = self._client._request_hetzner(  # pylint: disable=protected-access
            method="PUT",
            url=f"/storage_boxes/{storage_box.id}",
            json=data,
        )

        return BoundStorageBox(self, response["storage_box"])

    def delete(
        self,
        storage_box: BoundStorageBox | StorageBox,
    ) -> DeleteStorageBoxResponse:
        """
        Deletes a Storage Box.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-delete-storage-box

        :param storage_box: Storage Box to delete.
        """
        response = self._client._request_hetzner(  # pylint: disable=protected-access
            method="DELETE",
            url=f"/storage_boxes/{storage_box.id}",
        )

        return DeleteStorageBoxResponse(
            action=BoundAction(self._client.actions, response["action"])
        )

    def get_folders(
        self,
        storage_box: BoundStorageBox | StorageBox,
        path: str | None = None,
    ) -> StorageBoxFoldersResponse:
        """
        Lists the (sub)folders contained in a Storage Box.

        Files are not part of the response.

        See https://docs.hetzner.cloud/reference/hetzner#storage-boxes-list-content-of-storage-box

        :param storage_box: Storage Box to list the folders from.
        :param path: Relative path to list the folders from.
        """
        params: dict[str, Any] = {}
        if path is not None:
            params["path"] = path

        response = self._client._request_hetzner(  # pylint: disable=protected-access
            method="GET",
            url=f"/storage_boxes/{storage_box.id}/folders",
            params=params,
        )

        return StorageBoxFoldersResponse(folders=response["folders"])
