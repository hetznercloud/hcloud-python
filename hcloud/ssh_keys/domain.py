# -*- coding: utf-8 -*-
from hcloud.core.domain import BaseDomain, DomainIdentityMixin

from hcloud.helpers.descriptors import ISODateTime


class SSHKey(BaseDomain, DomainIdentityMixin):
    """SSHKey Domain

    :param id: int
           ID of the SSH key
    :param name: str
           Name of the SSH key (must be unique per project)
    :param fingerprint: str
           Fingerprint of public key
    :param public_key: str
           Public Key
    :param labels: Dict
            User-defined labels (key-value pairs)
    :param created: datetime
           Point in time when the SSH Key was created
    """
    __slots__ = (
        "id",
        "name",
        "fingerprint",
        "public_key",
        "labels"
    )

    created = ISODateTime()
    supported_fields = ("created",)

    def __init__(
        self,
        id=None,
        name=None,
        fingerprint=None,
        public_key=None,
        labels=None,
        created=None
    ):
        self.id = id
        self.name = name
        self.fingerprint = fingerprint
        self.public_key = public_key
        self.labels = labels
        self.created = created
