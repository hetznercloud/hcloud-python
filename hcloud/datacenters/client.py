from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any, NamedTuple

from ..core import BoundModelBase, Meta, ResourceClientBase
from ..locations import BoundLocation
from ..server_types import BoundServerType
from .domain import Datacenter, DatacenterServerTypes

if TYPE_CHECKING:
    from .._client import Client

__all__ = [
    "BoundDatacenter",
    "DatacentersPageResult",
    "DatacentersClient",
]

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    class BoundDatacenter(BoundModelBase[Datacenter], Datacenter):
        """
        .. deprecated:: 2.22.0
            The bound datacenter class is deprecated and will be removed after the 2026-10-01.
            See https://docs.hetzner.cloud/changelog#2026-06-02-datacenters-deprecated.
        """

        _client: DatacentersClient

        model = Datacenter

        def __init__(self, client: DatacentersClient, data: dict[str, Any]):
            location = data.get("location")
            if location is not None:
                data["location"] = BoundLocation(client._parent.locations, location)

            server_types = data.get("server_types")
            if server_types is not None:
                available = [
                    BoundServerType(
                        client._parent.server_types, {"id": server_type}, complete=False
                    )
                    for server_type in server_types["available"]
                ]
                supported = [
                    BoundServerType(
                        client._parent.server_types, {"id": server_type}, complete=False
                    )
                    for server_type in server_types["supported"]
                ]
                available_for_migration = [
                    BoundServerType(
                        client._parent.server_types, {"id": server_type}, complete=False
                    )
                    for server_type in server_types["available_for_migration"]
                ]
                data["server_types"] = DatacenterServerTypes(
                    available=available,
                    supported=supported,
                    available_for_migration=available_for_migration,
                )

            super().__init__(client, data)


class DatacentersPageResult(NamedTuple):
    """
    .. deprecated:: 2.22.0
        The datacenters page result class is deprecated and will be removed after the 2026-10-01.
        See https://docs.hetzner.cloud/changelog#2026-06-02-datacenters-deprecated.
    """

    datacenters: list[BoundDatacenter]
    meta: Meta


class DatacentersClient(ResourceClientBase):
    """
    .. deprecated:: 2.22.0
        The datacenters client class is deprecated and will be removed after the 2026-10-01.
        See https://docs.hetzner.cloud/changelog#2026-06-02-datacenters-deprecated.
    """

    _base_url = "/datacenters"

    def __init__(self, client: Client):
        warnings.warn(
            "The datacenters client class is deprecated and will be removed after the 2026-10-01. "
            "See https://docs.hetzner.cloud/changelog#2026-06-02-datacenters-deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(client)

    def get_by_id(self, id: int) -> BoundDatacenter:
        """Get a specific datacenter by its ID.

        :param id: int
        :return: :class:`BoundDatacenter <hcloud.datacenters.client.BoundDatacenter>`
        """
        response = self._client.request(url=f"{self._base_url}/{id}", method="GET")
        return BoundDatacenter(self, response["datacenter"])

    def get_list(
        self,
        name: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> DatacentersPageResult:
        """Get a list of datacenters

        :param name: str (optional)
               Can be used to filter datacenters by their name.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundDatacenter <hcloud.datacenters.client.BoundDatacenter>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name

        if page is not None:
            params["page"] = page

        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url=self._base_url, method="GET", params=params)

        datacenters = [
            BoundDatacenter(self, datacenter_data)
            for datacenter_data in response["datacenters"]
        ]

        return DatacentersPageResult(datacenters, Meta.parse_meta(response))

    def get_all(self, name: str | None = None) -> list[BoundDatacenter]:
        """Get all datacenters

        :param name: str (optional)
               Can be used to filter datacenters by their name.
        :return: List[:class:`BoundDatacenter <hcloud.datacenters.client.BoundDatacenter>`]
        """
        return self._iter_pages(self.get_list, name=name)

    def get_by_name(self, name: str) -> BoundDatacenter | None:
        """Get datacenter by name

        :param name: str
               Used to get datacenter by name.
        :return: :class:`BoundDatacenter <hcloud.datacenters.client.BoundDatacenter>`
        """
        return self._get_first_by(self.get_list, name=name)
