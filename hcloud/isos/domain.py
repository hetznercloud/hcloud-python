from __future__ import annotations

from datetime import datetime
from warnings import warn

from ..core import BaseDomain, DomainIdentityMixin
from ..deprecation import DeprecationInfo


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
           ISO 8601 timestamp of deprecation, None if ISO is still available. After the deprecation time it will no longer be possible to attach the ISO to servers. This field is deprecated. Use `deprecation` instead.
    :param deprecation: :class:`DeprecationInfo <hcloud.deprecation.domain.DeprecationInfo>`, None
        Describes if, when & how the resources was deprecated. If this field is set to None the resource is not
        deprecated. If it has a value, it is considered deprecated.
    """

    __api_properties__ = (
        "id",
        "name",
        "type",
        "architecture",
        "description",
        "deprecation",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        type: str | None = None,
        architecture: str | None = None,
        description: str | None = None,
        deprecated: str | None = None,  # pylint: disable=unused-argument
        deprecation: dict | None = None,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.architecture = architecture
        self.description = description
        self.deprecation = (
            DeprecationInfo.from_dict(deprecation) if deprecation is not None else None
        )

    @property
    def deprecated(self) -> datetime | None:
        """
        ISO 8601 timestamp of deprecation, None if ISO is still available.
        """
        warn(
            "The `deprecated` field is deprecated, please use the `deprecation` field instead.",
            DeprecationWarning,
        )
        if self.deprecation is None:
            return None
        return self.deprecation.unavailable_after
