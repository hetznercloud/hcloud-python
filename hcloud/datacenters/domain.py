from __future__ import annotations

from typing import TYPE_CHECKING

from ..core import BaseDomain, DomainIdentityMixin

if TYPE_CHECKING:
    from ..locations import Location
    from ..server_types import BoundServerType


class Datacenter(BaseDomain, DomainIdentityMixin):
    """Datacenter Domain

    :param id: int ID of Datacenter
    :param name: str Name of Datacenter
    :param description: str Description of Datacenter
    :param location: :class:`BoundLocation <hcloud.locations.client.BoundLocation>`
    :param server_types: :class:`DatacenterServerTypes <hcloud.datacenters.domain.DatacenterServerTypes>`
    """

    __api_properties__ = ("id", "name", "description", "location", "server_types")
    __slots__ = __api_properties__

    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        description: str | None = None,
        location: Location | None = None,
        server_types: DatacenterServerTypes | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.location = location
        self.server_types = server_types


class DatacenterServerTypes(BaseDomain):
    """DatacenterServerTypes Domain

    :param available: List[:class:`BoundServerTypes <hcloud.server_types.client.BoundServerTypes>`]
           All available server types for this datacenter
    :param supported: List[:class:`BoundServerTypes <hcloud.server_types.client.BoundServerTypes>`]
           All supported server types for this datacenter
    :param available_for_migration: List[:class:`BoundServerTypes <hcloud.server_types.client.BoundServerTypes>`]
           All available for migration (change type) server types for this datacenter
    """

    __api_properties__ = ("available", "supported", "available_for_migration")
    __slots__ = __api_properties__

    def __init__(
        self,
        available: list[BoundServerType],
        supported: list[BoundServerType],
        available_for_migration: list[BoundServerType],
    ):
        self.available = available
        self.supported = supported
        self.available_for_migration = available_for_migration
