# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase, GetEntityByNameMixin

from hcloud.actions.client import BoundAction
from hcloud.core.domain import add_meta_to_result
from hcloud.volumes.domain import Volume, CreateVolumeResponse
from hcloud.locations.client import BoundLocation


class BoundVolume(BoundModelBase):
    model = Volume

    def __init__(self, client, data, complete=True):
        location = data.get("location")
        if location is not None:
            data["location"] = BoundLocation(client._client.locations, location)

        from hcloud.servers.client import BoundServer

        server = data.get("server")
        if server is not None:
            data["server"] = BoundServer(
                client._client.servers, {"id": server}, complete=False
            )
        super(BoundVolume, self).__init__(client, data, complete)

    def get_actions_list(self, status=None, sort=None, page=None, per_page=None):
        # type: (Optional[List[str]], Optional[int], Optional[int]) -> PageResults[List[BoundAction, Meta]]
        """Returns all action objects for a volume.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundAction <hcloud.actions.client.BoundAction>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        return self._client.get_actions_list(self, status, sort, page, per_page)

    def get_actions(self, status=None, sort=None):
        # type: (Optional[List[str]]) -> List[BoundAction]
        """Returns all action objects for a volume.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort:List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.get_actions(self, status, sort)

    def update(self, name=None, labels=None):
        # type: (Optional[str], Optional[Dict[str, str]]) -> BoundAction
        """Updates the volume properties.

        :param name: str (optional)
               New volume name
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.update(self, name, labels)

    def delete(self):
        # type: () -> BoundAction
        """Deletes a volume. All volume data is irreversibly destroyed. The volume must not be attached to a server and it must not have delete protection enabled.

        :return: boolean
        """
        return self._client.delete(self)

    def attach(self, server, automount=None):
        # type: (Union[Server, BoundServer]) -> BoundAction
        """Attaches a volume to a server. Works only if the server is in the same location as the volume.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param automount: boolean
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.attach(self, server, automount)

    def detach(self):
        # type: () -> BoundAction
        """Detaches a volume from the server it’s attached to. You may attach it to a server again at a later time.

        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.detach(self)

    def resize(self, size):
        # type: (int) -> BoundAction
        """Changes the size of a volume. Note that downsizing a volume is not possible.

        :param size: int
               New volume size in GB (must be greater than current size)
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.resize(self, size)

    def change_protection(self, delete=None):
        # type: (Optional[bool]) -> BoundAction
        """Changes the protection configuration of a volume.

        :param delete: boolean
               If True, prevents the volume from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_protection(self, delete)


class VolumesClient(ClientEntityBase, GetEntityByNameMixin):
    results_list_attribute_name = "volumes"

    def get_by_id(self, id):
        # type: (int) -> volumes.client.BoundVolume
        """Get a specific volume by its id

        :param id: int
        :return: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>`
        """
        response = self._client.request(
            url="/volumes/{volume_id}".format(volume_id=id), method="GET"
        )
        return BoundVolume(self, response["volume"])

    def get_list(
        self, name=None, label_selector=None, page=None, per_page=None, status=None
    ):
        # type: (Optional[str], Optional[str], Optional[int], Optional[int], Optional[List[str]]) -> PageResults[List[BoundVolume], Meta]
        """Get a list of volumes from this account

        :param name: str (optional)
               Can be used to filter volumes by their name.
        :param label_selector:  str (optional)
               Can be used to filter volumes by labels. The response will only contain volumes matching the label selector.
        :param status: List[str] (optional)
               Can be used to filter volumes by their status. The response will only contain volumes matching the status.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundVolume <hcloud.volumes.client.BoundVolume>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params = {}
        if name is not None:
            params["name"] = name
        if label_selector is not None:
            params["label_selector"] = label_selector
        if status is not None:
            params["status"] = status
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url="/volumes", method="GET", params=params)
        volumes = [
            BoundVolume(self, volume_data) for volume_data in response["volumes"]
        ]
        return self._add_meta_to_result(volumes, response)

    def get_all(self, label_selector=None, status=None):
        # type: (Optional[str], Optional[List[str]]) -> List[BoundVolume]
        """Get all volumes from this account

        :param label_selector:
               Can be used to filter volumes by labels. The response will only contain volumes matching the label selector.
        :param status: List[str] (optional)
               Can be used to filter volumes by their status. The response will only contain volumes matching the status.
        :return: List[:class:`BoundVolume <hcloud.volumes.client.BoundVolume>`]
        """
        return super(VolumesClient, self).get_all(
            label_selector=label_selector, status=status
        )

    def get_by_name(self, name):
        # type: (str) -> BoundVolume
        """Get volume by name

        :param name: str
               Used to get volume by name.
        :return: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>`
        """
        return super(VolumesClient, self).get_by_name(name)

    def create(
        self,
        size,  # type: int
        name,  # type: str
        labels=None,  # type: Optional[str]
        location=None,  # type: Optional[Location]
        server=None,  # type: Optional[Server],
        automount=None,  # type: Optional[bool],
        format=None,  # type: Optional[str],
    ):
        # type: (...) -> CreateVolumeResponse
        """Creates a new volume attached to a server.

        :param size: int
               Size of the volume in GB
        :param name: str
               Name of the volume
        :param labels: Dict[str,str] (optional)
               User-defined labels (key-value pairs)
        :param location: :class:`BoundLocation <hcloud.locations.client.BoundLocation>` or :class:`Location <hcloud.locations.domain.Location>`
        :param server:  :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param automount: boolean (optional)
               Auto mount volumes after attach.
        :param format: str (optional)
               Format volume after creation. One of: xfs, ext4
        :return: :class:`CreateVolumeResponse <hcloud.volumes.domain.CreateVolumeResponse>`
        """

        if size <= 0:
            raise ValueError("size must be greater than 0")

        if not (bool(location) ^ bool(server)):
            raise ValueError("only one of server or location must be provided")

        data = {
            "name": name,
            "size": size,
        }
        if labels is not None:
            data["labels"] = labels
        if location is not None:
            data["location"] = location.id_or_name

        if server is not None:
            data["server"] = server.id
        if automount is not None:
            data["automount"] = automount
        if format is not None:
            data["format"] = format

        response = self._client.request(url="/volumes", json=data, method="POST")

        result = CreateVolumeResponse(
            volume=BoundVolume(self, response["volume"]),
            action=BoundAction(self._client.actions, response["action"]),
            next_actions=[
                BoundAction(self._client.actions, action)
                for action in response["next_actions"]
            ],
        )
        return result

    def get_actions_list(
        self, volume, status=None, sort=None, page=None, per_page=None
    ):
        # type: (Volume, Optional[List[str]], Optional[int], Optional[int]) -> PageResults[List[BoundAction], Meta]
        """Returns all action objects for a volume.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundAction <hcloud.actions.client.BoundAction>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params = {}
        if status is not None:
            params["status"] = status
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(
            url="/volumes/{volume_id}/actions".format(volume_id=volume.id),
            method="GET",
            params=params,
        )
        actions = [
            BoundAction(self._client.actions, action_data)
            for action_data in response["actions"]
        ]
        return add_meta_to_result(actions, response, "actions")

    def get_actions(self, volume, status=None, sort=None):
        # type: (Union[Volume, BoundVolume], Optional[List[str]]) -> List[BoundAction]
        """Returns all action objects for a volume.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort:List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return super(VolumesClient, self).get_actions(volume, status=status, sort=sort)

    def update(self, volume, name=None, labels=None):
        # type:(Union[Volume, BoundVolume],  Optional[str],  Optional[Dict[str, str]]) -> BoundVolume
        """Updates the volume properties.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :param name: str (optional)
               New volume name
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {}
        if name is not None:
            data.update({"name": name})
        if labels is not None:
            data.update({"labels": labels})
        response = self._client.request(
            url="/volumes/{volume_id}".format(volume_id=volume.id),
            method="PUT",
            json=data,
        )
        return BoundVolume(self, response["volume"])

    def delete(self, volume):
        # type: (Union[Volume, BoundVolume]) -> BoundAction
        """Deletes a volume. All volume data is irreversibly destroyed. The volume must not be attached to a server and it must not have delete protection enabled.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :return: boolean
        """
        self._client.request(
            url="/volumes/{volume_id}".format(volume_id=volume.id), method="DELETE"
        )
        return True

    def resize(self, volume, size):
        # type: (Union[Volume, BoundVolume], int) -> BoundAction
        """Changes the size of a volume. Note that downsizing a volume is not possible.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :param size: int
               New volume size in GB (must be greater than current size)
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = self._client.request(
            url="/volumes/{volume_id}/actions/resize".format(volume_id=volume.id),
            json={"size": size},
            method="POST",
        )
        return BoundAction(self._client.actions, data["action"])

    def attach(self, volume, server, automount=None):
        # type: (Union[Volume, BoundVolume], Union[Server, BoundServer], Optional[bool]) -> BoundAction
        """Attaches a volume to a server. Works only if the server is in the same location as the volume.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param automount: boolean
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {"server": server.id}
        if automount is not None:
            data["automount"] = automount

        data = self._client.request(
            url="/volumes/{volume_id}/actions/attach".format(volume_id=volume.id),
            json=data,
            method="POST",
        )
        return BoundAction(self._client.actions, data["action"])

    def detach(self, volume):
        # type: (Union[Volume, BoundVolume]) -> BoundAction
        """Detaches a volume from the server it’s attached to. You may attach it to a server again at a later time.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = self._client.request(
            url="/volumes/{volume_id}/actions/detach".format(volume_id=volume.id),
            method="POST",
        )
        return BoundAction(self._client.actions, data["action"])

    def change_protection(self, volume, delete=None):
        # type: (Union[Volume, BoundVolume], Optional[bool], Optional[bool]) -> BoundAction
        """Changes the protection configuration of a volume.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :param delete: boolean
               If True, prevents the volume from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {}
        if delete is not None:
            data.update({"delete": delete})

        response = self._client.request(
            url="/volumes/{volume_id}/actions/change_protection".format(
                volume_id=volume.id
            ),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])
