from __future__ import annotations

from typing import TYPE_CHECKING

from dateutil.parser import isoparse

from ..core import BaseDomain, DomainIdentityMixin

if TYPE_CHECKING:
    from ..actions import BoundAction
    from ..servers import BoundServer, Server
    from .client import BoundImage


class Image(BaseDomain, DomainIdentityMixin):
    """Image Domain

    :param id: int
           ID of the image
    :param type: str
           Type of the image Choices: `system`, `snapshot`, `backup`, `app`
    :param status: str
           Whether the image can be used or if it’s still being created Choices: `available`, `creating`
    :param name: str, None
           Unique identifier of the image. This value is only set for system images.
    :param description: str
           Description of the image
    :param image_size: number, None
           Size of the image file in our storage in GB. For snapshot images this is the value relevant for calculating costs for the image.
    :param disk_size: number
           Size of the disk contained in the image in GB.
    :param created: datetime
           Point in time when the image was created
    :param created_from: :class:`BoundServer <hcloud.servers.client.BoundServer>`, None
           Information about the server the image was created from
    :param bound_to: :class:`BoundServer <hcloud.servers.client.BoundServer>`, None
           ID of server the image is bound to. Only set for images of type `backup`.
    :param os_flavor: str
           Flavor of operating system contained in the image Choices: `ubuntu`, `centos`, `debian`, `fedora`, `unknown`
    :param os_version: str, None
           Operating system version
    :param architecture: str
           CPU Architecture that the image is compatible with. Choices: `x86`, `arm`
    :param rapid_deploy: bool
           Indicates that rapid deploy of the image is available
    :param protection: dict
           Protection configuration for the image
    :param deprecated: datetime, None
           Point in time when the image is considered to be deprecated (in ISO-8601 format)
    :param labels: Dict
            User-defined labels (key-value pairs)
    """

    __api_properties__ = (
        "id",
        "name",
        "type",
        "description",
        "image_size",
        "disk_size",
        "bound_to",
        "os_flavor",
        "os_version",
        "architecture",
        "rapid_deploy",
        "created_from",
        "status",
        "protection",
        "labels",
        "created",
        "deprecated",
    )
    __slots__ = __api_properties__

    # pylint: disable=too-many-locals
    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        type: str | None = None,
        created: str | None = None,
        description: str | None = None,
        image_size: int | None = None,
        disk_size: int | None = None,
        deprecated: str | None = None,
        bound_to: Server | BoundServer | None = None,
        os_flavor: str | None = None,
        os_version: str | None = None,
        architecture: str | None = None,
        rapid_deploy: bool | None = None,
        created_from: Server | BoundServer | None = None,
        protection: dict | None = None,
        labels: dict[str, str] | None = None,
        status: str | None = None,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.created = isoparse(created) if created else None
        self.description = description
        self.image_size = image_size
        self.disk_size = disk_size
        self.deprecated = isoparse(deprecated) if deprecated else None
        self.bound_to = bound_to
        self.os_flavor = os_flavor
        self.os_version = os_version
        self.architecture = architecture
        self.rapid_deploy = rapid_deploy
        self.created_from = created_from
        self.protection = protection
        self.labels = labels
        self.status = status


class CreateImageResponse(BaseDomain):
    """Create Image Response Domain

    :param image: :class:`BoundImage <hcloud.images.client.BoundImage>`
           The Image which was created
    :param action: :class:`BoundAction <hcloud.actions.client.BoundAction>`
           The Action which shows the progress of the Floating IP Creation
    """

    __api_properties__ = ("action", "image")
    __slots__ = __api_properties__

    def __init__(
        self,
        action: BoundAction,
        image: BoundImage,
    ):
        self.action = action
        self.image = image
