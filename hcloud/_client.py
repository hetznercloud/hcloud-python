from __future__ import annotations

import time
from random import uniform
from typing import Protocol

import requests

from ._exceptions import APIException
from ._version import __version__
from .actions import ActionsClient
from .certificates import CertificatesClient
from .datacenters import DatacentersClient
from .firewalls import FirewallsClient
from .floating_ips import FloatingIPsClient
from .images import ImagesClient
from .isos import IsosClient
from .load_balancer_types import LoadBalancerTypesClient
from .load_balancers import LoadBalancersClient
from .locations import LocationsClient
from .networks import NetworksClient
from .placement_groups import PlacementGroupsClient
from .primary_ips import PrimaryIPsClient
from .server_types import ServerTypesClient
from .servers import ServersClient
from .ssh_keys import SSHKeysClient
from .volumes import VolumesClient


class BackoffFunction(Protocol):
    def __call__(self, retries: int) -> float:
        """
        Return a interval in seconds to wait between each API call.

        :param retries: Number of calls already made.
        """


def constant_backoff_function(interval: float) -> BackoffFunction:
    """
    Return a backoff function, implementing a constant backoff.

    :param interval: Constant interval to return.
    """

    # pylint: disable=unused-argument
    def func(retries: int) -> float:
        return interval

    return func


def exponential_backoff_function(
    *,
    base: float,
    multiplier: int,
    cap: float,
    jitter: bool = False,
) -> BackoffFunction:
    """
    Return a backoff function, implementing a truncated exponential backoff with
    optional full jitter.

    :param base: Base for the exponential backoff algorithm.
    :param multiplier: Multiplier for the exponential backoff algorithm.
    :param cap: Value at which the interval is truncated.
    :param jitter: Whether to add jitter.
    """

    def func(retries: int) -> float:
        interval = base * multiplier**retries  # Exponential backoff
        interval = min(cap, interval)  # Cap backoff
        if jitter:
            interval = uniform(base, interval)  # Add jitter
        return interval

    return func


class Client:
    """Base Client for accessing the Hetzner Cloud API"""

    _version = __version__
    __user_agent_prefix = "hcloud-python"

    _retry_interval = staticmethod(
        exponential_backoff_function(base=1.0, multiplier=2, cap=60.0, jitter=True)
    )
    _retry_max_retries = 5

    def __init__(
        self,
        token: str,
        api_endpoint: str = "https://api.hetzner.cloud/v1",
        application_name: str | None = None,
        application_version: str | None = None,
        poll_interval: int | float | BackoffFunction = 1.0,
        poll_max_retries: int = 120,
        timeout: float | tuple[float, float] | None = None,
    ):
        """Create a new Client instance

        :param token: Hetzner Cloud API token
        :param api_endpoint: Hetzner Cloud API endpoint
        :param application_name: Your application name
        :param application_version: Your application _version
        :param poll_interval:
            Interval in seconds to use when polling actions from the API.
            You may pass a function to compute a custom poll interval.
        :param poll_max_retries:
            Max retries before timeout when polling actions from the API.
        :param timeout: Requests timeout in seconds
        """
        self.token = token
        self._api_endpoint = api_endpoint
        self._application_name = application_name
        self._application_version = application_version
        self._requests_session = requests.Session()
        self._requests_timeout = timeout

        if isinstance(poll_interval, (int, float)):
            self._poll_interval_func = constant_backoff_function(poll_interval)
        else:
            self._poll_interval_func = poll_interval
        self._poll_max_retries = poll_max_retries

        self.datacenters = DatacentersClient(self)
        """DatacentersClient Instance

        :type: :class:`DatacentersClient <hcloud.datacenters.client.DatacentersClient>`
        """
        self.locations = LocationsClient(self)
        """LocationsClient Instance

        :type: :class:`LocationsClient <hcloud.locations.client.LocationsClient>`
        """
        self.servers = ServersClient(self)
        """ServersClient Instance

        :type: :class:`ServersClient <hcloud.servers.client.ServersClient>`
        """
        self.server_types = ServerTypesClient(self)
        """ServerTypesClient Instance

        :type: :class:`ServerTypesClient <hcloud.server_types.client.ServerTypesClient>`
        """
        self.volumes = VolumesClient(self)
        """VolumesClient Instance

        :type: :class:`VolumesClient <hcloud.volumes.client.VolumesClient>`
        """
        self.actions = ActionsClient(self)
        """ActionsClient Instance

        :type: :class:`ActionsClient <hcloud.actions.client.ActionsClient>`
        """
        self.images = ImagesClient(self)
        """ImagesClient Instance

        :type: :class:`ImagesClient <hcloud.images.client.ImagesClient>`
        """
        self.isos = IsosClient(self)
        """ImagesClient Instance

        :type: :class:`IsosClient <hcloud.isos.client.IsosClient>`
        """
        self.ssh_keys = SSHKeysClient(self)
        """SSHKeysClient Instance

        :type: :class:`SSHKeysClient <hcloud.ssh_keys.client.SSHKeysClient>`
        """
        self.floating_ips = FloatingIPsClient(self)
        """FloatingIPsClient Instance

        :type: :class:`FloatingIPsClient <hcloud.floating_ips.client.FloatingIPsClient>`
        """
        self.primary_ips = PrimaryIPsClient(self)
        """PrimaryIPsClient Instance

        :type: :class:`PrimaryIPsClient <hcloud.primary_ips.client.PrimaryIPsClient>`
        """
        self.networks = NetworksClient(self)
        """NetworksClient Instance

        :type: :class:`NetworksClient <hcloud.networks.client.NetworksClient>`
        """
        self.certificates = CertificatesClient(self)
        """CertificatesClient Instance

        :type: :class:`CertificatesClient <hcloud.certificates.client.CertificatesClient>`
        """

        self.load_balancers = LoadBalancersClient(self)
        """LoadBalancersClient Instance

        :type: :class:`LoadBalancersClient <hcloud.load_balancers.client.LoadBalancersClient>`
        """

        self.load_balancer_types = LoadBalancerTypesClient(self)
        """LoadBalancerTypesClient Instance

        :type: :class:`LoadBalancerTypesClient <hcloud.load_balancer_types.client.LoadBalancerTypesClient>`
        """

        self.firewalls = FirewallsClient(self)
        """FirewallsClient Instance

        :type: :class:`FirewallsClient <hcloud.firewalls.client.FirewallsClient>`
        """

        self.placement_groups = PlacementGroupsClient(self)
        """PlacementGroupsClient Instance

        :type: :class:`PlacementGroupsClient <hcloud.placement_groups.client.PlacementGroupsClient>`
        """

    def _get_user_agent(self) -> str:
        """Get the user agent of the hcloud-python instance with the user application name (if specified)

        :return: The user agent of this hcloud-python instance
        """
        user_agents = []
        for name, version in [
            (self._application_name, self._application_version),
            (self.__user_agent_prefix, self._version),
        ]:
            if name is not None:
                user_agents.append(name if version is None else f"{name}/{version}")

        return " ".join(user_agents)

    def _get_headers(self) -> dict:
        headers = {
            "User-Agent": self._get_user_agent(),
            "Authorization": f"Bearer {self.token}",
        }
        return headers

    def request(  # type: ignore[no-untyped-def]
        self,
        method: str,
        url: str,
        **kwargs,
    ) -> dict:
        """Perform a request to the Hetzner Cloud API, wrapper around requests.request

        :param method: HTTP Method to perform the Request
        :param url: URL of the Endpoint
        :param timeout: Requests timeout in seconds
        :return: Response
        """
        kwargs.setdefault("timeout", self._requests_timeout)

        url = self._api_endpoint + url
        headers = self._get_headers()

        retries = 0
        while True:
            response = self._requests_session.request(
                method=method,
                url=url,
                headers=headers,
                **kwargs,
            )

            correlation_id = response.headers.get("X-Correlation-Id")
            payload = {}
            try:
                if len(response.content) > 0:
                    payload = response.json()
            except (TypeError, ValueError) as exc:
                raise APIException(
                    code=response.status_code,
                    message=response.reason,
                    details={"content": response.content},
                    correlation_id=correlation_id,
                ) from exc

            if not response.ok:
                if not payload or "error" not in payload:
                    raise APIException(
                        code=response.status_code,
                        message=response.reason,
                        details={"content": response.content},
                        correlation_id=correlation_id,
                    )

                error: dict = payload["error"]

                if (
                    error["code"] == "rate_limit_exceeded"
                    and retries < self._retry_max_retries
                ):
                    time.sleep(self._retry_interval(retries))
                    retries += 1
                    continue

                raise APIException(
                    code=error["code"],
                    message=error["message"],
                    details=error.get("details"),
                    correlation_id=correlation_id,
                )

            return payload
