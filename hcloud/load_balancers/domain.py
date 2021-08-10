# -*- coding: utf-8 -*-
from dateutil.parser import isoparse

from hcloud.core.domain import BaseDomain


class LoadBalancer(BaseDomain):
    """LoadBalancer Domain

    :param id: int
           ID of the Load Balancer
    :param name: str
           Name of the Load Balancer (must be unique per project)
    :param created: datetime
           Point in time when the Load Balancer was created
    :param protection: dict
           Protection configuration for the Load Balancer
    :param labels: dict
            User-defined labels (key-value pairs)
    :param location: Location
            Location of the Load Balancer
    :param public_net: :class:`PublicNetwork <hcloud.load_balancers.domain.PublicNetwork>`
           Public network information.
    :param private_net: List[:class:`PrivateNet <hcloud.load_balancers.domain.PrivateNet`]
            Private networks information.
    :param algorithm: LoadBalancerAlgorithm
            The algorithm the Load Balancer is currently using
    :param services: List[LoadBalancerService]
            The services the LoadBalancer is currently serving
    :param targets: LoadBalancerTarget
            The targets the LoadBalancer is currently serving
    :param load_balancer_type: LoadBalancerType
            The type of the Load Balancer
    :param outgoing_traffic: int, None
           Outbound Traffic for the current billing period in bytes
    :param ingoing_traffic: int, None
           Inbound Traffic for the current billing period in bytes
    :param included_traffic: int
           Free Traffic for the current billing period in bytes
    """

    __slots__ = (
        "id",
        "name",
        "public_net",
        "private_net",
        "location",
        "algorithm",
        "services",
        "load_balancer_type",
        "protection",
        "labels",
        "targets",
        "created",
        "outgoing_traffic",
        "ingoing_traffic",
        "included_traffic",
    )

    def __init__(
        self,
        id,
        name=None,
        public_net=None,
        private_net=None,
        location=None,
        algorithm=None,
        services=None,
        load_balancer_type=None,
        protection=None,
        labels=None,
        targets=None,
        created=None,
        outgoing_traffic=None,
        ingoing_traffic=None,
        included_traffic=None,
    ):
        self.id = id
        self.name = name
        self.created = isoparse(created) if created else None
        self.public_net = public_net
        self.private_net = private_net
        self.location = location
        self.algorithm = algorithm
        self.services = services
        self.load_balancer_type = load_balancer_type
        self.targets = targets
        self.protection = protection
        self.labels = labels
        self.outgoing_traffic = outgoing_traffic
        self.ingoing_traffic = ingoing_traffic
        self.included_traffic = included_traffic


class LoadBalancerService(BaseDomain):
    """LoadBalancerService Domain

    :param protocol: str
           Protocol of the service Choices: tcp, http, https
    :param listen_port: int
           Required when protocol is tcp, must be unique per Load Balancer.
    :param destination_port: int
           Required when protocol is tcp
    :param proxyprotocol: bool
            Enable proxyprotocol
    :param health_check: LoadBalancerHealthCheck
            Configuration for health checks
    :param http: LoadBalancerServiceHttp
            Configuration for http/https protocols, required when protocol is http/https
    """

    def __init__(
        self,
        protocol=None,
        listen_port=None,
        destination_port=None,
        proxyprotocol=None,
        health_check=None,
        http=None,
    ):
        self.protocol = protocol
        self.listen_port = listen_port
        self.destination_port = destination_port
        self.proxyprotocol = proxyprotocol
        self.health_check = health_check
        self.http = http


class LoadBalancerServiceHttp(BaseDomain):
    """LoadBalancerServiceHttp Domain

    :param cookie_name: str
        Name of the cookie used for Session Stickness
    :param cookie_lifetime: str
        Lifetime of the cookie used for Session Stickness
    :param certificates: list
            IDs of the Certificates to use for TLS/SSL termination by the Load Balancer; empty for TLS/SSL passthrough or if protocol is "http"
    :param redirect_http: bool
           Redirect traffic from http port 80 to port 443
    :param sticky_sessions: bool
           Use sticky sessions. Only available if protocol is "http" or "https".
    """

    def __init__(
        self,
        cookie_name=None,
        cookie_lifetime=None,
        certificates=None,
        redirect_http=None,
        sticky_sessions=None,
    ):
        self.cookie_name = cookie_name
        self.cookie_lifetime = cookie_lifetime
        self.certificates = certificates
        self.redirect_http = redirect_http
        self.sticky_sessions = sticky_sessions


class LoadBalancerHealthCheck(BaseDomain):
    """LoadBalancerHealthCheck Domain

    :param protocol: str
        Protocol of the service Choices: tcp, http, https
    :param port: int
        Port the healthcheck will be performed on
    :param interval: int
           Interval we trigger health check in
    :param timeout: int
            Timeout in sec after a try is assumed as timeout
    :param retries: int
            Retries we perform until we assume a target as unhealthy
    :param http: LoadBalancerHealtCheckHttp
            HTTP Config
    """

    def __init__(
        self,
        protocol=None,
        port=None,
        interval=None,
        timeout=None,
        retries=None,
        http=None,
    ):
        self.protocol = protocol
        self.port = port
        self.interval = interval
        self.timeout = timeout
        self.retries = retries
        self.http = http


class LoadBalancerHealtCheckHttp(BaseDomain):
    """LoadBalancerHealtCheckHttp Domain

    :param domain: str
            Domain name to send in HTTP request. Can be null: In that case we will not send a domain name
    :param path: str
            HTTP Path send in Request
    :param response: str
            Optional HTTP response to receive in order to pass the health check
    :param status_codes: list
            List of HTTP status codes to receive in order to pass the health check
    :param tls: bool
            Type of health check
    """

    def __init__(
        self, domain=None, path=None, response=None, status_codes=None, tls=None
    ):
        self.domain = domain
        self.path = path
        self.response = response
        self.status_codes = status_codes
        self.tls = tls


class LoadBalancerTarget(BaseDomain):
    """LoadBalancerTarget Domain

    :param type: str
            Type of the resource, can be server or label_selector
    :param server: Server
            Target server
    :param label_selector: LoadBalancerTargetLabelSelector
            Target label selector
    :param ip: LoadBalancerTargetIP
            Target IP
    :param use_private_ip: bool
            use the private IP instead of primary public IP
    """

    def __init__(
        self, type=None, server=None, label_selector=None, ip=None, use_private_ip=None
    ):
        self.type = type
        self.server = server
        self.label_selector = label_selector
        self.ip = ip
        self.use_private_ip = use_private_ip


class LoadBalancerTargetLabelSelector(BaseDomain):
    """LoadBalancerTargetLabelSelector Domain

    :param selector: str Target label selector
    """

    def __init__(self, selector=None):
        self.selector = selector


class LoadBalancerTargetIP(BaseDomain):
    """LoadBalancerTargetIP Domain

    :param ip: str Target IP
    """

    def __init__(self, ip=None):
        self.ip = ip


class LoadBalancerAlgorithm(BaseDomain):
    """LoadBalancerAlgorithm Domain

    :param type: str
            Algorithm of the Load Balancer. Choices: round_robin, least_connections
    """

    def __init__(self, type=None):
        self.type = type


class PublicNetwork(BaseDomain):
    """Public Network Domain

    :param ipv4: :class:`IPv4Address <hcloud.load_balancers.domain.IPv4Address>`
    :param ipv6: :class:`IPv6Network <hcloud.load_balancers.domain.IPv6Network>`
    :param enabled:  boolean
    """

    __slots__ = ("ipv4", "ipv6", "enabled")

    def __init__(
        self,
        ipv4,  # type: IPv4Address
        ipv6,  # type: IPv6Network
        enabled,  # type: bool
    ):
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.enabled = enabled


class IPv4Address(BaseDomain):
    """IPv4 Address Domain

    :param ip: str
           The IPv4 Address
    """

    __slots__ = ("ip",)

    def __init__(
        self,
        ip,  # type: str
    ):
        self.ip = ip


class IPv6Network(BaseDomain):
    """IPv6 Network Domain

    :param ip: str
           The IPv6 Network as CIDR Notation
    """

    __slots__ = ("ip",)

    def __init__(
        self,
        ip,  # type: str
    ):
        self.ip = ip


class PrivateNet(BaseDomain):
    """PrivateNet Domain

    :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
           The Network the LoadBalancer is attached to
    :param ip: str
           The main IP Address of the LoadBalancer in the Network
    """

    __slots__ = (
        "network",
        "ip",
    )

    def __init__(
        self,
        network,  # type: BoundNetwork
        ip,  # type: str
    ):
        self.network = network
        self.ip = ip


class CreateLoadBalancerResponse(BaseDomain):
    """Create Load Balancer Response Domain

    :param load_balancer: :class:`BoundLoadBalancer <hcloud.load_balancers.client.BoundLoadBalancer>`
           The created Load Balancer
    :param action: :class:`BoundAction <hcloud.actions.client.BoundAction>`
           Shows the progress of the Load Balancer creation
    """

    __slots__ = (
        "load_balancer",
        "action",
    )

    def __init__(
        self,
        load_balancer,  # type: BoundLoadBalancer
        action,  # type: BoundAction
    ):
        self.load_balancer = load_balancer
        self.action = action
