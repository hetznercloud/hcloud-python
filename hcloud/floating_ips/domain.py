# -*- coding: utf-8 -*-
from hcloud.core.domain import BaseDomain


class FloatingIP(BaseDomain):

    __slots__ = (
        "id",
        "type",
        "description",
        "ip",
        "server",
        "dns_ptr",
        "home_location",
        "blocked",
        "protection",
        "labels"
    )

    def __init__(
        self,
        id=None,
        type=None,
        description=None,
        ip=None,
        server=None,
        dns_ptr=None,
        home_location=None,
        blocked=None,
        protection=None,
        labels=None

    ):
        self.id = id
        self.type = type
        self.description = description
        self.ip = ip
        self.server = server
        self.dns_ptr = dns_ptr
        self.home_location = home_location
        self.blocked = blocked
        self.protection = protection
        self.labels = labels


class CreateFloatingIPResponse(BaseDomain):
    __slots__ = (
        "floating_ip",
        "action"
    )

    def __init__(
            self,
            floating_ip,     # type: BoundFloatingIP
            action,          # type: BoundAction
    ):
        self.floating_ip = floating_ip
        self.action = action
