from __future__ import annotations

import warnings

from ..core import BaseDomain, DomainIdentityMixin
from ..deprecation import DeprecationInfo
from ..locations import BoundLocation


class ServerType(BaseDomain, DomainIdentityMixin):
    """ServerType Domain

    :param id: int
           ID of the server type
    :param name: str
           Unique identifier of the server type
    :param description: str
           Description of the server type
    :param category: str
           Category of the Server Type.
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
    :param locations: Supported Location of the Server Type.
    """

    __properties__ = (
        "id",
        "name",
        "description",
        "category",
        "cores",
        "memory",
        "disk",
        "prices",
        "storage_type",
        "cpu_type",
        "architecture",
        "locations",
    )
    __api_properties__ = (
        *__properties__,
        "deprecated",
        "deprecation",
        "included_traffic",
    )
    __slots__ = (
        *__properties__,
        "_deprecated",
        "_deprecation",
        "_included_traffic",
    )

    # pylint: disable=too-many-locals
    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        description: str | None = None,
        category: str | None = None,
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
        locations: list[ServerTypeLocation] | None = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.cores = cores
        self.memory = memory
        self.disk = disk
        self.prices = prices
        self.storage_type = storage_type
        self.cpu_type = cpu_type
        self.architecture = architecture
        self.locations = locations

        self.deprecated = deprecated
        self.deprecation = (
            DeprecationInfo.from_dict(deprecation) if deprecation is not None else None
        )
        self.included_traffic = included_traffic

    @property
    def deprecated(self) -> bool | None:
        """
        .. deprecated:: 2.6.0
            The 'deprecated' property is deprecated and will gradually be phased starting 24 September 2025.
            Please refer to the '.locations[].deprecation' property instead.

            See https://docs.hetzner.cloud/changelog#2025-09-24-per-location-server-types.
        """
        warnings.warn(
            "The 'deprecated' property is deprecated and will gradually be phased starting 24 September 2025. "
            "Please refer to the '.locations[].deprecation' property instead. "
            "See https://docs.hetzner.cloud/changelog#2025-09-24-per-location-server-types",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._deprecated

    @deprecated.setter
    def deprecated(self, value: bool | None) -> None:
        self._deprecated = value

    @property
    def deprecation(self) -> DeprecationInfo | None:
        """
        .. deprecated:: 2.6.0
            The 'deprecation' property is deprecated and will gradually be phased starting 24 September 2025.
            Please refer to the '.locations[].deprecation' property instead.

            See https://docs.hetzner.cloud/changelog#2025-09-24-per-location-server-types.
        """
        warnings.warn(
            "The 'deprecation' property is deprecated and will gradually be phased starting 24 September 2025. "
            "Please refer to the '.locations[].deprecation' property instead. "
            "See https://docs.hetzner.cloud/changelog#2025-09-24-per-location-server-types",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._deprecation

    @deprecation.setter
    def deprecation(self, value: DeprecationInfo | None) -> None:
        self._deprecation = value

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


class ServerTypeLocation(BaseDomain):
    """Server Type Location Domain

    :param location: Location of the Server Type.
    :param deprecation: Wether the Server Type is deprecated in this Location.
    """

    __api_properties__ = (
        "location",
        "deprecation",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        *,
        location: BoundLocation,
        deprecation: dict | None,
    ):
        self.location = location
        self.deprecation = (
            DeprecationInfo.from_dict(deprecation) if deprecation is not None else None
        )
