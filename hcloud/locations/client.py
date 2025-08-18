from __future__ import annotations

from typing import Any, NamedTuple

from ..core import BoundModelBase, Meta, ResourceClientBase
from .domain import Location


class BoundLocation(BoundModelBase, Location):
    _client: LocationsClient

    model = Location


class LocationsPageResult(NamedTuple):
    locations: list[BoundLocation]
    meta: Meta


class LocationsClient(ResourceClientBase):
    _base_url = "/locations"

    def get_by_id(self, id: int) -> BoundLocation:
        """Get a specific location by its ID.

        :param id: int
        :return: :class:`BoundLocation <hcloud.locations.client.BoundLocation>`
        """
        response = self._client.request(url=f"{self._base_url}/{id}", method="GET")
        return BoundLocation(self, response["location"])

    def get_list(
        self,
        name: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> LocationsPageResult:
        """Get a list of locations

        :param name: str (optional)
               Can be used to filter locations by their name.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundLocation <hcloud.locations.client.BoundLocation>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url=self._base_url, method="GET", params=params)
        locations = [
            BoundLocation(self, location_data)
            for location_data in response["locations"]
        ]
        return LocationsPageResult(locations, Meta.parse_meta(response))

    def get_all(self, name: str | None = None) -> list[BoundLocation]:
        """Get all locations

        :param name: str (optional)
               Can be used to filter locations by their name.
        :return: List[:class:`BoundLocation <hcloud.locations.client.BoundLocation>`]
        """
        return self._iter_pages(self.get_list, name=name)

    def get_by_name(self, name: str) -> BoundLocation | None:
        """Get location by name

        :param name: str
               Used to get location by name.
        :return: :class:`BoundLocation <hcloud.locations.client.BoundLocation>`
        """
        return self._get_first_by(name=name)
