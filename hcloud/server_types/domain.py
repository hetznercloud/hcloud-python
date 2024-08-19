from __future__ import annotations

import warnings

from ..core import BaseDomain, DomainIdentityMixin
from ..deprecation import DeprecationInfo


class ServerType(BaseDomain, DomainIdentityMixin):
    """ServerType Domain

    :param id: int
           ID of the server type
    :param name: str
           Unique identifier of the server type
    :param description: str
           Description of the server type
    :param cores: int
           Number of cpu cores a server of this type will have
    :param memory: int
           Memory a server of this type will have in GB
    :param disk: int
           Disk size a server of this type will have in GB
    :param prices: List of dict
           Prices in different locations
    :param storage_type: str
           Type of server boot drive. Local has higher speed. Network has better availability. Choices: `local`, `network`
    :param cpu_type: string
           Type of cpu. Choices: `shared`, `dedicated`
    :param architecture: string
           Architecture of cpu. Choices: `x86`, `arm`
    :param deprecated: bool
           True if server type is deprecated. This field is deprecated. Use `deprecation` instead.
    :param deprecation: :class:`DeprecationInfo <hcloud.deprecation.domain.DeprecationInfo>`, None
           Describes if, when & how the resources was deprecated. If this field is set to None the resource is not
           deprecated. If it has a value, it is considered deprecated.
    :param included_traffic: int
           Free traffic per month in bytes
    """

    __properties__ = (
        "id",
        "name",
        "description",
        "cores",
        "memory",
        "disk",
        "prices",
        "storage_type",
        "cpu_type",
        "architecture",
        "deprecated",
        "deprecation",
    )
    __api_properties__ = (
        *__properties__,
        "included_traffic",
    )
    __slots__ = (
        *__properties__,
        "_included_traffic",
    )

    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        description: str | None = None,
        cores: int | None = None,
        memory: int | None = None,
        disk: int | None = None,
        prices: list[dict] | None = None,
        storage_type: str | None = None,
        cpu_type: str | None = None,
        architecture: str | None = None,
        deprecated: bool | None = None,
        deprecation: dict | None = None,
        included_traffic: int | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.cores = cores
        self.memory = memory
        self.disk = disk
        self.prices = prices
        self.storage_type = storage_type
        self.cpu_type = cpu_type
        self.architecture = architecture
        self.deprecated = deprecated
        self.deprecation = (
            DeprecationInfo.from_dict(deprecation) if deprecation is not None else None
        )
        self.included_traffic = included_traffic

    @property
    def included_traffic(self) -> int | None:
        """
        .. deprecated:: 2.1.0
            The 'included_traffic' property is deprecated and will be set to 'None' on 5 August 2024.
            Please refer to the 'prices' property instead.

            See https://docs.hetzner.cloud/changelog#2024-07-25-cloud-api-returns-traffic-information-in-different-format.
        """
        warnings.warn(
            "The 'included_traffic' property is deprecated and will be set to 'None' on 5 August 2024. "
            "Please refer to the 'prices' property instead. "
            "See https://docs.hetzner.cloud/changelog#2024-07-25-cloud-api-returns-traffic-information-in-different-format",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._included_traffic

    @included_traffic.setter
    def included_traffic(self, value: int | None) -> None:
        self._included_traffic = value
