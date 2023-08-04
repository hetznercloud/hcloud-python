from __future__ import annotations

from dateutil.parser import isoparse

from ..core import BaseDomain, DomainIdentityMixin


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
    :param architecture: str, None
           CPU Architecture that the ISO is compatible with. None means that the compatibility is unknown. Choices: `x86`, `arm`
    :param deprecated: datetime, None
           ISO 8601 timestamp of deprecation, None if ISO is still available. After the deprecation time it will no longer be possible to attach the ISO to servers.
    """

    __slots__ = ("id", "name", "type", "architecture", "description", "deprecated")

    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        type: str | None = None,
        architecture: str | None = None,
        description: str | None = None,
        deprecated: str | None = None,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.architecture = architecture
        self.description = description
        self.deprecated = isoparse(deprecated) if deprecated else None
