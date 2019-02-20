# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase

from hcloud.actions.client import BoundAction
from hcloud.core.domain import add_meta_to_result
from hcloud.volumes.domain import Volume, CreateVolumeResponse
from hcloud.locations.client import BoundLocation


class BoundVolume(BoundModelBase):
    model = Volume

    def __init__(self, client, data, complete=True):
        location = data.get("location")
        if location is not None:
            data['location'] = BoundLocation(client._client.locations, location)
        super(BoundVolume, self).__init__(client, data, complete)

    def get_actions_list(self, sort=None, page=None, per_page=None):
        # type: (Optional[List[str]], Optional[int], Optional[int]) -> PageResults[List[BoundAction, Meta]]
        return self._client.get_actions_list(self, sort, page, per_page)

    def get_actions(self, sort=None):
        # type: (Optional[List[str]]) -> List[BoundAction]
        return self._client.get_actions(self, sort)

    def update(self, name=None, labels=None):
        # type: (Optional[str], Optional[Dict[str, str]]) -> BoundAction
        return self._client.update(self, name, labels)

    def delete(self):
        # type: () -> BoundAction
        return self._client.delete(self)

    def attach(self, server, automount=None):
        # type: (Union[Server, BoundServer]) -> BoundAction
        return self._client.attach(self, server, automount)

    def detach(self):
        # type: () -> BoundAction
        return self._client.detach(self)

    def resize(self, size):
        # type: (int) -> BoundAction
        return self._client.resize(self, size)

    def change_protection(self, delete=None):
        # type: (Optional[bool]) -> BoundAction
        return self._client.change_protection(self, delete)


class VolumesClient(ClientEntityBase):
    results_list_attribute_name = 'volumes'

    def get_by_id(self, id):
        # type: (int) -> volumes.client.BoundVolume
        response = self._client.request(url="/volumes/{volume_id}".format(volume_id=id), method="GET")
        return BoundVolume(self, response['volume'])

    def get_list(self, label_selector=None, page=None, per_page=None):
        # type: (Optional[str], Optional[int], Optional[int]) -> PageResults[List[BoundVolume], Meta]
        params = {}
        if label_selector:
            params['label_selector'] = label_selector
        if page is not None:
            params['page'] = page
        if per_page is not None:
            params['per_page'] = per_page

        response = self._client.request(url="/volumes", method="GET", params=params)
        volumes = [BoundVolume(self, volume_data) for volume_data in response['volumes']]
        return self._add_meta_to_result(volumes, response)

    def get_all(self, label_selector=None):
        # type: (Optional[str]) -> List[BoundVolume]
        return super(VolumesClient, self).get_all(label_selector=label_selector)

    def create(self,
               size,            # type: int
               name,            # type: str
               labels=None,     # type: Optional[str]
               location=None,   # type: Optional[Location]
               server=None,     # type: Optional[Server],
               automount=None,  # type: Optional[bool],
               format=None,     # type: Optional[str],
               ):
        # type: (...) -> CreateVolumeResponse

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
            data['location'] = location.id_or_name

        if server is not None:
            data['server'] = server.id
        if automount is not None:
            data['automount'] = automount
        if format is not None:
            data['format'] = format

        response = self._client.request(url="/volumes", json=data, method="POST")

        result = CreateVolumeResponse(
            volume=BoundVolume(self, response['volume']),
            action=BoundAction(self._client.actions, response['action']),
            next_actions=[BoundAction(self._client.actions, action) for action in response['next_actions']]
        )
        return result

    def get_actions_list(self, volume, sort=None, page=None, per_page=None):
        # type: (Volume, Optional[List[str]], Optional[int], Optional[int]) -> PageResults[List[BoundAction], Meta]
        params = {}
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url="/volumes/{volume_id}/actions".format(volume_id=volume.id), method="GET", params=params)
        actions = [BoundAction(self._client.actions, action_data) for action_data in response['actions']]
        return add_meta_to_result(actions, response, 'actions')

    def get_actions(self, volume, sort=None):
        # type: (Union[Volume, BoundVolume], Optional[List[str]]) -> List[BoundAction]
        return super(VolumesClient, self).get_actions(volume, sort=sort)

    def update(self, volume, name=None, labels=None):
        # type:(Union[Volume, BoundVolume],  Optional[str],  Optional[Dict[str, str]]) -> BoundVolume
        data = {}
        if name is not None:
            data.update({"name": name})
        if labels is not None:
            data.update({"labels": labels})
        response = self._client.request(url="/volumes/{volume_id}".format(volume_id=volume.id), method="PUT", json=data)
        return BoundVolume(self, response['volume'])

    def delete(self, volume):
        # type: (Union[Volume, BoundVolume]) -> BoundAction
        self._client.request(url="/volumes/{volume_id}".format(volume_id=volume.id), method="DELETE")
        return True

    def resize(self, volume, size):
        # type: (Union[Volume, BoundVolume], int) -> BoundAction
        data = self._client.request(url="/volumes/{volume_id}/actions/resize".format(volume_id=volume.id), json={'size': size}, method="POST")
        return BoundAction(self._client.actions, data['action'])

    def attach(self, volume, server, automount=None):
        # type: (Union[Volume, BoundVolume], Union[Server, BoundServer], Optional[bool]) -> BoundAction
        data = {'server': server.id}
        if automount is not None:
            data["automount"] = automount

        data = self._client.request(url="/volumes/{volume_id}/actions/attach".format(volume_id=volume.id), json=data, method="POST")
        return BoundAction(self._client.actions, data['action'])

    def detach(self, volume):
        # type: (Union[Volume, BoundVolume]) -> BoundAction
        data = self._client.request(url="/volumes/{volume_id}/actions/detach".format(volume_id=volume.id), method="POST")
        return BoundAction(self._client.actions, data['action'])

    def change_protection(self, volume, delete=None):
        # type: (Union[Volume, BoundVolume], Optional[bool], Optional[bool]) -> BoundAction
        data = {}
        if delete is not None:
            data.update({"delete": delete})

        response = self._client.request(url="/volumes/{volume_id}/actions/change_protection".format(volume_id=volume.id),
                                        method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])
