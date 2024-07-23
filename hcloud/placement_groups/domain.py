from __future__ import annotations

from typing import TYPE_CHECKING

from dateutil.parser import isoparse

from ..core import BaseDomain, DomainIdentityMixin

if TYPE_CHECKING:
    from ..actions import BoundAction
    from .client import BoundPlacementGroup


class PlacementGroup(BaseDomain, DomainIdentityMixin):
    """Placement Group Domain

    :param id: int
           ID of the Placement Group
    :param name: str
           Name of the Placement Group
    :param labels: dict
           User-defined labels (key-value pairs)
    :param servers: List[ int ]
           List of server IDs assigned to the Placement Group
    :param type: str
           Type of the Placement Group
    :param created: datetime
           Point in time when the image was created
    """

    __api_properties__ = ("id", "name", "labels", "servers", "type", "created")
    __slots__ = __api_properties__

    """Placement Group type spread
       spreads all servers in the group on different vhosts
    """
    TYPE_SPREAD = "spread"

    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        labels: dict[str, str] | None = None,
        servers: list[int] | None = None,
        type: str | None = None,
        created: str | None = None,
    ):
        self.id = id
        self.name = name
        self.labels = labels
        self.servers = servers
        self.type = type
        self.created = isoparse(created) if created else None


class CreatePlacementGroupResponse(BaseDomain):
    """Create Placement Group Response Domain

    :param placement_group: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>`
           The Placement Group which was created
    :param action: :class:`BoundAction <hcloud.actions.client.BoundAction>`
           The Action which shows the progress of the Placement Group Creation
    """

    __api_properties__ = ("placement_group", "action")
    __slots__ = __api_properties__

    def __init__(
        self,
        placement_group: BoundPlacementGroup,
        action: BoundAction | None,
    ):
        self.placement_group = placement_group
        self.action = action
