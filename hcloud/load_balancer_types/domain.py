from __future__ import annotations

from ..core import BaseDomain, DomainIdentityMixin


class LoadBalancerType(BaseDomain, DomainIdentityMixin):
    """LoadBalancerType Domain

    :param id: int
           ID of the Load Balancer type
    :param name: str
           Name of the Load Balancer type
    :param description: str
           Description of the Load Balancer type
    :param max_connections: int
           Max amount of connections the Load Balancer can handle
    :param max_services: int
           Max amount of services the Load Balancer can handle
    :param max_targets: int
           Max amount of targets the Load Balancer can handle
    :param max_assigned_certificates: int
           Max amount of certificates the Load Balancer can serve
    :param prices: List of dict
           Prices in different locations

    """

    __api_properties__ = (
        "id",
        "name",
        "description",
        "max_connections",
        "max_services",
        "max_targets",
        "max_assigned_certificates",
        "prices",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        description: str | None = None,
        max_connections: int | None = None,
        max_services: int | None = None,
        max_targets: int | None = None,
        max_assigned_certificates: int | None = None,
        prices: list[dict] | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.max_connections = max_connections
        self.max_services = max_services
        self.max_targets = max_targets
        self.max_assigned_certificates = max_assigned_certificates
        self.prices = prices
