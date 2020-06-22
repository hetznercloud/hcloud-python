# -*- coding: utf-8 -*-
from dateutil.parser import isoparse

from hcloud.core.domain import BaseDomain, DomainIdentityMixin


class Certificate(BaseDomain, DomainIdentityMixin):
    """Certificate Domain

    :param id: int ID of Certificate
    :param name: str Name of Certificate
    :param certificate: str Certificate and chain in PEM format, in order so that each record directly certifies the one preceding
    :param not_valid_before: datetime
           Point in time when the Certificate becomes valid
    :param not_valid_after: datetime
           Point in time when the Certificate becomes invalid
    :param domain_names: List[str] List of domains and subdomains covered by this certificate
    :param fingerprint: str Fingerprint of the Certificate
    :param labels: dict
           User-defined labels (key-value pairs)
    :param created: datetime
           Point in time when the certificate was created
    """
    __slots__ = (
        "id",
        "name",
        "certificate",
        "not_valid_before",
        "not_valid_after",
        "domain_names",
        "fingerprint",
        "created",
        "labels",
    )

    def __init__(
            self,
            id=None,
            name=None,
            certificate=None,
            not_valid_before=None,
            not_valid_after=None,
            domain_names=None,
            fingerprint=None,
            created=None,
            labels=None,
    ):
        self.id = id
        self.name = name
        self.certificate = certificate
        self.domain_names = domain_names
        self.fingerprint = fingerprint
        self.not_valid_before = isoparse(not_valid_before) if not_valid_before else None
        self.not_valid_after = isoparse(not_valid_after) if not_valid_after else None
        self.created = isoparse(created) if created else None
        self.labels = labels
