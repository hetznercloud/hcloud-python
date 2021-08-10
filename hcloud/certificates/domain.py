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
    :param type: str Type of Certificate
    :param status: ManagedCertificateStatus Current status of a type managed Certificate, always none for type uploaded Certificates
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
        "type",
        "status",
    )
    TYPE_UPLOADED = "uploaded"
    TYPE_MANAGED = "managed"

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
        type=None,
        status=None,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.certificate = certificate
        self.domain_names = domain_names
        self.fingerprint = fingerprint
        self.not_valid_before = isoparse(not_valid_before) if not_valid_before else None
        self.not_valid_after = isoparse(not_valid_after) if not_valid_after else None
        self.created = isoparse(created) if created else None
        self.labels = labels
        self.status = status


class ManagedCertificateStatus(BaseDomain):
    """ManagedCertificateStatus Domain

    :param issuance: str
           Status of the issuance process of the Certificate
    :param renewal: str
           Status of the renewal process of the Certificate
    :param error: ManagedCertificateError
          If issuance or renewal reports failure, this property contains information about what happened
    """

    def __init__(self, issuance=None, renewal=None, error=None):
        self.issuance = issuance
        self.renewal = renewal
        self.error = error


class ManagedCertificateError(BaseDomain):
    """ManagedCertificateError Domain

    :param code: str
        Error code identifying the error
    :param message:
        Message detailing the error
    """

    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message


class CreateManagedCertificateResponse(BaseDomain):
    """Create Managed Certificate Response Domain

    :param certificate: :class:`BoundCertificate <hcloud.certificate.client.BoundCertificate>`
           The created server
    :param action: :class:`BoundAction <hcloud.actions.client.BoundAction>`
           Shows the progress of the certificate creation
    """

    __slots__ = (
        "certificate",
        "action",
    )

    def __init__(
        self,
        certificate,  # type: BoundCertificate
        action,  # type: BoundAction
    ):
        self.certificate = certificate
        self.action = action
