from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

from ..actions import ActionsPageResult, BoundAction, ResourceActionsClient
from ..core import BoundModelBase, Meta, ResourceClientBase
from .domain import Network, NetworkRoute, NetworkSubnet

if TYPE_CHECKING:
    from .._client import Client


class BoundNetwork(BoundModelBase, Network):
    _client: NetworksClient

    model = Network

    def __init__(self, client: NetworksClient, data: dict, complete: bool = True):
        subnets = data.get("subnets", [])
        if subnets is not None:
            subnets = [NetworkSubnet.from_dict(subnet) for subnet in subnets]
            data["subnets"] = subnets

        routes = data.get("routes", [])
        if routes is not None:
            routes = [NetworkRoute.from_dict(route) for route in routes]
            data["routes"] = routes

        # pylint: disable=import-outside-toplevel
        from ..servers import BoundServer

        servers = data.get("servers", [])
        if servers is not None:
            servers = [
                BoundServer(client._parent.servers, {"id": server}, complete=False)
                for server in servers
            ]
            data["servers"] = servers

        super().__init__(client, data, complete)

    def update(
        self,
        name: str | None = None,
        expose_routes_to_vswitch: bool | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundNetwork:
        """Updates a network. You can update a network’s name and a networks’s labels.

        :param name: str (optional)
               New name to set
        :param expose_routes_to_vswitch: Optional[bool]
                Indicates if the routes from this network should be exposed to the vSwitch connection.
                The exposing only takes effect if a vSwitch connection is active.
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
        """
        return self._client.update(
            self,
            name=name,
            expose_routes_to_vswitch=expose_routes_to_vswitch,
            labels=labels,
        )

    def delete(self) -> bool:
        """Deletes a network.

        :return: boolean
        """
        return self._client.delete(self)

    def get_actions_list(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """Returns all action objects for a network.

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
        """Returns all action objects for a network.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.get_actions(self, status=status, sort=sort)

    def add_subnet(self, subnet: NetworkSubnet) -> BoundAction:
        """Adds a subnet entry to a network.

        :param subnet: :class:`NetworkSubnet <hcloud.networks.domain.NetworkSubnet>`
                       The NetworkSubnet you want to add to the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.add_subnet(self, subnet=subnet)

    def delete_subnet(self, subnet: NetworkSubnet) -> BoundAction:
        """Removes a subnet entry from a network

        :param subnet: :class:`NetworkSubnet <hcloud.networks.domain.NetworkSubnet>`
                       The NetworkSubnet you want to remove from the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.delete_subnet(self, subnet=subnet)

    def add_route(self, route: NetworkRoute) -> BoundAction:
        """Adds a route entry to a network.

        :param route: :class:`NetworkRoute <hcloud.networks.domain.NetworkRoute>`
                    The NetworkRoute you want to add to the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.add_route(self, route=route)

    def delete_route(self, route: NetworkRoute) -> BoundAction:
        """Removes a route entry to a network.

        :param route: :class:`NetworkRoute <hcloud.networks.domain.NetworkRoute>`
                    The NetworkRoute you want to remove from the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.delete_route(self, route=route)

    def change_ip_range(self, ip_range: str) -> BoundAction:
        """Changes the IP range of a network.

        :param ip_range: str
                    The new prefix for the whole network.
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_ip_range(self, ip_range=ip_range)

    def change_protection(self, delete: bool | None = None) -> BoundAction:
        """Changes the protection configuration of a network.

        :param delete: boolean
               If True, prevents the network from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_protection(self, delete=delete)


class NetworksPageResult(NamedTuple):
    networks: list[BoundNetwork]
    meta: Meta


class NetworksClient(ResourceClientBase):
    _base_url = "/networks"

    actions: ResourceActionsClient
    """Networks scoped actions client

    :type: :class:`ResourceActionsClient <hcloud.actions.client.ResourceActionsClient>`
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.actions = ResourceActionsClient(client, self._base_url)

    def get_by_id(self, id: int) -> BoundNetwork:
        """Get a specific network

        :param id: int
        :return: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
        """
        response = self._client.request(url=f"{self._base_url}/{id}", method="GET")
        return BoundNetwork(self, response["network"])

    def get_list(
        self,
        name: str | None = None,
        label_selector: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> NetworksPageResult:
        """Get a list of networks from this account

        :param name: str (optional)
               Can be used to filter networks by their name.
        :param label_selector: str (optional)
               Can be used to filter networks by labels. The response will only contain networks matching the label selector.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if label_selector is not None:
            params["label_selector"] = label_selector
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url=self._base_url, method="GET", params=params)

        networks = [
            BoundNetwork(self, network_data) for network_data in response["networks"]
        ]
        return NetworksPageResult(networks, Meta.parse_meta(response))

    def get_all(
        self,
        name: str | None = None,
        label_selector: str | None = None,
    ) -> list[BoundNetwork]:
        """Get all networks from this account

        :param name: str (optional)
               Can be used to filter networks by their name.
        :param label_selector: str (optional)
               Can be used to filter networks by labels. The response will only contain networks matching the label selector.
        :return: List[:class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`]
        """
        return self._iter_pages(self.get_list, name=name, label_selector=label_selector)

    def get_by_name(self, name: str) -> BoundNetwork | None:
        """Get network by name

        :param name: str
               Used to get network by name.
        :return: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
        """
        return self._get_first_by(name=name)

    def create(
        self,
        name: str,
        ip_range: str,
        subnets: list[NetworkSubnet] | None = None,
        routes: list[NetworkRoute] | None = None,
        expose_routes_to_vswitch: bool | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundNetwork:
        """Creates a network with range ip_range.

        :param name: str
                Name of the network
        :param ip_range: str
                IP range of the whole network which must span all included subnets and route destinations
        :param subnets: List[:class:`NetworkSubnet <hcloud.networks.domain.NetworkSubnet>`]
                Array of subnets allocated
        :param routes: List[:class:`NetworkRoute <hcloud.networks.domain.NetworkRoute>`]
                Array of routes set in this network
        :param expose_routes_to_vswitch: Optional[bool]
                Indicates if the routes from this network should be exposed to the vSwitch connection.
                The exposing only takes effect if a vSwitch connection is active.
        :param labels: Dict[str, str] (optional)
                User-defined labels (key-value pairs)
        :return: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
        """
        data: dict[str, Any] = {"name": name, "ip_range": ip_range}
        if subnets is not None:
            data_subnets = []
            for subnet in subnets:
                data_subnet: dict[str, Any] = {
                    "type": subnet.type,
                    "ip_range": subnet.ip_range,
                    "network_zone": subnet.network_zone,
                }
                if subnet.vswitch_id is not None:
                    data_subnet["vswitch_id"] = subnet.vswitch_id

                data_subnets.append(data_subnet)
            data["subnets"] = data_subnets

        if routes is not None:
            data["routes"] = [
                {"destination": route.destination, "gateway": route.gateway}
                for route in routes
            ]

        if expose_routes_to_vswitch is not None:
            data["expose_routes_to_vswitch"] = expose_routes_to_vswitch

        if labels is not None:
            data["labels"] = labels

        response = self._client.request(url=self._base_url, method="POST", json=data)

        return BoundNetwork(self, response["network"])

    def update(
        self,
        network: Network | BoundNetwork,
        name: str | None = None,
        expose_routes_to_vswitch: bool | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundNetwork:
        """Updates a network. You can update a network’s name and a network’s labels.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param name: str (optional)
               New name to set
        :param expose_routes_to_vswitch: Optional[bool]
                Indicates if the routes from this network should be exposed to the vSwitch connection.
                The exposing only takes effect if a vSwitch connection is active.
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
        """
        data: dict[str, Any] = {}
        if name is not None:
            data.update({"name": name})

        if expose_routes_to_vswitch is not None:
            data["expose_routes_to_vswitch"] = expose_routes_to_vswitch

        if labels is not None:
            data.update({"labels": labels})

        response = self._client.request(
            url=f"{self._base_url}/{network.id}",
            method="PUT",
            json=data,
        )
        return BoundNetwork(self, response["network"])

    def delete(self, network: Network | BoundNetwork) -> bool:
        """Deletes a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :return: boolean
        """
        self._client.request(url=f"{self._base_url}/{network.id}", method="DELETE")
        return True

    def get_actions_list(
        self,
        network: Network | BoundNetwork,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """Returns all action objects for a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
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
            url=f"{self._base_url}/{network.id}/actions",
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
        network: Network | BoundNetwork,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """Returns all action objects for a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._iter_pages(
            self.get_actions_list,
            network,
            status=status,
            sort=sort,
        )

    def add_subnet(
        self,
        network: Network | BoundNetwork,
        subnet: NetworkSubnet,
    ) -> BoundAction:
        """Adds a subnet entry to a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param subnet: :class:`NetworkSubnet <hcloud.networks.domain.NetworkSubnet>`
                       The NetworkSubnet you want to add to the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {
            "type": subnet.type,
            "network_zone": subnet.network_zone,
        }
        if subnet.ip_range is not None:
            data["ip_range"] = subnet.ip_range
        if subnet.vswitch_id is not None:
            data["vswitch_id"] = subnet.vswitch_id

        response = self._client.request(
            url=f"{self._base_url}/{network.id}/actions/add_subnet",
            method="POST",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def delete_subnet(
        self,
        network: Network | BoundNetwork,
        subnet: NetworkSubnet,
    ) -> BoundAction:
        """Removes a subnet entry from a network

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param subnet: :class:`NetworkSubnet <hcloud.networks.domain.NetworkSubnet>`
                       The NetworkSubnet you want to remove from the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {"ip_range": subnet.ip_range}

        response = self._client.request(
            url=f"{self._base_url}/{network.id}/actions/delete_subnet",
            method="POST",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def add_route(
        self,
        network: Network | BoundNetwork,
        route: NetworkRoute,
    ) -> BoundAction:
        """Adds a route entry to a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param route: :class:`NetworkRoute <hcloud.networks.domain.NetworkRoute>`
                    The NetworkRoute you want to add to the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {
            "destination": route.destination,
            "gateway": route.gateway,
        }

        response = self._client.request(
            url=f"{self._base_url}/{network.id}/actions/add_route",
            method="POST",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def delete_route(
        self,
        network: Network | BoundNetwork,
        route: NetworkRoute,
    ) -> BoundAction:
        """Removes a route entry to a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param route: :class:`NetworkRoute <hcloud.networks.domain.NetworkRoute>`
                    The NetworkRoute you want to remove from the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {
            "destination": route.destination,
            "gateway": route.gateway,
        }

        response = self._client.request(
            url=f"{self._base_url}/{network.id}/actions/delete_route",
            method="POST",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def change_ip_range(
        self,
        network: Network | BoundNetwork,
        ip_range: str,
    ) -> BoundAction:
        """Changes the IP range of a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param ip_range: str
                    The new prefix for the whole network.
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {"ip_range": ip_range}

        response = self._client.request(
            url=f"{self._base_url}/{network.id}/actions/change_ip_range",
            method="POST",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def change_protection(
        self,
        network: Network | BoundNetwork,
        delete: bool | None = None,
    ) -> BoundAction:
        """Changes the protection configuration of a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param delete: boolean
               If True, prevents the network from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {}
        if delete is not None:
            data.update({"delete": delete})

        response = self._client.request(
            url=f"{self._base_url}/{network.id}/actions/change_protection",
            method="POST",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])
