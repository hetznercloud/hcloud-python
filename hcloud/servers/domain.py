# -*- coding: utf-8 -*-
from dateutil.parser import isoparse

from hcloud.core.domain import BaseDomain


class Server(BaseDomain):
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
    :param protection: dict
           Protection configuration for the server
    :param labels: dict
            User-defined labels (key-value pairs)
    :param volumes: List[:class:`BoundVolume <hcloud.volumes.client.BoundVolume>`]
            Volumes assigned to this server.
    :param private_net: List[:class:`PrivateNet <hcloud.servers.domain.PrivateNet`]
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
    __slots__ = (
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
        "created"
    )

    def __init__(
            self,
            id,
            name=None,
            status=None,
            created=None,
            public_net=None,
            server_type=None,
            datacenter=None,
            image=None,
            iso=None,
            rescue_enabled=None,
            locked=None,
            backup_window=None,
            outgoing_traffic=None,
            ingoing_traffic=None,
            included_traffic=None,
            protection=None,
            labels=None,
            volumes=None,
            private_net=None,
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
    __slots__ = (
        "server",
        "action",
        "next_actions",
        "root_password"
    )

    def __init__(
            self,
            server,  # type: BoundServer
            action,  # type: BoundAction
            next_actions,  # type: List[Action]
            root_password  # type: str
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
    __slots__ = (
        "action",
        "root_password"
    )

    def __init__(
            self,
            action,  # type: BoundAction
            root_password  # type: str
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
    __slots__ = (
        "action",
        "root_password"
    )

    def __init__(
            self,
            action,  # type: BoundAction
            root_password  # type: str
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
    __slots__ = (
        "action",
        "wss_url",
        "password"
    )

    def __init__(
            self,
            action,  # type: BoundAction
            wss_url,  # type: str
            password,  # type: str
    ):
        self.action = action
        self.wss_url = wss_url
        self.password = password


class PublicNetwork(BaseDomain):
    """Public Network Domain

    :param ipv4: :class:`IPv4Address <hcloud.servers.domain.IPv4Address>`
    :param ipv6: :class:`IPv6Network <hcloud.servers.domain.IPv6Network>`
    :param floating_ips: List[:class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`]
    """
    __slots__ = (
        "ipv4",
        "ipv6",
        "floating_ips"
    )

    def __init__(self,
                 ipv4,  # type: IPv4Address
                 ipv6,  # type: IPv6Network
                 floating_ips,  # type: List[BoundFloatingIP]
                 ):
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.floating_ips = floating_ips


class IPv4Address(BaseDomain):
    """IPv4 Address Domain

    :param ip: str
           The IPv4 Address
    :param blocked: bool
           Determine if the IP is blocked
    :param dns_ptr: str
           DNS PTR for the ip
    """
    __slots__ = (
        "ip",
        "blocked",
        "dns_ptr"
    )

    def __init__(self,
                 ip,  # type: str
                 blocked,  # type: bool
                 dns_ptr,  # type: str
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
    __slots__ = (
        "ip",
        "blocked",
        "dns_ptr",
        "network",
        "network_mask"
    )

    def __init__(self,
                 ip,  # type: str
                 blocked,  # type: bool
                 dns_ptr,  # type: list
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
    __slots__ = (
        "network",
        "ip",
        "alias_ips",
        "mac_address"
    )

    def __init__(self,
                 network,  # type: BoundNetwork
                 ip,  # type: str
                 alias_ips,  # type: List[str]
                 mac_address,  # type: str
                 ):
        self.network = network
        self.ip = ip
        self.alias_ips = alias_ips
        self.mac_address = mac_address
