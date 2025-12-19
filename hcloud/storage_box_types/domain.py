from __future__ import annotations

from typing import Any

from ..core import BaseDomain, DomainIdentityMixin
from ..deprecation import DeprecationInfo

__all__ = [
    "StorageBoxType",
]


class StorageBoxType(BaseDomain, DomainIdentityMixin):
    """
    Storage Box Type Domain.

    See https://docs.hetzner.cloud/reference/hetzner#storage-box-types.
    """

    __api_properties__ = (
        "id",
        "name",
        "description",
        "snapshot_limit",
        "automatic_snapshot_limit",
        "subaccounts_limit",
        "size",
        "deprecation",
        "prices",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        description: str | None = None,
        snapshot_limit: int | None = None,
        automatic_snapshot_limit: int | None = None,
        subaccounts_limit: int | None = None,
        size: int | None = None,
        prices: list[dict[str, Any]] | None = None,
        deprecation: dict[str, Any] | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.snapshot_limit = snapshot_limit
        self.automatic_snapshot_limit = automatic_snapshot_limit
        self.subaccounts_limit = subaccounts_limit
        self.size = size
        self.prices = prices
        self.deprecation = (
            DeprecationInfo.from_dict(deprecation) if deprecation is not None else None
        )
