from __future__ import annotations

from dateutil.parser import isoparse

from ..core import BaseDomain, DomainIdentityMixin


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

    __api_properties__ = (
        "id",
        "name",
        "fingerprint",
        "public_key",
        "labels",
        "created",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        fingerprint: str | None = None,
        public_key: str | None = None,
        labels: dict[str, str] | None = None,
        created: str | None = None,
    ):
        self.id = id
        self.name = name
        self.fingerprint = fingerprint
        self.public_key = public_key
        self.labels = labels
        self.created = isoparse(created) if created else None
