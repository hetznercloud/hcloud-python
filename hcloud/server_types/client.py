from __future__ import annotations

from typing import Any, NamedTuple

from ..core import BoundModelBase, Meta, ResourceClientBase
from ..locations import BoundLocation
from .domain import ServerType, ServerTypeLocation


class BoundServerType(BoundModelBase, ServerType):
    _client: ServerTypesClient

    model = ServerType

    def __init__(
        self,
        client: ServerTypesClient,
        data: dict,
        complete: bool = True,
    ):
        raw = data.get("locations")
        if raw is not None:
            data["locations"] = [
                ServerTypeLocation.from_dict(
                    {
                        "location": BoundLocation(
                            client._parent.locations, o, complete=False
                        ),
                        **o,
                    }
                )
                for o in raw
            ]

        super().__init__(client, data, complete)


class ServerTypesPageResult(NamedTuple):
    server_types: list[BoundServerType]
    meta: Meta


class ServerTypesClient(ResourceClientBase):
    _base_url = "/server_types"

    def get_by_id(self, id: int) -> BoundServerType:
        """Returns a specific Server Type.

        :param id: int
        :return: :class:`BoundServerType <hcloud.server_types.client.BoundServerType>`
        """
        response = self._client.request(url=f"{self._base_url}/{id}", method="GET")
        return BoundServerType(self, response["server_type"])

    def get_list(
        self,
        name: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ServerTypesPageResult:
        """Get a list of Server types

        :param name: str (optional)
               Can be used to filter server type by their name.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundServerType <hcloud.server_types.client.BoundServerType>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url=self._base_url, method="GET", params=params)
        server_types = [
            BoundServerType(self, server_type_data)
            for server_type_data in response["server_types"]
        ]
        return ServerTypesPageResult(server_types, Meta.parse_meta(response))

    def get_all(self, name: str | None = None) -> list[BoundServerType]:
        """Get all Server types

        :param name: str (optional)
               Can be used to filter server type by their name.
        :return: List[:class:`BoundServerType <hcloud.server_types.client.BoundServerType>`]
        """
        return self._iter_pages(self.get_list, name=name)

    def get_by_name(self, name: str) -> BoundServerType | None:
        """Get Server type by name

        :param name: str
               Used to get Server type by name.
        :return: :class:`BoundServerType <hcloud.server_types.client.BoundServerType>`
        """
        return self._get_first_by(name=name)
