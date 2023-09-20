from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

from ..actions import ActionsPageResult, BoundAction, ResourceActionsClient
from ..core import BoundModelBase, ClientEntityBase, Meta
from ..locations import BoundLocation
from .domain import CreateVolumeResponse, Volume

if TYPE_CHECKING:
    from .._client import Client
    from ..locations import Location
    from ..servers import BoundServer, Server


class BoundVolume(BoundModelBase, Volume):
    _client: VolumesClient

    model = Volume

    def __init__(self, client: VolumesClient, data: dict, complete: bool = True):
        location = data.get("location")
        if location is not None:
            data["location"] = BoundLocation(client._client.locations, location)

        # pylint: disable=import-outside-toplevel
        from ..servers import BoundServer

        server = data.get("server")
        if server is not None:
            data["server"] = BoundServer(
                client._client.servers, {"id": server}, complete=False
            )
        super().__init__(client, data, complete)

    def get_actions_list(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
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

    def get_actions(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """Returns all action objects for a volume.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.get_actions(self, status, sort)

    def update(
        self,
        name: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundVolume:
        """Updates the volume properties.

        :param name: str (optional)
               New volume name
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.update(self, name, labels)

    def delete(self) -> bool:
        """Deletes a volume. All volume data is irreversibly destroyed. The volume must not be attached to a server and it must not have delete protection enabled.

        :return: boolean
        """
        return self._client.delete(self)

    def attach(
        self,
        server: Server | BoundServer,
        automount: bool | None = None,
    ) -> BoundAction:
        """Attaches a volume to a server. Works only if the server is in the same location as the volume.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param automount: boolean
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.attach(self, server, automount)

    def detach(self) -> BoundAction:
        """Detaches a volume from the server it’s attached to. You may attach it to a server again at a later time.

        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.detach(self)

    def resize(self, size: int) -> BoundAction:
        """Changes the size of a volume. Note that downsizing a volume is not possible.

        :param size: int
               New volume size in GB (must be greater than current size)
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.resize(self, size)

    def change_protection(self, delete: bool | None = None) -> BoundAction:
        """Changes the protection configuration of a volume.

        :param delete: boolean
               If True, prevents the volume from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_protection(self, delete)


class VolumesPageResult(NamedTuple):
    volumes: list[BoundVolume]
    meta: Meta | None


class VolumesClient(ClientEntityBase):
    _client: Client

    actions: ResourceActionsClient
    """Volumes scoped actions client

    :type: :class:`ResourceActionsClient <hcloud.actions.client.ResourceActionsClient>`
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.actions = ResourceActionsClient(client, "/volumes")

    def get_by_id(self, id: int) -> BoundVolume:
        """Get a specific volume by its id

        :param id: int
        :return: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>`
        """
        response = self._client.request(url=f"/volumes/{id}", method="GET")
        return BoundVolume(self, response["volume"])

    def get_list(
        self,
        name: str | None = None,
        label_selector: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        status: list[str] | None = None,
    ) -> VolumesPageResult:
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
        params: dict[str, Any] = {}
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
        return VolumesPageResult(volumes, Meta.parse_meta(response))

    def get_all(
        self,
        label_selector: str | None = None,
        status: list[str] | None = None,
    ) -> list[BoundVolume]:
        """Get all volumes from this account

        :param label_selector:
               Can be used to filter volumes by labels. The response will only contain volumes matching the label selector.
        :param status: List[str] (optional)
               Can be used to filter volumes by their status. The response will only contain volumes matching the status.
        :return: List[:class:`BoundVolume <hcloud.volumes.client.BoundVolume>`]
        """
        return self._iter_pages(
            self.get_list,
            label_selector=label_selector,
            status=status,
        )

    def get_by_name(self, name: str) -> BoundVolume | None:
        """Get volume by name

        :param name: str
               Used to get volume by name.
        :return: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>`
        """
        return self._get_first_by(name=name)

    def create(
        self,
        size: int,
        name: str,
        labels: str | None = None,
        location: Location | None = None,
        server: Server | None = None,
        automount: bool | None = None,
        format: str | None = None,
    ) -> CreateVolumeResponse:
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

        if not bool(location) ^ bool(server):
            raise ValueError("only one of server or location must be provided")

        data: dict[str, Any] = {"name": name, "size": size}
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
        self,
        volume: Volume | BoundVolume,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
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
        params: dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(
            url=f"/volumes/{volume.id}/actions",
            method="GET",
            params=params,
        )
        actions = [
            BoundAction(self._client.actions, action_data)
            for action_data in response["actions"]
        ]
        return ActionsPageResult(actions, Meta.parse_meta(response))

    def get_actions(
        self,
        volume: Volume | BoundVolume,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """Returns all action objects for a volume.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._iter_pages(
            self.get_actions_list,
            volume,
            status=status,
            sort=sort,
        )

    def update(
        self,
        volume: Volume | BoundVolume,
        name: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundVolume:
        """Updates the volume properties.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :param name: str (optional)
               New volume name
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {}
        if name is not None:
            data.update({"name": name})
        if labels is not None:
            data.update({"labels": labels})
        response = self._client.request(
            url=f"/volumes/{volume.id}",
            method="PUT",
            json=data,
        )
        return BoundVolume(self, response["volume"])

    def delete(self, volume: Volume | BoundVolume) -> bool:
        """Deletes a volume. All volume data is irreversibly destroyed. The volume must not be attached to a server and it must not have delete protection enabled.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :return: boolean
        """
        self._client.request(url=f"/volumes/{volume.id}", method="DELETE")
        return True

    def resize(self, volume: Volume | BoundVolume, size: int) -> BoundAction:
        """Changes the size of a volume. Note that downsizing a volume is not possible.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :param size: int
               New volume size in GB (must be greater than current size)
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = self._client.request(
            url=f"/volumes/{volume.id}/actions/resize",
            json={"size": size},
            method="POST",
        )
        return BoundAction(self._client.actions, data["action"])

    def attach(
        self,
        volume: Volume | BoundVolume,
        server: Server | BoundServer,
        automount: bool | None = None,
    ) -> BoundAction:
        """Attaches a volume to a server. Works only if the server is in the same location as the volume.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param automount: boolean
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {"server": server.id}
        if automount is not None:
            data["automount"] = automount

        data = self._client.request(
            url=f"/volumes/{volume.id}/actions/attach",
            json=data,
            method="POST",
        )
        return BoundAction(self._client.actions, data["action"])

    def detach(self, volume: Volume | BoundVolume) -> BoundAction:
        """Detaches a volume from the server it’s attached to. You may attach it to a server again at a later time.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = self._client.request(
            url=f"/volumes/{volume.id}/actions/detach",
            method="POST",
        )
        return BoundAction(self._client.actions, data["action"])

    def change_protection(
        self,
        volume: Volume | BoundVolume,
        delete: bool | None = None,
    ) -> BoundAction:
        """Changes the protection configuration of a volume.

        :param volume: :class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`
        :param delete: boolean
               If True, prevents the volume from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {}
        if delete is not None:
            data.update({"delete": delete})

        response = self._client.request(
            url=f"/volumes/{volume.id}/actions/change_protection",
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])
