# -*- coding: utf-8 -*-
from dateutil.parser import isoparse

from hcloud.core.domain import BaseDomain, DomainIdentityMixin


class Iso(BaseDomain, DomainIdentityMixin):
    """Iso Domain

    :param id: int
           ID of the ISO
    :param name: str, None
           Unique identifier of the ISO. Only set for public ISOs
    :param description: str
           Description of the ISO
    :param type: str
           Type of the ISO. Choices: `public`, `private`
    :param deprecated: datetime, None
           ISO 8601 timestamp of deprecation, None if ISO is still available. After the deprecation time it will no longer be possible to attach the ISO to servers.
    """

    __slots__ = ("id", "name", "type", "description", "deprecated")

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
        self.deprecated = isoparse(deprecated) if deprecated else None
