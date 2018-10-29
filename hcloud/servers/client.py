# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase

from hcloud.actions.domain import Action
from hcloud.servers.domain import Server, CreateServerResponse
from hcloud.volumes.client import BoundVolume


class BoundServer(BoundModelBase):
    model = Server

    def __init__(self, client, data):
        volumes = data.get('volumes', [])
        if volumes:
            volumes = [BoundVolume(client._client.volumes, {"id": volume}, complete=False) for volume in volumes]
            data['volumes'] = volumes
        super(BoundServer, self).__init__(client, data)

    def power_off(self):
        # type: () -> Action
        return self._client.power_off(self)

    def power_on(self):
        # type: () -> Action
        return self._client.power_on(self)

    def reboot(self):
        # type: () -> Action
        return self._client.reboot(self)


class ServersClient(ClientEntityBase):

    def get_by_id(self, id):
        # type: (int) -> BoundServer
        response = self._client.request(url="/servers/{server_id}".format(server_id=id), method="GET")
        return BoundServer(self, response['server'])

    def get_all(self, name=None, label_selector=None):
        # type: (Optional[str], Optional[str]) -> List[BoundServer]
        params = {}
        if name:
            params['name'] = name
        if label_selector:
            params['label_selector'] = label_selector

        response = self._client.request(url="/servers", method="GET", params=params)
        return [BoundServer(self, server_data) for server_data in response['servers']]

    def create(self,
               name,                     # type: str
               server_type,              # type: str
               image,                    # type: image
               ssh_keys=None,            # type: Optional[List[str]]
               volumes=None,             # type: Optional[List[Volume]]
               user_data=None,           # type: Optional[str]
               labels=None,              # type: Optional[Dict[str, str]]
               location=None,            # type: Optional[str]
               datacenter=None,          # type: Optional[str]
               start_after_create=True   # type: Optional[bool]
               ):
        # type: (...) -> CreateServerResponse
        # TODO: convert image str type to images.domain.Image type, when implementation is ready
        # TODO: convert location str type to locations.domain.Location type, when implementation is ready
        # TODO: convert datacenter str type to datacenters.domain.Datacenter type, when implementation is ready
        """
        Should be visible in docs
        :param name:
        :param server_type:
        :param image:
        :param ssh_keys:
        :param volumes:
        :param user_data:
        :param labels:
        :param location:
        :param datacenter:
        :param start_after_create:
        :return:
        """
        data = {
            'name': name,
            'server_type': server_type,
            'image': image,
            "start_after_create": start_after_create
        }
        if ssh_keys is not None:
            data['ssh_keys'] = ssh_keys
        if volumes is not None:
            data['volumes'] = [str(volume.id) for volume in volumes]
        if user_data is not None:
            data['user_data'] = user_data
        if labels is not None:
            data['labels'] = labels
        if location is not None:
            data['location'] = location
        if datacenter is not None:
            data["datacenter"] = datacenter

        response = self._client.request(url="/servers", method="POST", json=data)

        result = CreateServerResponse(
            server=BoundServer(self, response['server']),
            action=Action(**response['action']),
            next_actions=[Action(**action) for action in response['next_actions']],
            root_password=response['root_password']
        )
        return result

    def power_off(self, server):
        # type: (Server) -> Action
        response = self._client.request(url="/servers/{server_id}/actions/poweroff".format(server_id=server.id), method="POST")
        return Action(**response['action'])

    def power_on(self, server):
        # type: (servers.domain.Server) -> actions.domain.Action
        response = self._client.request(url="/servers/{server_id}/actions/poweron".format(server_id=server.id), method="POST")
        return Action(**response['action'])

    def reboot(self, server):
        # type: (servers.domain.Server) -> actions.domain.Action
        response = self._client.request(url="/servers/{server_id}/actions/reboot".format(server_id=server.id), method="POST")
        return Action(**response['action'])
