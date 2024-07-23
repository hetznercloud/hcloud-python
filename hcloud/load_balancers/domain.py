from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from dateutil.parser import isoparse

from ..core import BaseDomain, DomainIdentityMixin

if TYPE_CHECKING:
    from ..actions import BoundAction
    from ..certificates import BoundCertificate
    from ..load_balancer_types import BoundLoadBalancerType
    from ..locations import BoundLocation
    from ..metrics import Metrics
    from ..networks import BoundNetwork
    from ..servers import BoundServer
    from .client import BoundLoadBalancer


class LoadBalancer(BaseDomain, DomainIdentityMixin):
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

    __api_properties__ = (
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
    __slots__ = __api_properties__

    # pylint: disable=too-many-locals
    def __init__(
        self,
        id: int,
        name: str | None = None,
        public_net: PublicNetwork | None = None,
        private_net: list[PrivateNet] | None = None,
        location: BoundLocation | None = None,
        algorithm: LoadBalancerAlgorithm | None = None,
        services: list[LoadBalancerService] | None = None,
        load_balancer_type: BoundLoadBalancerType | None = None,
        protection: dict | None = None,
        labels: dict[str, str] | None = None,
        targets: list[LoadBalancerTarget] | None = None,
        created: str | None = None,
        outgoing_traffic: int | None = None,
        ingoing_traffic: int | None = None,
        included_traffic: int | None = None,
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
        protocol: str | None = None,
        listen_port: int | None = None,
        destination_port: int | None = None,
        proxyprotocol: bool | None = None,
        health_check: LoadBalancerHealthCheck | None = None,
        http: LoadBalancerServiceHttp | None = None,
    ):
        self.protocol = protocol
        self.listen_port = listen_port
        self.destination_port = destination_port
        self.proxyprotocol = proxyprotocol
        self.health_check = health_check
        self.http = http

    # pylint: disable=too-many-branches
    def to_payload(self) -> dict[str, Any]:
        """
        Generates the request payload from this domain object.
        """
        payload: dict[str, Any] = {}

        if self.protocol is not None:
            payload["protocol"] = self.protocol
        if self.listen_port is not None:
            payload["listen_port"] = self.listen_port
        if self.destination_port is not None:
            payload["destination_port"] = self.destination_port
        if self.proxyprotocol is not None:
            payload["proxyprotocol"] = self.proxyprotocol

        if self.http is not None:
            http: dict[str, Any] = {}
            if self.http.cookie_name is not None:
                http["cookie_name"] = self.http.cookie_name
            if self.http.cookie_lifetime is not None:
                http["cookie_lifetime"] = self.http.cookie_lifetime
            if self.http.redirect_http is not None:
                http["redirect_http"] = self.http.redirect_http
            if self.http.sticky_sessions is not None:
                http["sticky_sessions"] = self.http.sticky_sessions

            http["certificates"] = [
                certificate.id for certificate in self.http.certificates or []
            ]

            payload["http"] = http

        if self.health_check is not None:
            health_check: dict[str, Any] = {
                "protocol": self.health_check.protocol,
                "port": self.health_check.port,
                "interval": self.health_check.interval,
                "timeout": self.health_check.timeout,
                "retries": self.health_check.retries,
            }
            if self.health_check.protocol is not None:
                health_check["protocol"] = self.health_check.protocol
            if self.health_check.port is not None:
                health_check["port"] = self.health_check.port
            if self.health_check.interval is not None:
                health_check["interval"] = self.health_check.interval
            if self.health_check.timeout is not None:
                health_check["timeout"] = self.health_check.timeout
            if self.health_check.retries is not None:
                health_check["retries"] = self.health_check.retries

            if self.health_check.http is not None:
                health_check_http: dict[str, Any] = {}
                if self.health_check.http.domain is not None:
                    health_check_http["domain"] = self.health_check.http.domain
                if self.health_check.http.path is not None:
                    health_check_http["path"] = self.health_check.http.path
                if self.health_check.http.response is not None:
                    health_check_http["response"] = self.health_check.http.response
                if self.health_check.http.status_codes is not None:
                    health_check_http["status_codes"] = (
                        self.health_check.http.status_codes
                    )
                if self.health_check.http.tls is not None:
                    health_check_http["tls"] = self.health_check.http.tls

                health_check["http"] = health_check_http

            payload["health_check"] = health_check
        return payload


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
        cookie_name: str | None = None,
        cookie_lifetime: str | None = None,
        certificates: list[BoundCertificate] | None = None,
        redirect_http: bool | None = None,
        sticky_sessions: bool | None = None,
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
        protocol: str | None = None,
        port: int | None = None,
        interval: int | None = None,
        timeout: int | None = None,
        retries: int | None = None,
        http: LoadBalancerHealtCheckHttp | None = None,
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
        self,
        domain: str | None = None,
        path: str | None = None,
        response: str | None = None,
        status_codes: list | None = None,
        tls: bool | None = None,
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
    :param health_status: list
            List of health statuses of the services on this target. Only present for target types "server" and "ip".
    """

    def __init__(
        self,
        type: str | None = None,
        server: BoundServer | None = None,
        label_selector: LoadBalancerTargetLabelSelector | None = None,
        ip: LoadBalancerTargetIP | None = None,
        use_private_ip: bool | None = None,
        health_status: list[LoadBalancerTargetHealthStatus] | None = None,
    ):
        self.type = type
        self.server = server
        self.label_selector = label_selector
        self.ip = ip
        self.use_private_ip = use_private_ip
        self.health_status = health_status

    def to_payload(self) -> dict[str, Any]:
        """
        Generates the request payload from this domain object.
        """
        payload: dict[str, Any] = {
            "type": self.type,
        }
        if self.use_private_ip is not None:
            payload["use_private_ip"] = self.use_private_ip

        if self.type == "server":
            if self.server is None:
                raise ValueError(f"server is not defined in target {self!r}")
            payload["server"] = {"id": self.server.id}

        elif self.type == "label_selector":
            if self.label_selector is None:
                raise ValueError(f"label_selector is not defined in target {self!r}")
            payload["label_selector"] = {"selector": self.label_selector.selector}

        elif self.type == "ip":
            if self.ip is None:
                raise ValueError(f"ip is not defined in target {self!r}")
            payload["ip"] = {"ip": self.ip.ip}

        return payload


class LoadBalancerTargetHealthStatus(BaseDomain):
    """LoadBalancerTargetHealthStatus Domain

    :param listen_port: Load Balancer Target listen port
    :param status: Load Balancer Target status. Choices: healthy, unhealthy, unknown
    """

    def __init__(
        self,
        listen_port: int | None = None,
        status: str | None = None,
    ):
        self.listen_port = listen_port
        self.status = status


class LoadBalancerTargetLabelSelector(BaseDomain):
    """LoadBalancerTargetLabelSelector Domain

    :param selector: str Target label selector
    """

    def __init__(self, selector: str | None = None):
        self.selector = selector


class LoadBalancerTargetIP(BaseDomain):
    """LoadBalancerTargetIP Domain

    :param ip: str Target IP
    """

    def __init__(self, ip: str | None = None):
        self.ip = ip


class LoadBalancerAlgorithm(BaseDomain):
    """LoadBalancerAlgorithm Domain

    :param type: str
            Algorithm of the Load Balancer. Choices: round_robin, least_connections
    """

    def __init__(self, type: str | None = None):
        self.type = type


class PublicNetwork(BaseDomain):
    """Public Network Domain

    :param ipv4: :class:`IPv4Address <hcloud.load_balancers.domain.IPv4Address>`
    :param ipv6: :class:`IPv6Network <hcloud.load_balancers.domain.IPv6Network>`
    :param enabled:  boolean
    """

    __api_properties__ = ("ipv4", "ipv6", "enabled")
    __slots__ = __api_properties__

    def __init__(
        self,
        ipv4: IPv4Address,
        ipv6: IPv6Network,
        enabled: bool,
    ):
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.enabled = enabled


class IPv4Address(BaseDomain):
    """IPv4 Address Domain

    :param ip: str
           The IPv4 Address
    """

    __api_properties__ = ("ip", "dns_ptr")
    __slots__ = __api_properties__

    def __init__(
        self,
        ip: str,
        dns_ptr: str,
    ):
        self.ip = ip
        self.dns_ptr = dns_ptr


class IPv6Network(BaseDomain):
    """IPv6 Network Domain

    :param ip: str
           The IPv6 Network as CIDR Notation
    """

    __api_properties__ = ("ip", "dns_ptr")
    __slots__ = __api_properties__

    def __init__(
        self,
        ip: str,
        dns_ptr: str,
    ):
        self.ip = ip
        self.dns_ptr = dns_ptr


class PrivateNet(BaseDomain):
    """PrivateNet Domain

    :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
           The Network the LoadBalancer is attached to
    :param ip: str
           The main IP Address of the LoadBalancer in the Network
    """

    __api_properties__ = ("network", "ip")
    __slots__ = __api_properties__

    def __init__(
        self,
        network: BoundNetwork,
        ip: str,
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

    __api_properties__ = ("load_balancer", "action")
    __slots__ = __api_properties__

    def __init__(
        self,
        load_balancer: BoundLoadBalancer,
        action: BoundAction,
    ):
        self.load_balancer = load_balancer
        self.action = action


MetricsType = Literal[
    "open_connections",
    "connections_per_second",
    "requests_per_second",
    "bandwidth",
]


class GetMetricsResponse(BaseDomain):
    """Get a Load Balancer Metrics Response Domain

    :param metrics: The Load Balancer metrics
    """

    __api_properties__ = ("metrics",)
    __slots__ = __api_properties__

    def __init__(
        self,
        metrics: Metrics,
    ):
        self.metrics = metrics
