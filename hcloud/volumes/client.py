# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase

from hcloud.actions.client import BoundAction
from hcloud.volumes.domain import Volume, CreateVolumeResponse


class BoundVolume(BoundModelBase):
    model = Volume

    def attach(self, server):
        # type: (Union[Server, BoundServer]) -> Action
        return self._client.attach(server, self)

    def detach(self):
        # type: () -> BoundAction
        return self._client.detach(self)


class VolumesClient(ClientEntityBase):

    def get_by_id(self, id):
        # type: (int) -> volumes.client.BoundVolume
        response = self._client.request(url="/volumes/{volume_id}".format(volume_id=id), method="GET")
        return BoundVolume(self, response['volume'])

    def get_all(self, label_selector=None):
        # type: (Optional[str]) -> List[volumes.client.BoundVolume]
        params = {}
        if label_selector:
            params['label_selector'] = label_selector

        response = self._client.request(url="/volumes", method="GET", params=params)
        return [BoundVolume(self, volume_data) for volume_data in response['volumes']]

    def create(self,
               size,           # type: int
               name,           # type: str
               labels=None,    # type: Optional[str]
               location=None,  # type: Optional[str]
               server=None     # type: Optional[Server]
               ):
        # type: (...) -> CreateVolumeResponse
        # TODO: convert location str type to locations.domain.Location type, when implementation is ready

        if size <= 0:
            raise ValueError("size must be greater than 0")

        if not(bool(location) ^ bool(server)):
            raise ValueError("only one of server or location must be provided")

        data = {
            'name': name,
            'size': size,
        }
        if labels is not None:
            data['labels'] = labels
        if location is not None:
            data['location'] = location
        if server is not None:
            data['server'] = server.id

        response = self._client.request(url="/volumes", json=data, method="POST")

        result = CreateVolumeResponse(
            volume=BoundVolume(self, response['volume']),
            action=BoundAction(self._client.actions, response['action']),
            next_actions=[BoundAction(self._client.actions, action) for action in response['next_actions']]
        )
        return result

    def attach(self, server, volume):
        # type: (Union[Server, BoundServer], Union[Volume, BoundVolume]) -> Action
        data = self._client.request(url="/volumes/{volume_id}/actions/attach".format(volume_id=volume.id), json={'server': server.id}, method="POST")
        return BoundAction(self._client.actions, data['action'])

    def detach(self, volume):
        # type: (Union[Volume, BoundVolume]) -> Action
        data = self._client.request(url="/volumes/{volume_id}/actions/detach".format(volume_id=volume.id), method="POST")
        return BoundAction(self._client.actions, data['action'])
