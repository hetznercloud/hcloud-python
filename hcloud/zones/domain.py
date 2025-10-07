from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

from dateutil.parser import isoparse

from ..core import BaseDomain, DomainIdentityMixin

if TYPE_CHECKING:
    from ..actions import BoundAction
    from .client import BoundZone, BoundZoneRRSet


ZoneMode = Literal["primary", "secondary"]
ZoneStatus = Literal["ok", "updating", "error"]
ZoneRegistrar = Literal["hetzner", "other", "unknown"]


class Zone(BaseDomain, DomainIdentityMixin):
    """
    Zone Domain.

    See https://docs.hetzner.cloud/reference/cloud#zones.
    """

    MODE_PRIMARY = "primary"
    """
    Zone in primary mode, resource record sets (RRSets) and resource records (RRs) are
    managed via the Cloud API or Cloud Console.
    """
    MODE_SECONDARY = "secondary"
    """
    Zone in secondary mode, Hetzner's nameservers query RRSets and RRs from given
    primary nameservers via AXFR.
    """

    STATUS_OK = "ok"
    """The Zone is pushed to the authoritative nameservers."""
    STATUS_UPDATING = "updating"
    """The Zone is currently being published to the authoritative nameservers."""
    STATUS_ERROR = "error"
    """The Zone could not be published to the authoritative nameservers."""

    REGISTRAR_HETZNER = "hetzner"
    REGISTRAR_OTHER = "other"
    REGISTRAR_UNKNOWN = "unknown"

    __api_properties__ = (
        "id",
        "name",
        "created",
        "mode",
        "ttl",
        "labels",
        "protection",
        "status",
        "record_count",
        "registrar",
        "primary_nameservers",
        "authoritative_nameservers",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        created: str | None = None,
        mode: ZoneMode | None = None,
        ttl: int | None = None,
        labels: dict[str, str] | None = None,
        protection: ZoneProtection | None = None,
        status: ZoneStatus | None = None,
        record_count: int | None = None,
        registrar: ZoneRegistrar | None = None,
        primary_nameservers: list[ZonePrimaryNameserver] | None = None,
        authoritative_nameservers: ZoneAuthoritativeNameservers | None = None,
    ):
        self.id = id
        self.name = name
        self.created = isoparse(created) if created else None
        self.mode = mode
        self.ttl = ttl
        self.labels = labels
        self.protection = protection
        self.status = status
        self.record_count = record_count
        self.registrar = registrar
        self.primary_nameservers = primary_nameservers
        self.authoritative_nameservers = authoritative_nameservers


ZonePrimaryNameserverTSIGAlgorithm = Literal[
    "hmac-md5",
    "hmac-sha1",
    "hmac-sha256",
]


class ZonePrimaryNameserver(BaseDomain):
    """
    Zone Primary Nameserver Domain.
    """

    TSIG_ALGORITHM_HMAC_MD5 = "hmac-md5"
    """Transaction signature (TSIG) algorithm used to generate the TSIG key."""
    TSIG_ALGORITHM_HMAC_SHA1 = "hmac-sha1"
    """Transaction signature (TSIG) algorithm used to generate the TSIG key."""
    TSIG_ALGORITHM_HMAC_SHA256 = "hmac-sha256"
    """Transaction signature (TSIG) algorithm used to generate the TSIG key."""

    __api_properties__ = (
        "address",
        "port",
        "tsig_algorithm",
        "tsig_key",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        address: str,
        port: int | None = None,
        tsig_algorithm: ZonePrimaryNameserverTSIGAlgorithm | None = None,
        tsig_key: str | None = None,
    ):
        self.address = address
        self.port = port
        self.tsig_algorithm = tsig_algorithm
        self.tsig_key = tsig_key

    def to_payload(self) -> dict[str, Any]:
        """
        Generates the request payload from this domain object.
        """
        payload: dict[str, Any] = {
            "address": self.address,
        }
        if self.port is not None:
            payload["port"] = self.port
        if self.tsig_algorithm is not None:
            payload["tsig_algorithm"] = self.tsig_algorithm
        if self.tsig_key is not None:
            payload["tsig_key"] = self.tsig_key

        return payload


ZoneAuthoritativeNameserversDelegationStatus = Literal[
    "valid",
    "partially-valid",
    "invalid",
    "lame",
    "unregistered",
    "unknown",
]


class ZoneAuthoritativeNameservers(BaseDomain):
    """
    Zone Authoritative Nameservers Domain.
    """

    DELEGATION_STATUS_VALID = "valid"
    DELEGATION_STATUS_PARTIALLY_VALID = "partially-valid"
    DELEGATION_STATUS_INVALID = "invalid"
    DELEGATION_STATUS_LAME = "lame"
    DELEGATION_STATUS_UNREGISTERED = "unregistered"
    DELEGATION_STATUS_UNKNOWN = "unknown"

    __api_properties__ = (
        "assigned",
        "delegated",
        "delegation_last_check",
        "delegation_status",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        assigned: list[str] | None = None,
        delegated: list[str] | None = None,
        delegation_last_check: str | None = None,
        delegation_status: ZoneAuthoritativeNameserversDelegationStatus | None = None,
    ):
        self.assigned = assigned
        self.delegated = delegated
        self.delegation_last_check = (
            isoparse(delegation_last_check)
            if delegation_last_check is not None
            else None
        )
        self.delegation_status = delegation_status


class ZoneProtection(TypedDict):
    """
    Zone Protection.
    """

    delete: bool


class CreateZoneResponse(BaseDomain):
    """
    Create Zone Response Domain.
    """

    __api_properties__ = ("zone", "action")
    __slots__ = __api_properties__

    def __init__(
        self,
        zone: BoundZone,
        action: BoundAction,
    ):
        self.zone = zone
        self.action = action


class DeleteZoneResponse(BaseDomain):
    """
    Delete Zone Response Domain.
    """

    __api_properties__ = ("action",)
    __slots__ = __api_properties__

    def __init__(
        self,
        action: BoundAction,
    ):
        self.action = action


class ExportZonefileResponse(BaseDomain):
    """
    Export Zonefile Response Domain.
    """

    __api_properties__ = ("zonefile",)
    __slots__ = __api_properties__

    def __init__(
        self,
        zonefile: str,
    ):
        self.zonefile = zonefile


ZoneRRSetType = Literal[
    "A",
    "AAAA",
    "CAA",
    "CNAME",
    "DS",
    "HINFO",
    "HTTPS",
    "MX",
    "NS",
    "PTR",
    "RP",
    "SOA",
    "SRV",
    "SVCB",
    "TLSA",
    "TXT",
]


class ZoneRRSet(BaseDomain):
    """
    Zone RRSet Domain.

    See https://docs.hetzner.cloud/reference/cloud#zone-rrsets
    """

    TYPE_A = "A"
    TYPE_AAAA = "AAAA"
    TYPE_CAA = "CAA"
    TYPE_CNAME = "CNAME"
    TYPE_DS = "DS"
    TYPE_HINFO = "HINFO"
    TYPE_HTTPS = "HTTPS"
    TYPE_MX = "MX"
    TYPE_NS = "NS"
    TYPE_PTR = "PTR"
    TYPE_RP = "RP"
    TYPE_SOA = "SOA"
    TYPE_SRV = "SRV"
    TYPE_SVCB = "SVCB"
    TYPE_TLSA = "TLSA"
    TYPE_TXT = "TXT"

    __api_properties__ = (
        "name",
        "type",
        "ttl",
        "labels",
        "protection",
        "records",
        "id",
        "zone",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        name: str | None = None,
        type: ZoneRRSetType | None = None,
        ttl: int | None = None,
        labels: dict[str, str] | None = None,
        protection: ZoneRRSetProtection | None = None,
        records: list[ZoneRecord] | None = None,
        id: str | None = None,
        zone: BoundZone | Zone | None = None,
    ):
        # Ensure that 'id', 'name' and 'type' are always populated.
        if name is not None and type is not None:
            if id is None:
                id = f"{name}/{type}"
        else:
            if id is not None:
                name, _, type = id.partition("/")  # type: ignore[assignment]
            else:
                raise ValueError("id or name and type must be set")

        self.name = name
        self.type = type
        self.ttl = ttl
        self.labels = labels
        self.protection = protection
        self.records = records

        self.id = id
        self.zone = zone

    def to_payload(self) -> dict[str, Any]:
        """
        Generates the request payload from this domain object.
        """
        payload: dict[str, Any] = {
            "name": self.name,
            "type": self.type,
        }
        if self.ttl is not None:
            payload["ttl"] = self.ttl
        if self.labels is not None:
            payload["labels"] = self.labels
        if self.protection is not None:
            payload["protection"] = self.protection
        if self.records is not None:
            payload["records"] = [o.to_payload() for o in self.records]

        return payload


class ZoneRRSetProtection(TypedDict):
    """
    Zone RRSet Protection.
    """

    change: bool


class ZoneRecord(BaseDomain):
    """
    Zone Record Domain.
    """

    __api_properties__ = (
        "value",
        "comment",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        value: str,
        comment: str | None = None,
    ):
        self.value = value
        self.comment = comment

    def to_payload(self) -> dict[str, Any]:
        """
        Generates the request payload from this domain object.
        """
        payload: dict[str, Any] = {
            "value": self.value,
        }
        if self.comment is not None:
            payload["comment"] = self.comment

        return payload


class CreateZoneRRSetResponse(BaseDomain):
    """
    Create Zone RRSet Response Domain.
    """

    __api_properties__ = (
        "rrset",
        "action",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        rrset: BoundZoneRRSet,
        action: BoundAction,
    ):
        self.rrset = rrset
        self.action = action


class DeleteZoneRRSetResponse(BaseDomain):
    """
    Delete Zone RRSet Response Domain.
    """

    __api_properties__ = ("action",)
    __slots__ = __api_properties__

    def __init__(
        self,
        action: BoundAction,
    ):
        self.action = action
