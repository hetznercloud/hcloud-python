from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from dateutil.parser import isoparse

from ..actions import BoundAction
from ..core import BaseDomain, DomainIdentityMixin
from ..locations import BoundLocation, Location
from ..storage_box_types import BoundStorageBoxType, StorageBoxType

if TYPE_CHECKING:
    from .client import BoundStorageBox

StorageBoxStatus = Literal[
    "active",
    "initializing",
    "locked",
]


class StorageBox(BaseDomain, DomainIdentityMixin):
    """
    Storage Box Domain.

    See https://docs.hetzner.cloud/reference/hetzner#storage-boxes.
    """

    STATUS_ACTIVE = "active"
    STATUS_INITIALIZING = "initializing"
    STATUS_LOCKED = "locked"

    __api_properties__ = (
        "id",
        "name",
        "storage_box_type",
        "location",
        "system",
        "server",
        "username",
        "labels",
        "protection",
        "snapshot_plan",
        "access_settings",
        "stats",
        "status",
        "created",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        storage_box_type: BoundStorageBoxType | StorageBoxType | None = None,
        location: BoundLocation | Location | None = None,
        system: str | None = None,
        server: str | None = None,
        username: str | None = None,
        labels: dict[str, str] | None = None,
        protection: dict[str, bool] | None = None,
        snapshot_plan: StorageBoxSnapshotPlan | None = None,
        access_settings: StorageBoxAccessSettings | None = None,
        stats: StorageBoxStats | None = None,
        status: StorageBoxStatus | None = None,
        created: str | None = None,
    ):
        self.id = id
        self.name = name
        self.storage_box_type = storage_box_type
        self.location = location
        self.system = system
        self.server = server
        self.username = username
        self.labels = labels
        self.protection = protection
        self.snapshot_plan = snapshot_plan
        self.access_settings = access_settings
        self.stats = stats
        self.status = status
        self.created = isoparse(created) if created else None


class StorageBoxAccessSettings(BaseDomain):
    """
    Storage Box Access Settings Domain.
    """

    __api_properties__ = (
        "reachable_externally",
        "samba_enabled",
        "ssh_enabled",
        "webdav_enabled",
        "zfs_enabled",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        reachable_externally: bool | None = None,
        samba_enabled: bool | None = None,
        ssh_enabled: bool | None = None,
        webdav_enabled: bool | None = None,
        zfs_enabled: bool | None = None,
    ):
        self.reachable_externally = reachable_externally
        self.samba_enabled = samba_enabled
        self.ssh_enabled = ssh_enabled
        self.webdav_enabled = webdav_enabled
        self.zfs_enabled = zfs_enabled

    def to_payload(self) -> dict[str, Any]:
        """
        Generates the request payload from this domain object.
        """
        payload: dict[str, Any] = {}
        if self.reachable_externally is not None:
            payload["reachable_externally"] = self.reachable_externally
        if self.samba_enabled is not None:
            payload["samba_enabled"] = self.samba_enabled
        if self.ssh_enabled is not None:
            payload["ssh_enabled"] = self.ssh_enabled
        if self.webdav_enabled is not None:
            payload["webdav_enabled"] = self.webdav_enabled
        if self.zfs_enabled is not None:
            payload["zfs_enabled"] = self.zfs_enabled
        return payload


class StorageBoxStats(BaseDomain):
    """
    Storage Box Stats Domain.
    """

    __api_properties__ = (
        "size",
        "size_data",
        "size_snapshots",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        size: int | None = None,
        size_data: int | None = None,
        size_snapshots: int | None = None,
    ):
        self.size = size
        self.size_data = size_data
        self.size_snapshots = size_snapshots


class StorageBoxSnapshotPlan(BaseDomain):
    """
    Storage Box Snapshot Plan Domain.
    """

    __api_properties__ = (
        "max_snapshots",
        "minute",
        "hour",
        "day_of_week",
        "day_of_month",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        max_snapshots: int | None = None,
        minute: int | None = None,
        hour: int | None = None,
        day_of_week: int | None = None,
        day_of_month: int | None = None,
    ):
        self.max_snapshots = max_snapshots
        self.minute = minute
        self.hour = hour
        self.day_of_week = day_of_week
        self.day_of_month = day_of_month


class CreateStorageBoxResponse(BaseDomain):
    """
    Create Storage Box Response Domain.
    """

    __api_properties__ = (
        "storage_box",
        "action",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        storage_box: BoundStorageBox,
        action: BoundAction,
    ):
        self.storage_box = storage_box
        self.action = action


class DeleteStorageBoxResponse(BaseDomain):
    """
    Delete Storage Box Response Domain.
    """

    __api_properties__ = ("action",)
    __slots__ = __api_properties__

    def __init__(
        self,
        action: BoundAction,
    ):
        self.action = action


class StorageBoxFoldersResponse(BaseDomain):
    """
    Storage Box Folders Response Domain.
    """

    __api_properties__ = ("folders",)
    __slots__ = __api_properties__

    def __init__(
        self,
        folders: list[str],
    ):
        self.folders = folders
