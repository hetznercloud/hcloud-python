# -*- coding: utf-8 -*-
from __future__ import absolute_import

import requests

from hcloud.actions.client import ActionsClient
from hcloud.servers.client import ServersClient
from hcloud.server_types.client import ServerTypesClient
from hcloud.volumes.client import VolumesClient
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

    def _get_user_agent(self):
        return "hcloud-python/" + self.version

    def _get_headers(self):
        headers = {
            "User-Agent": self._get_user_agent(),
            "Authorization": "Bearer {token}".format(token=self.token)
        }
        return headers

    def request(self, method, url, **kwargs):
        response = requests.request(
            method,
            self.api_endpoint + url,
            headers=self._get_headers(),
            **kwargs
        )

        try:
            result = response.json()
        except (TypeError, ValueError):
            raise HcloudAPIException(
                code=response.status_code,
                message=response.reason,
                details={
                    'content': response.content
                }
            )

        if not response.ok:

            raise HcloudAPIException(
                code=result['error']['code'],
                message=result['error']['message'],
                details=result['error']['details']
            )

        return result
