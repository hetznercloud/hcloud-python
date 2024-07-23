from __future__ import annotations

from ..core import BaseDomain, DomainIdentityMixin


class Location(BaseDomain, DomainIdentityMixin):
    """Location Domain

    :param id: int
           ID of location
    :param name: str
           Name of location
    :param description: str
           Description of location
    :param country: str
           ISO 3166-1 alpha-2 code of the country the location resides in
    :param city: str
           City the location is closest to
    :param latitude: float
           Latitude of the city closest to the location
    :param longitude: float
           Longitude of the city closest to the location
    :param network_zone: str
           Name of network zone this location resides in
    """

    __api_properties__ = (
        "id",
        "name",
        "description",
        "country",
        "city",
        "latitude",
        "longitude",
        "network_zone",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        description: str | None = None,
        country: str | None = None,
        city: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        network_zone: str | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.country = country
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.network_zone = network_zone
