# -*- coding: utf-8 -*-
from __future__ import absolute_import

import time
import requests

from hcloud.actions.client import ActionsClient
from hcloud.certificates.client import CertificatesClient
from hcloud.floating_ips.client import FloatingIPsClient
from hcloud.networks.client import NetworksClient
from hcloud.isos.client import IsosClient
from hcloud.servers.client import ServersClient
from hcloud.server_types.client import ServerTypesClient
from hcloud.ssh_keys.client import SSHKeysClient
from hcloud.volumes.client import VolumesClient
from hcloud.images.client import ImagesClient
from hcloud.locations.client import LocationsClient
from hcloud.datacenters.client import DatacentersClient
from hcloud.load_balancers.client import LoadBalancersClient
from hcloud.load_balancer_types.client import LoadBalancerTypesClient

from .__version__ import VERSION


class APIException(Exception):
    """There was an error while performing an API Request"""
    def __init__(self, code, message, details):
        self.code = code
        self.message = message
        self.details = details

    def __str__(self):
        return self.message


class Client(object):
    """Base Client for accessing the Hetzner Cloud API"""

    _version = VERSION
    _retry_wait_time = 0.5
    __user_agent_prefix = 'hcloud-python'

    def __init__(self, token, api_endpoint="https://api.hetzner.cloud/v1", application_name=None, application_version=None, poll_interval=1):
        """Create an new Client instance

        :param token: str
                Hetzner Cloud API token
        :param api_endpoint: str
                Hetzner Cloud API endpoint (default is https://api.hetzner.cloud/v1)
        :param application_name: str
                Your application name (default is None)
        :param application_version: str
                Your application _version (default is None)
        :param poll_interval: int
                Interval for polling information from Hetzner Cloud API in seconds (default is 1)
        """
        self.token = token
        self._api_endpoint = api_endpoint
        self._application_name = application_name
        self._application_version = application_version
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

    def _get_user_agent(self):
        """Get the user agent of the hcloud-python instance with the user application name (if specified)

        :return: str
            The user agent of this hcloud-python instance
        """
        if self._application_name is not None and self._application_version is None:
            return "{application_name} {prefix}/{version}".format(application_name=self._application_name,
                                                                  prefix=self.__user_agent_prefix,
                                                                  version=self._version)
        elif self._application_name is not None and self._application_version is not None:
            return "{application_name}/{application_version} {prefix}/{version}".format(
                application_name=self._application_name,
                application_version=self._application_version,
                prefix=self.__user_agent_prefix,
                version=self._version)
        else:
            return "{prefix}/{version}".format(prefix=self.__user_agent_prefix, version=self._version)

    def _get_headers(self):

        headers = {
            "User-Agent": self._get_user_agent(),
            "Authorization": "Bearer {token}".format(token=self.token)
        }
        return headers

    def _raise_exception_from_response(self, response):
        raise APIException(
            code=response.status_code,
            message=response.reason,
            details={
                'content': response.content
            }
        )

    def _raise_exception_from_json_content(self, json_content):
        raise APIException(
            code=json_content['error']['code'],
            message=json_content['error']['message'],
            details=json_content['error']['details']
        )

    def request(self, method, url, tries=1, **kwargs):
        """Perform a request to the Hetzner Cloud API, wrapper around requests.request

        :param method: str
                HTTP Method to perform the Request
        :param url: str
                URL of the Endpoint
        :param tries: int
                Tries of the request (used internally, should not be set by the user)
        :return: Response
        :rtype: requests.Response
        """
        response = requests.request(
            method,
            self._api_endpoint + url,
            headers=self._get_headers(),
            **kwargs
        )

        json_content = response.content
        try:
            if len(json_content) > 0:
                json_content = response.json()
        except (TypeError, ValueError):
            self._raise_exception_from_response(response)

        if not response.ok:
            if json_content:
                if json_content['error']['code'] == "rate_limit_exceeded" and tries < 5:
                    time.sleep(tries * self._retry_wait_time)
                    tries = tries + 1
                    return self.request(method, url, tries, **kwargs)
                else:
                    self._raise_exception_from_json_content(json_content)
            else:
                self._raise_exception_from_response(response)

        return json_content
