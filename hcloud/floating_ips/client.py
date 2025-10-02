from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

from ..actions import ActionsPageResult, BoundAction, ResourceActionsClient
from ..core import BoundModelBase, Meta, ResourceClientBase
from ..locations import BoundLocation
from .domain import CreateFloatingIPResponse, FloatingIP

if TYPE_CHECKING:
    from .._client import Client
    from ..locations import Location
    from ..servers import BoundServer, Server


class BoundFloatingIP(BoundModelBase, FloatingIP):
    _client: FloatingIPsClient

    model = FloatingIP

    def __init__(self, client: FloatingIPsClient, data: dict, complete: bool = True):
        # pylint: disable=import-outside-toplevel
        from ..servers import BoundServer

        server = data.get("server")
        if server is not None:
            data["server"] = BoundServer(
                client._parent.servers, {"id": server}, complete=False
            )

        home_location = data.get("home_location")
        if home_location is not None:
            data["home_location"] = BoundLocation(
                client._parent.locations, home_location
            )

        super().__init__(client, data, complete)

    def get_actions_list(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """Returns all action objects for a Floating IP.

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
        return self._client.get_actions_list(
            self,
            status=status,
            sort=sort,
            page=page,
            per_page=per_page,
        )

    def get_actions(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """Returns all action objects for a Floating IP.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.get_actions(self, status=status, sort=sort)

    def update(
        self,
        description: str | None = None,
        labels: dict[str, str] | None = None,
        name: str | None = None,
    ) -> BoundFloatingIP:
        """Updates the description or labels of a Floating IP.

        :param description: str (optional)
               New Description to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str (optional)
               New Name to set
        :return: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`
        """
        return self._client.update(
            self, description=description, labels=labels, name=name
        )

    def delete(self) -> bool:
        """Deletes a Floating IP. If it is currently assigned to a server it will automatically get unassigned.

        :return: boolean
        """
        return self._client.delete(self)

    def change_protection(self, delete: bool | None = None) -> BoundAction:
        """Changes the protection configuration of the Floating IP.

        :param delete: boolean
               If true, prevents the Floating IP from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_protection(self, delete=delete)

    def assign(self, server: Server | BoundServer) -> BoundAction:
        """Assigns a Floating IP to a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
               Server the Floating IP shall be assigned to
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.assign(self, server=server)

    def unassign(self) -> BoundAction:
        """Unassigns a Floating IP, resulting in it being unreachable. You may assign it to a server again at a later time.

        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.unassign(self)

    def change_dns_ptr(self, ip: str, dns_ptr: str) -> BoundAction:
        """Changes the hostname that will appear when getting the hostname belonging to this Floating IP.

        :param ip: str
               The IP address for which to set the reverse DNS entry
        :param dns_ptr: str
               Hostname to set as a reverse DNS PTR entry, will reset to original default value if `None`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_dns_ptr(self, ip=ip, dns_ptr=dns_ptr)


class FloatingIPsPageResult(NamedTuple):
    floating_ips: list[BoundFloatingIP]
    meta: Meta


class FloatingIPsClient(ResourceClientBase):
    _base_url = "/floating_ips"

    actions: ResourceActionsClient
    """Floating IPs scoped actions client

    :type: :class:`ResourceActionsClient <hcloud.actions.client.ResourceActionsClient>`
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.actions = ResourceActionsClient(client, self._base_url)

    def get_actions_list(
        self,
        floating_ip: FloatingIP | BoundFloatingIP,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """Returns all action objects for a Floating IP.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
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
            url=f"{self._base_url}/{floating_ip.id}/actions",
            method="GET",
            params=params,
        )
        actions = [
            BoundAction(self._parent.actions, action_data)
            for action_data in response["actions"]
        ]
        return ActionsPageResult(actions, Meta.parse_meta(response))

    def get_actions(
        self,
        floating_ip: FloatingIP | BoundFloatingIP,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """Returns all action objects for a Floating IP.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`

        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._iter_pages(
            self.get_actions_list,
            floating_ip,
            status=status,
            sort=sort,
        )

    def get_by_id(self, id: int) -> BoundFloatingIP:
        """Returns a specific Floating IP object.

        :param id: int
        :return: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`
        """
        response = self._client.request(url=f"{self._base_url}/{id}", method="GET")
        return BoundFloatingIP(self, response["floating_ip"])

    def get_list(
        self,
        label_selector: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        name: str | None = None,
    ) -> FloatingIPsPageResult:
        """Get a list of floating ips from this account

        :param label_selector: str (optional)
               Can be used to filter Floating IPs by labels. The response will only contain Floating IPs matching the label selector.able values.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :param name: str (optional)
               Can be used to filter networks by their name.
        :return: (List[:class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params: dict[str, Any] = {}

        if label_selector is not None:
            params["label_selector"] = label_selector
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if name is not None:
            params["name"] = name

        response = self._client.request(url=self._base_url, method="GET", params=params)
        floating_ips = [
            BoundFloatingIP(self, floating_ip_data)
            for floating_ip_data in response["floating_ips"]
        ]

        return FloatingIPsPageResult(floating_ips, Meta.parse_meta(response))

    def get_all(
        self,
        label_selector: str | None = None,
        name: str | None = None,
    ) -> list[BoundFloatingIP]:
        """Get all floating ips from this account

        :param label_selector: str (optional)
               Can be used to filter Floating IPs by labels. The response will only contain Floating IPs matching the label selector.able values.
        :param name: str (optional)
               Can be used to filter networks by their name.
        :return: List[:class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`]
        """
        return self._iter_pages(self.get_list, label_selector=label_selector, name=name)

    def get_by_name(self, name: str) -> BoundFloatingIP | None:
        """Get Floating IP by name

        :param name: str
               Used to get Floating IP by name.
        :return: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`
        """
        return self._get_first_by(name=name)

    def create(
        self,
        type: str,
        description: str | None = None,
        labels: dict[str, str] | None = None,
        home_location: Location | BoundLocation | None = None,
        server: Server | BoundServer | None = None,
        name: str | None = None,
    ) -> CreateFloatingIPResponse:
        """Creates a new Floating IP assigned to a server.

        :param type: str
               Floating IP type Choices: ipv4, ipv6
        :param description: str (optional)
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param home_location: :class:`BoundLocation <hcloud.locations.client.BoundLocation>` or :class:`Location <hcloud.locations.domain.Location>` (
               Home location (routing is optimized for that location). Only optional if server argument is passed.
        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or  :class:`Server <hcloud.servers.domain.Server>`
               Server to assign the Floating IP to
        :param name: str (optional)
        :return: :class:`CreateFloatingIPResponse <hcloud.floating_ips.domain.CreateFloatingIPResponse>`
        """

        data: dict[str, Any] = {"type": type}
        if description is not None:
            data["description"] = description
        if labels is not None:
            data["labels"] = labels
        if home_location is not None:
            data["home_location"] = home_location.id_or_name
        if server is not None:
            data["server"] = server.id
        if name is not None:
            data["name"] = name

        response = self._client.request(url=self._base_url, json=data, method="POST")

        action = None
        if response.get("action") is not None:
            action = BoundAction(self._parent.actions, response["action"])

        result = CreateFloatingIPResponse(
            floating_ip=BoundFloatingIP(self, response["floating_ip"]), action=action
        )
        return result

    def update(
        self,
        floating_ip: FloatingIP | BoundFloatingIP,
        description: str | None = None,
        labels: dict[str, str] | None = None,
        name: str | None = None,
    ) -> BoundFloatingIP:
        """Updates the description or labels of a Floating IP.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
        :param description: str (optional)
               New Description to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str (optional)
               New name to set
        :return: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`
        """
        data: dict[str, Any] = {}
        if description is not None:
            data["description"] = description
        if labels is not None:
            data["labels"] = labels
        if name is not None:
            data["name"] = name

        response = self._client.request(
            url=f"{self._base_url}/{floating_ip.id}",
            method="PUT",
            json=data,
        )
        return BoundFloatingIP(self, response["floating_ip"])

    def delete(self, floating_ip: FloatingIP | BoundFloatingIP) -> bool:
        """Deletes a Floating IP. If it is currently assigned to a server it will automatically get unassigned.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
        :return: boolean
        """
        self._client.request(
            url=f"{self._base_url}/{floating_ip.id}",
            method="DELETE",
        )
        # Return always true, because the API does not return an action for it. When an error occurs a HcloudAPIException will be raised
        return True

    def change_protection(
        self,
        floating_ip: FloatingIP | BoundFloatingIP,
        delete: bool | None = None,
    ) -> BoundAction:
        """Changes the protection configuration of the Floating IP.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
        :param delete: boolean
               If true, prevents the Floating IP from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {}
        if delete is not None:
            data.update({"delete": delete})

        response = self._client.request(
            url=f"{self._base_url}/{floating_ip.id}/actions/change_protection",
            method="POST",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def assign(
        self,
        floating_ip: FloatingIP | BoundFloatingIP,
        server: Server | BoundServer,
    ) -> BoundAction:
        """Assigns a Floating IP to a server.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or  :class:`Server <hcloud.servers.domain.Server>`
               Server the Floating IP shall be assigned to
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"{self._base_url}/{floating_ip.id}/actions/assign",
            method="POST",
            json={"server": server.id},
        )
        return BoundAction(self._parent.actions, response["action"])

    def unassign(self, floating_ip: FloatingIP | BoundFloatingIP) -> BoundAction:
        """Unassigns a Floating IP, resulting in it being unreachable. You may assign it to a server again at a later time.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"{self._base_url}/{floating_ip.id}/actions/unassign",
            method="POST",
        )
        return BoundAction(self._parent.actions, response["action"])

    def change_dns_ptr(
        self,
        floating_ip: FloatingIP | BoundFloatingIP,
        ip: str,
        dns_ptr: str,
    ) -> BoundAction:
        """Changes the hostname that will appear when getting the hostname belonging to this Floating IP.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
        :param ip: str
               The IP address for which to set the reverse DNS entry
        :param dns_ptr: str
               Hostname to set as a reverse DNS PTR entry, will reset to original default value if `None`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"{self._base_url}/{floating_ip.id}/actions/change_dns_ptr",
            method="POST",
            json={"ip": ip, "dns_ptr": dns_ptr},
        )
        return BoundAction(self._parent.actions, response["action"])
