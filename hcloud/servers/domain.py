from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from dateutil.parser import isoparse

from ..core import BaseDomain, DomainIdentityMixin

if TYPE_CHECKING:
    from ..actions import BoundAction
    from ..datacenters import BoundDatacenter
    from ..firewalls import BoundFirewall
    from ..floating_ips import BoundFloatingIP
    from ..images import BoundImage
    from ..isos import BoundIso
    from ..metrics import Metrics
    from ..networks import BoundNetwork
    from ..placement_groups import BoundPlacementGroup
    from ..primary_ips import BoundPrimaryIP, PrimaryIP
    from ..server_types import BoundServerType
    from ..volumes import BoundVolume
    from .client import BoundServer


class Server(BaseDomain, DomainIdentityMixin):
    """Server Domain

    :param id: int
           ID of the server
    :param name: str
           Name of the server (must be unique per project and a valid hostname as per RFC 1123)
    :param status: str
           Status of the server Choices: `running`, `initializing`, `starting`, `stopping`, `off`, `deleting`, `migrating`, `rebuilding`, `unknown`
    :param created: datetime
           Point in time when the server was created
    :param public_net: :class:`PublicNetwork <hcloud.servers.domain.PublicNetwork>`
           Public network information.
    :param server_type: :class:`BoundServerType <hcloud.server_types.client.BoundServerType>`
    :param datacenter: :class:`BoundDatacenter <hcloud.datacenters.client.BoundDatacenter>`
    :param image: :class:`BoundImage <hcloud.images.client.BoundImage>`, None
    :param iso: :class:`BoundIso <hcloud.isos.client.BoundIso>`, None
    :param rescue_enabled: bool
           True if rescue mode is enabled: Server will then boot into rescue system on next reboot.
    :param locked: bool
           True if server has been locked and is not available to user.
    :param backup_window: str, None
           Time window (UTC) in which the backup will run, or None if the backups are not enabled
    :param outgoing_traffic: int, None
           Outbound Traffic for the current billing period in bytes
    :param ingoing_traffic: int, None
           Inbound Traffic for the current billing period in bytes
    :param included_traffic: int
           Free Traffic for the current billing period in bytes
    :param primary_disk_size: int
           Size of the primary Disk
    :param protection: dict
           Protection configuration for the server
    :param labels: dict
            User-defined labels (key-value pairs)
    :param volumes: List[:class:`BoundVolume <hcloud.volumes.client.BoundVolume>`]
            Volumes assigned to this server.
    :param private_net: List[:class:`PrivateNet <hcloud.servers.domain.PrivateNet>`]
            Private networks information.
    """

    STATUS_RUNNING = "running"
    """Server Status running"""
    STATUS_INIT = "initializing"
    """Server Status initializing"""
    STATUS_STARTING = "starting"
    """Server Status starting"""
    STATUS_STOPPING = "stopping"
    """Server Status stopping"""
    STATUS_OFF = "off"
    """Server Status off"""
    STATUS_DELETING = "deleting"
    """Server Status deleting"""
    STATUS_MIGRATING = "migrating"
    """Server Status migrating"""
    STATUS_REBUILDING = "rebuilding"
    """Server Status rebuilding"""
    STATUS_UNKNOWN = "unknown"
    """Server Status unknown"""

    __api_properties__ = (
        "id",
        "name",
        "status",
        "public_net",
        "server_type",
        "datacenter",
        "image",
        "iso",
        "rescue_enabled",
        "locked",
        "backup_window",
        "outgoing_traffic",
        "ingoing_traffic",
        "included_traffic",
        "protection",
        "labels",
        "volumes",
        "private_net",
        "created",
        "primary_disk_size",
        "placement_group",
    )
    __slots__ = __api_properties__

    # pylint: disable=too-many-locals
    def __init__(
        self,
        id: int,
        name: str | None = None,
        status: str | None = None,
        created: str | None = None,
        public_net: PublicNetwork | None = None,
        server_type: BoundServerType | None = None,
        datacenter: BoundDatacenter | None = None,
        image: BoundImage | None = None,
        iso: BoundIso | None = None,
        rescue_enabled: bool | None = None,
        locked: bool | None = None,
        backup_window: str | None = None,
        outgoing_traffic: int | None = None,
        ingoing_traffic: int | None = None,
        included_traffic: int | None = None,
        protection: dict | None = None,
        labels: dict[str, str] | None = None,
        volumes: list[BoundVolume] | None = None,
        private_net: list[PrivateNet] | None = None,
        primary_disk_size: int | None = None,
        placement_group: BoundPlacementGroup | None = None,
    ):
        self.id = id
        self.name = name
        self.status = status
        self.created = isoparse(created) if created else None
        self.public_net = public_net
        self.server_type = server_type
        self.datacenter = datacenter
        self.image = image
        self.iso = iso
        self.rescue_enabled = rescue_enabled
        self.locked = locked
        self.backup_window = backup_window
        self.outgoing_traffic = outgoing_traffic
        self.ingoing_traffic = ingoing_traffic
        self.included_traffic = included_traffic
        self.protection = protection
        self.labels = labels
        self.volumes = volumes
        self.private_net = private_net
        self.primary_disk_size = primary_disk_size
        self.placement_group = placement_group


class CreateServerResponse(BaseDomain):
    """Create Server Response Domain

    :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>`
           The created server
    :param action: :class:`BoundAction <hcloud.actions.client.BoundAction>`
           Shows the progress of the server creation
    :param next_actions: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
           Additional actions like a `start_server` action after the server creation
    :param root_password: str, None
           The root password of the server if no SSH-Key was given on server creation
    """

    __api_properties__ = ("server", "action", "next_actions", "root_password")
    __slots__ = __api_properties__

    def __init__(
        self,
        server: BoundServer,
        action: BoundAction,
        next_actions: list[BoundAction],
        root_password: str | None,
    ):
        self.server = server
        self.action = action
        self.next_actions = next_actions
        self.root_password = root_password


class ResetPasswordResponse(BaseDomain):
    """Reset Password Response Domain

    :param action: :class:`BoundAction <hcloud.actions.client.BoundAction>`
           Shows the progress of the server passwort reset action
    :param root_password: str
           The root password of the server
    """

    __api_properties__ = ("action", "root_password")
    __slots__ = __api_properties__

    def __init__(
        self,
        action: BoundAction,
        root_password: str,
    ):
        self.action = action
        self.root_password = root_password


class EnableRescueResponse(BaseDomain):
    """Enable Rescue Response Domain

    :param action: :class:`BoundAction <hcloud.actions.client.BoundAction>`
           Shows the progress of the server enable rescue action
    :param root_password: str
           The root password of the server in the rescue mode
    """

    __api_properties__ = ("action", "root_password")
    __slots__ = __api_properties__

    def __init__(
        self,
        action: BoundAction,
        root_password: str,
    ):
        self.action = action
        self.root_password = root_password


class RequestConsoleResponse(BaseDomain):
    """Request Console Response Domain

    :param action: :class:`BoundAction <hcloud.actions.client.BoundAction>`
           Shows the progress of the server request console action
    :param wss_url: str
           URL of websocket proxy to use. This includes a token which is valid for a limited time only.
    :param password: str
           VNC password to use for this connection. This password only works in combination with a wss_url with valid token.
    """

    __api_properties__ = ("action", "wss_url", "password")
    __slots__ = __api_properties__

    def __init__(
        self,
        action: BoundAction,
        wss_url: str,
        password: str,
    ):
        self.action = action
        self.wss_url = wss_url
        self.password = password


class RebuildResponse(BaseDomain):
    """Rebuild Response Domain

    :param action: Shows the progress of the server rebuild action
    :param root_password: The root password of the server when not using SSH keys
    """

    __api_properties__ = ("action", "root_password")
    __slots__ = __api_properties__

    def __init__(
        self,
        action: BoundAction,
        root_password: str | None,
    ):
        self.action = action
        self.root_password = root_password


class PublicNetwork(BaseDomain):
    """Public Network Domain

    :param ipv4: :class:`IPv4Address <hcloud.servers.domain.IPv4Address>`
    :param ipv6: :class:`IPv6Network <hcloud.servers.domain.IPv6Network>`
    :param floating_ips: List[:class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`]
    :param primary_ipv4: :class:`BoundPrimaryIP <hcloud.primary_ips.domain.BoundPrimaryIP>`
    :param primary_ipv6: :class:`BoundPrimaryIP <hcloud.primary_ips.domain.BoundPrimaryIP>`
    :param firewalls: List[:class:`PublicNetworkFirewall <hcloud.servers.client.PublicNetworkFirewall>`]
    """

    __api_properties__ = (
        "ipv4",
        "ipv6",
        "floating_ips",
        "firewalls",
        "primary_ipv4",
        "primary_ipv6",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        ipv4: IPv4Address,
        ipv6: IPv6Network,
        floating_ips: list[BoundFloatingIP],
        primary_ipv4: BoundPrimaryIP | None,
        primary_ipv6: BoundPrimaryIP | None,
        firewalls: list[PublicNetworkFirewall] | None = None,
    ):
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.floating_ips = floating_ips
        self.firewalls = firewalls
        self.primary_ipv4 = primary_ipv4
        self.primary_ipv6 = primary_ipv6


class PublicNetworkFirewall(BaseDomain):
    """Public Network Domain

    :param firewall: :class:`BoundFirewall <hcloud.firewalls.domain.BoundFirewall>`
    :param status: str
    """

    __api_properties__ = ("firewall", "status")
    __slots__ = __api_properties__

    STATUS_APPLIED = "applied"
    """Public Network Firewall Status applied"""
    STATUS_PENDING = "pending"
    """Public Network Firewall Status pending"""

    def __init__(
        self,
        firewall: BoundFirewall,
        status: str,
    ):
        self.firewall = firewall
        self.status = status


class IPv4Address(BaseDomain):
    """IPv4 Address Domain

    :param ip: str
           The IPv4 Address
    :param blocked: bool
           Determine if the IP is blocked
    :param dns_ptr: str
           DNS PTR for the ip
    """

    __api_properties__ = ("ip", "blocked", "dns_ptr")
    __slots__ = __api_properties__

    def __init__(
        self,
        ip: str,
        blocked: bool,
        dns_ptr: str,
    ):
        self.ip = ip
        self.blocked = blocked
        self.dns_ptr = dns_ptr


class IPv6Network(BaseDomain):
    """IPv6 Network Domain

    :param ip: str
           The IPv6 Network as CIDR Notation
    :param blocked: bool
           Determine if the Network is blocked
    :param dns_ptr: dict
           DNS PTR Records for the Network as Dict
    :param network: str
           The network without the network mask
    :param network_mask: str
           The network mask
    """

    __api_properties__ = ("ip", "blocked", "dns_ptr", "network", "network_mask")
    __slots__ = __api_properties__

    def __init__(
        self,
        ip: str,
        blocked: bool,
        dns_ptr: list,
    ):
        self.ip = ip
        self.blocked = blocked
        self.dns_ptr = dns_ptr
        ip_parts = self.ip.split("/")  # 2001:db8::/64 to 2001:db8:: and 64
        self.network = ip_parts[0]
        self.network_mask = ip_parts[1]


class PrivateNet(BaseDomain):
    """PrivateNet Domain

    :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
           The network the server is attached to
    :param ip: str
           The main IP Address of the server in the Network
    :param alias_ips: List[str]
           The alias ips for a server
    :param mac_address: str
           The mac address of the interface on the server
    """

    __api_properties__ = ("network", "ip", "alias_ips", "mac_address")
    __slots__ = __api_properties__

    def __init__(
        self,
        network: BoundNetwork,
        ip: str,
        alias_ips: list[str],
        mac_address: str,
    ):
        self.network = network
        self.ip = ip
        self.alias_ips = alias_ips
        self.mac_address = mac_address


class ServerCreatePublicNetwork(BaseDomain):
    """Server Create Public Network Domain

    :param ipv4: Optional[:class:`PrimaryIP <hcloud.primary_ips.domain.PrimaryIP>`]
    :param ipv6: Optional[:class:`PrimaryIP <hcloud.primary_ips.domain.PrimaryIP>`]
    :param enable_ipv4: bool
    :param enable_ipv6: bool
    """

    __api_properties__ = ("ipv4", "ipv6", "enable_ipv4", "enable_ipv6")
    __slots__ = __api_properties__

    def __init__(
        self,
        ipv4: PrimaryIP | None = None,
        ipv6: PrimaryIP | None = None,
        enable_ipv4: bool = True,
        enable_ipv6: bool = True,
    ):
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.enable_ipv4 = enable_ipv4
        self.enable_ipv6 = enable_ipv6


MetricsType = Literal[
    "cpu",
    "disk",
    "network",
]


class GetMetricsResponse(BaseDomain):
    """Get a Server Metrics Response Domain

    :param metrics: The Server metrics
    """

    __api_properties__ = ("metrics",)
    __slots__ = __api_properties__

    def __init__(
        self,
        metrics: Metrics,
    ):
        self.metrics = metrics
