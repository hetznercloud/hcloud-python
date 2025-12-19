from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

from ..core import BoundModelBase, Meta, ResourceClientBase
from .domain import StorageBoxType

if TYPE_CHECKING:
    from .._client import Client

__all__ = [
    "BoundStorageBoxType",
    "StorageBoxTypesPageResult",
    "StorageBoxTypesClient",
]


class BoundStorageBoxType(BoundModelBase[StorageBoxType], StorageBoxType):
    _client: StorageBoxTypesClient

    model = StorageBoxType


class StorageBoxTypesPageResult(NamedTuple):
    storage_box_types: list[BoundStorageBoxType]
    meta: Meta


class StorageBoxTypesClient(ResourceClientBase):
    """
    A client for the Storage Box Types API.

    See https://docs.hetzner.cloud/reference/hetzner#storage-box-types.

    Experimental:
        Storage Box support is experimental, breaking changes may occur within minor releases.
    """

    _base_url = "/storage_box_types"

    def __init__(self, client: Client):
        super().__init__(client)
        self._client = client._client_hetzner

    def get_by_id(self, id: int) -> BoundStorageBoxType:
        """
        Returns a specific Storage Box Type.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-types-get-a-storage-box-type

        :param id: ID of the Storage Box Type.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        response = self._client.request(
            method="GET",
            url=f"{self._base_url}/{id}",
        )
        return BoundStorageBoxType(self, response["storage_box_type"])

    def get_by_name(self, name: str) -> BoundStorageBoxType | None:
        """
        Returns a specific Storage Box Type.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-types-list-storage-box-types

        :param name: Name of the Storage Box Type.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._get_first_by(self.get_list, name=name)

    def get_list(
        self,
        name: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> StorageBoxTypesPageResult:
        """
        Returns a list of Storage Box Types for a specific page.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-types-list-storage-box-types

        :param name: Name of the Storage Box Type.
        :param page: Page number to return.
        :param per_page: Maximum number of entries returned per page.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(
            method="GET",
            url=f"{self._base_url}",
            params=params,
        )
        return StorageBoxTypesPageResult(
            storage_box_types=[
                BoundStorageBoxType(self, o) for o in response["storage_box_types"]
            ],
            meta=Meta.parse_meta(response),
        )

    def get_all(
        self,
        name: str | None = None,
    ) -> list[BoundStorageBoxType]:
        """
        Returns all Storage Box Types.

        See https://docs.hetzner.cloud/reference/hetzner#storage-box-types-list-storage-box-types

        :param name: Name of the Storage Box Type.

        Experimental:
            Storage Box support is experimental, breaking changes may occur within minor releases.
        """
        return self._iter_pages(
            self.get_list,
            name=name,
        )
