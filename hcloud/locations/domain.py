# -*- coding: utf-8 -*-
from hcloud.core.domain import BaseDomain


class Location(BaseDomain):

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
