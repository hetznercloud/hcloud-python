# -*- coding: utf-8 -*-
from __future__ import absolute_import

import requests

from hcloud.actions.client import ActionsClient
from hcloud.floating_ips.client import FloatingIPsClient
from hcloud.isos.client import IsosClient
from hcloud.servers.client import ServersClient
from hcloud.server_types.client import ServerTypesClient
from hcloud.ssh_keys.client import SSHKeysClient
from hcloud.volumes.client import VolumesClient
from hcloud.images.client import ImagesClient
from hcloud.locations.client import LocationsClient
from hcloud.datacenters.client import DatacentersClient

from .version import VERSION


class HcloudAPIException(Exception):
    def __init__(self, code, message, details):
        self.code = code
        self.message = message
        self.details = details


class HcloudClient(object):
    version = VERSION

    def __init__(self, token):
        self.token = token
        self.api_endpoint = "https://api.hetzner.cloud/v1"

        self.datacenters = DatacentersClient(self)
        self.locations = LocationsClient(self)
        self.servers = ServersClient(self)
        self.server_types = ServerTypesClient(self)
        self.volumes = VolumesClient(self)
        self.actions = ActionsClient(self)
        self.images = ImagesClient(self)
        self.isos = IsosClient(self)
        self.ssh_keys = SSHKeysClient(self)
        self.floating_ips = FloatingIPsClient(self)

    def _get_user_agent(self):
        return "hcloud-python/" + self.version

    def _get_headers(self):
        headers = {
            "User-Agent": self._get_user_agent(),
            "Authorization": "Bearer {token}".format(token=self.token)
        }
        return headers

    def _raise_exception_from_response(self, response):
        raise HcloudAPIException(
            code=response.status_code,
            message=response.reason,
            details={
                'content': response.content
            }
        )

    def _raise_exception_from_json_content(self, json_content):
        raise HcloudAPIException(
            code=json_content['error']['code'],
            message=json_content['error']['message'],
            details=json_content['error']['details']
        )

    def request(self, method, url, **kwargs):
        response = requests.request(
            method,
            self.api_endpoint + url,
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
                self._raise_exception_from_json_content(json_content)
            else:
                self._raise_exception_from_response(response)

        return json_content
