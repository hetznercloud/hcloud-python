from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from ..core.client import BoundModelBase, ClientEntityBase, GetEntityByNameMixin
from ..core.domain import Meta
from .domain import Location

if TYPE_CHECKING:
    from .._client import Client


class BoundLocation(BoundModelBase):
    _client: LocationsClient

    model = Location


class LocationsPageResult(NamedTuple):
    locations: list[BoundLocation]
    meta: Meta | None


class LocationsClient(ClientEntityBase, GetEntityByNameMixin):
    _client: Client

    def get_by_id(self, id):
        # type: (int) -> locations.client.BoundLocation
        """Get a specific location by its ID.

        :param id: int
        :return: :class:`BoundLocation <hcloud.locations.client.BoundLocation>`
        """
        response = self._client.request(url=f"/locations/{id}", method="GET")
        return BoundLocation(self, response["location"])

    def get_list(self, name=None, page=None, per_page=None):
        # type: (Optional[str], Optional[int], Optional[int]) -> PageResult[List[BoundLocation], Meta]
        """Get a list of locations

        :param name: str (optional)
               Can be used to filter locations by their name.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundLocation <hcloud.locations.client.BoundLocation>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params = {}
        if name is not None:
            params["name"] = name
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url="/locations", method="GET", params=params)
        locations = [
            BoundLocation(self, location_data)
            for location_data in response["locations"]
        ]
        return LocationsPageResult(locations, Meta.parse_meta(response))

    def get_all(self, name=None):
        # type: (Optional[str]) -> List[BoundLocation]
        """Get all locations

        :param name: str (optional)
               Can be used to filter locations by their name.
        :return: List[:class:`BoundLocation <hcloud.locations.client.BoundLocation>`]
        """
        return super().get_all(name=name)

    def get_by_name(self, name):
        # type: (str) -> BoundLocation
        """Get location by name

        :param name: str
               Used to get location by name.
        :return: :class:`BoundLocation <hcloud.locations.client.BoundLocation>`
        """
        return super().get_by_name(name)
