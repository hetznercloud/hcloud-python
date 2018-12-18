# -*- coding: utf-8 -*-
from hcloud.core.domain import BaseDomain


class SSHKey(BaseDomain):

    __slots__ = (
        "id",
        "name",
        "fingerprint",
        "public_key",
        "labels"
    )

    def __init__(
        self,
        id=None,
        name=None,
        fingerprint=None,
        public_key=None,
        labels=None
    ):
        self.id = id
        self.name = name
        self.fingerprint = fingerprint
        self.public_key = public_key
        self.labels = labels
