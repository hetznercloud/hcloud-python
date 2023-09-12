from __future__ import annotations

import time
from typing import NoReturn

import requests

from .__version__ import VERSION
from ._exceptions import APIException
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


class Client:
    """Base Client for accessing the Hetzner Cloud API"""

    _version = VERSION
    _retry_wait_time = 0.5
    __user_agent_prefix = "hcloud-python"

    def __init__(
        self,
        token: str,
        api_endpoint: str = "https://api.hetzner.cloud/v1",
        application_name: str | None = None,
        application_version: str | None = None,
        poll_interval: int = 1,
        timeout: float | tuple[float, float] | None = None,
    ):
        """Create a new Client instance

        :param token: Hetzner Cloud API token
        :param api_endpoint: Hetzner Cloud API endpoint
        :param application_name: Your application name
        :param application_version: Your application _version
        :param poll_interval: Interval for polling information from Hetzner Cloud API in seconds
        :param timeout: Requests timeout in seconds
        """
        self.token = token
        self._api_endpoint = api_endpoint
        self._application_name = application_name
        self._application_version = application_version
        self._requests_session = requests.Session()
        self._requests_timeout = timeout
        self.poll_interval = poll_interval

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

    def _raise_exception_from_response(self, response: requests.Response) -> NoReturn:
        raise APIException(
            code=response.status_code,
            message=response.reason,
            details={"content": response.content},
        )

    def _raise_exception_from_content(self, content: dict) -> NoReturn:
        raise APIException(
            code=content["error"]["code"],
            message=content["error"]["message"],
            details=content["error"]["details"],
        )

    def request(  # type: ignore[no-untyped-def]
        self,
        method: str,
        url: str,
        tries: int = 1,
        **kwargs,
    ) -> dict:
        """Perform a request to the Hetzner Cloud API, wrapper around requests.request

        :param method: HTTP Method to perform the Request
        :param url: URL of the Endpoint
        :param tries: Tries of the request (used internally, should not be set by the user)
        :param timeout: Requests timeout in seconds
        :return: Response
        """
        timeout = kwargs.pop("timeout", self._requests_timeout)

        response = self._requests_session.request(
            method=method,
            url=self._api_endpoint + url,
            headers=self._get_headers(),
            timeout=timeout,
            **kwargs,
        )

        content = response.content
        try:
            if len(content) > 0:
                content = response.json()
        except (TypeError, ValueError):
            self._raise_exception_from_response(response)

        if not response.ok:
            if content:
                assert isinstance(content, dict)
                if content["error"]["code"] == "rate_limit_exceeded" and tries < 5:
                    time.sleep(tries * self._retry_wait_time)
                    tries = tries + 1
                    return self.request(method, url, tries, **kwargs)

                self._raise_exception_from_content(content)
            else:
                self._raise_exception_from_response(response)

        # TODO: return an empty dict instead of an empty string when content == "".
        return content  # type: ignore[return-value]
