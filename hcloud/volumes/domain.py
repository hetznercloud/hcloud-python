# -*- coding: utf-8 -*-
from hcloud.core.domain import BaseDomain
from hcloud.helpers.descriptors import ISODateTime


class Volume(BaseDomain):
    created = ISODateTime()

    __slots__ = (
        "id",
        "name",
        "server",
        "location",
        "size",
        "linux_device",
        "protection",
        "labels",
        "status"
    )

    def __init__(
        self,
        id,
        name=None,
        server=None,
        created=None,
        location=None,
        size=None,
        linux_device=None,
        protection=None,
        labels=None,
        status=None

    ):
        self.id = id
        self.name = name
        self.server = server
        self.created = created
        self.location = location
        self.size = size
        self.linux_device = linux_device
        self.protection = protection
        self.labels = labels
        self.status = status


class CreateVolumeResponse(BaseDomain):
    __slots__ = (
        "volume",
        "action",
        "next_actions"
    )

    def __init__(
            self,
            volume,          # type: BoundVolume
            action,          # type: Action
            next_actions,    # type: List[Action]
    ):
        self.volume = volume
        self.action = action
        self.next_actions = next_actions
