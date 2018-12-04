# -*- coding: utf-8 -*-
from hcloud.core.domain import BaseDomain


class ServerType(BaseDomain):

    __slots__ = (
        "id",
        "name",
        "description",
        "cores",
        "memory",
        "disk",
        "prices",
        "storage_type",
        "cpu_type"
    )

    def __init__(
        self,
        id=None,
        name=None,
        description=None,
        cores=None,
        memory=None,
        disk=None,
        prices=None,
        storage_type=None,
        cpu_type=None

    ):
        self.id = id
        self.name = name
        self.description = description
        self.cores = cores
        self.memory = memory
        self.disk = disk
        self.prices = prices
        self.storage_type = storage_type
        self.cpu_type = cpu_type
