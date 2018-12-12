# -*- coding: utf-8 -*-
from hcloud.core.domain import BaseDomain
from hcloud.helpers.descriptors import ISODateTime


class Iso(BaseDomain):
    deprecated = ISODateTime()

    __slots__ = (
        "id",
        "name",
        "type",
        "description"
    )

    def __init__(
        self,
        id=None,
        name=None,
        type=None,
        description=None,
        deprecated=None,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.description = description
        self.deprecated = deprecated
