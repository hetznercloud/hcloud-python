# -*- coding: utf-8 -*-
from hcloud.core.domain import BaseDomain, DomainIdentityMixin


class Datacenter(BaseDomain, DomainIdentityMixin):
    """Datacenter Domain

    :param id: int ID of Datacenter
    :param name: str Name of Datacenter
    :param description: str Description of Datacenter
    :param location: :class:`BoundLocation <hcloud.locations.client.BoundLocation>`
    :param server_types: :class:`DatacenterServerTypes <hcloud.datacenters.domain.DatacenterServerTypes>`
    """

    __slots__ = (
        "id",
        "name",
        "description",
        "location",
        "server_types",
    )

    def __init__(
        self, id=None, name=None, description=None, location=None, server_types=None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.location = location
        self.server_types = server_types


class DatacenterServerTypes:
    """DatacenterServerTypes Domain

    :param available: List[:class:`BoundServerTypes <hcloud.server_types.client.BoundServerTypes>`]
           All available server types for this datacenter
    :param supported: List[:class:`BoundServerTypes <hcloud.server_types.client.BoundServerTypes>`]
           All supported server types for this datacenter
    :param available_for_migration: List[:class:`BoundServerTypes <hcloud.server_types.client.BoundServerTypes>`]
           All available for migration (change type) server types for this datacenter
    """

    __slots__ = ("available", "supported", "available_for_migration")

    def __init__(self, available, supported, available_for_migration):
        self.available = available
        self.supported = supported
        self.available_for_migration = available_for_migration
