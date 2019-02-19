# -*- coding: utf-8 -*-
from hcloud.core.domain import BaseDomain, DomainIdentityMixin


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
    """

    __slots__ = (
        "id",
        "name",
        "description",
        "country",
        "city",
        "latitude",
        "longitude"
    )

    def __init__(
            self,
            id=None,
            name=None,
            description=None,
            country=None,
            city=None,
            latitude=None,
            longitude=None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.country = country
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
