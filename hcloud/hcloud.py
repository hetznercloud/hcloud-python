# -*- coding: utf-8 -*-
from __future__ import absolute_import

import time
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

from .version import VERSION, USER_AGENT_PREFIX


class HcloudAPIException(Exception):
    def __init__(self, code, message, details):
        self.code = code
        self.message = message
        self.details = details


class HcloudClient(object):
    version = VERSION
    retry_wait_time = 0.5

    def __init__(self, token):
        self.token = token
        self._api_endpoint = "https://api.hetzner.cloud/v1"
        self._application_name = None
        self._application_version = None

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
        if self._application_name is not None and self._application_version is None:
            return "{application_name} {prefix}/{version}".format(application_name=self._application_name,
                                                                  prefix=USER_AGENT_PREFIX,
                                                                  version=self.version)
        elif self._application_name is not None and self._application_version is not None:
            return "{application_name}/{application_version} {prefix}/{version}".format(
                application_name=self._application_name,
                application_version=self._application_version,
                prefix=USER_AGENT_PREFIX,
                version=self.version)
        else:
            return "{prefix}/{version}".format(prefix=USER_AGENT_PREFIX, version=self.version)

    def _get_headers(self):
        headers = {
            "User-Agent": self._get_user_agent(),
            "Authorization": "Bearer {token}".format(token=self.token)
        }
        return headers

    def with_endpoint(self, api_endpoint):
        self._api_endpoint = api_endpoint
        return self

    def with_application(self, name, version=None):
        self._application_name = name
        self._application_version = version
        return self

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

    def request(self, method, url, tries=1, **kwargs):
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
                    time.sleep(tries * self.retry_wait_time)
                    tries = tries + 1
                    return self.request(method, url, tries, **kwargs)
                else:
                    self._raise_exception_from_json_content(json_content)
            else:
                self._raise_exception_from_response(response)

        return json_content
