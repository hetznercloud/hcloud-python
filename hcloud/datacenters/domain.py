# -*- coding: utf-8 -*-
from hcloud.core.domain import BaseDomain, DomainIdentityMixin


class Datacenter(BaseDomain, DomainIdentityMixin):

    __slots__ = (
        "id",
        "name",
        "description",
        "location",
        "server_types",
    )

    def __init__(
        self,
        id=None,
        name=None,
        description=None,
        location=None,
        server_types=None
    ):
        self.id = id
        """ID of Datacenter"""
        self.name = name
        self.description = description
        self.location = location
        self.server_types = server_types


class DatacenterServerTypes:
    __slots__ = (
        "available",
        "supported",
        "available_for_migration"
    )

    def __init__(self, available, supported, available_for_migration):
        self.available = available
        self.supported = supported
        self.available_for_migration = available_for_migration
