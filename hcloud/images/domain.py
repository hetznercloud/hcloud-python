# -*- coding: utf-8 -*-
from hcloud.core.domain import BaseDomain
from hcloud.helpers.descriptors import ISODateTime


class Image(BaseDomain):
    created = ISODateTime()
    deprecated = ISODateTime()

    __slots__ = (
        "id",
        "name",
        "type",
        "description",
        "image_size",
        "disk_size",
        "bound_to",
        "os_flavor",
        "os_version",
        "rapid_deploy",
        "created_from",
        "status",
        "protection",
        "labels"
    )

    def __init__(
        self,
        id=None,
        name=None,
        type=None,
        created=None,
        description=None,
        image_size=None,
        disk_size=None,
        deprecated=None,
        bound_to=None,
        os_flavor=None,
        os_version=None,
        rapid_deploy=None,
        created_from=None,
        protection=None,
        labels=None,
        status=None

    ):
        self.id = id
        self.name = name
        self.type = type
        self.created = created
        self.description = description
        self.image_size = image_size
        self.disk_size = disk_size
        self.deprecated = deprecated
        self.bound_to = bound_to
        self.os_flavor = os_flavor
        self.os_version = os_version
        self.rapid_deploy = rapid_deploy
        self.created_from = created_from
        self.protection = protection
        self.labels = labels
        self.status = status


class CreateImageResponse(BaseDomain):
    __slots__ = (
        "action",
        "image"
    )

    def __init__(
            self,
            action,  # type: BoundAction
            image    # type: BoundImage
    ):
        self.action = action
        self.image = image
