# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase, GetEntityByNameMixin
from hcloud.core.domain import add_meta_to_result

from hcloud.actions.client import BoundAction
from hcloud.networks.domain import Network, NetworkRoute, NetworkSubnet


class BoundNetwork(BoundModelBase):
    model = Network

    def __init__(self, client, data, complete=True):
        subnets = data.get("subnets", [])
        if subnets is not None:
            subnets = [NetworkSubnet.from_dict(subnet) for subnet in subnets]
            data["subnets"] = subnets

        routes = data.get("routes", [])
        if routes is not None:
            routes = [NetworkRoute.from_dict(route) for route in routes]
            data["routes"] = routes

        from hcloud.servers.client import BoundServer

        servers = data.get("servers", [])
        if servers is not None:
            servers = [
                BoundServer(client._client.servers, {"id": server}, complete=False)
                for server in servers
            ]
            data["servers"] = servers

        super(BoundNetwork, self).__init__(client, data, complete)

    def update(self, name=None, labels=None):
        # type: (Optional[str], Optional[Dict[str, str]]) -> BoundNetwork
        """Updates a network. You can update a network’s name and a networks’s labels.

        :param name: str (optional)
               New name to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
        """
        return self._client.update(self, name, labels)

    def delete(self):
        # type: () -> BoundAction
        """Deletes a network.

        :return: boolean
        """
        return self._client.delete(self)

    def get_actions_list(self, status=None, sort=None, page=None, per_page=None):
        # type: (Optional[List[str]], Optional[List[str]], Optional[int], Optional[int]) -> PageResults[List[BoundAction, Meta]]
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
        return self._client.get_actions_list(self, status, sort, page, per_page)

    def get_actions(self, status=None, sort=None):
        # type: (Optional[List[str]], Optional[List[str]]) -> List[BoundAction]
        """Returns all action objects for a network.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.get_actions(self, status, sort)

    def add_subnet(self, subnet):
        # type: (NetworkSubnet) -> List[BoundAction]
        """Adds a subnet entry to a network.

        :param subnet: :class:`NetworkSubnet <hcloud.networks.domain.NetworkSubnet>`
                       The NetworkSubnet you want to add to the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.add_subnet(self, subnet=subnet)

    def delete_subnet(self, subnet):
        # type: (NetworkSubnet) -> List[BoundAction]
        """Removes a subnet entry from a network

        :param subnet: :class:`NetworkSubnet <hcloud.networks.domain.NetworkSubnet>`
                       The NetworkSubnet you want to remove from the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.delete_subnet(self, subnet=subnet)

    def add_route(self, route):
        # type: (NetworkRoute) -> List[BoundAction]
        """Adds a route entry to a network.

        :param route: :class:`NetworkRoute <hcloud.networks.domain.NetworkRoute>`
                    The NetworkRoute you want to add to the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.add_route(self, route=route)

    def delete_route(self, route):
        # type: (NetworkRoute) -> List[BoundAction]
        """Removes a route entry to a network.

        :param route: :class:`NetworkRoute <hcloud.networks.domain.NetworkRoute>`
                    The NetworkRoute you want to remove from the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.delete_route(self, route=route)

    def change_ip_range(self, ip_range):
        # type: (str) -> List[BoundAction]
        """Changes the IP range of a network.

        :param ip_range: str
                    The new prefix for the whole network.
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_ip_range(self, ip_range=ip_range)

    def change_protection(self, delete=None):
        # type: (Optional[bool]) -> BoundAction
        """Changes the protection configuration of a network.

        :param delete: boolean
               If True, prevents the network from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_protection(self, delete=delete)


class NetworksClient(ClientEntityBase, GetEntityByNameMixin):
    results_list_attribute_name = "networks"

    def get_by_id(self, id):
        # type: (int) -> BoundNetwork
        """Get a specific network

        :param id: int
        :return: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>
        """
        response = self._client.request(
            url="/networks/{network_id}".format(network_id=id), method="GET"
        )
        return BoundNetwork(self, response["network"])

    def get_list(
        self,
        name=None,  # type: Optional[str]
        label_selector=None,  # type: Optional[str]
        page=None,  # type: Optional[int]
        per_page=None,  # type: Optional[int]
    ):
        # type: (...) -> PageResults[List[BoundNetwork], Meta]
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
        params = {}
        if name is not None:
            params["name"] = name
        if label_selector is not None:
            params["label_selector"] = label_selector
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url="/networks", method="GET", params=params)

        ass_networks = [
            BoundNetwork(self, network_data) for network_data in response["networks"]
        ]
        return self._add_meta_to_result(ass_networks, response)

    def get_all(self, name=None, label_selector=None):
        # type: (Optional[str], Optional[str]) -> List[BoundNetwork]
        """Get all networks from this account

        :param name: str (optional)
               Can be used to filter networks by their name.
        :param label_selector: str (optional)
               Can be used to filter networks by labels. The response will only contain networks matching the label selector.
        :return: List[:class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`]
        """
        return super(NetworksClient, self).get_all(
            name=name, label_selector=label_selector
        )

    def get_by_name(self, name):
        # type: (str) -> BoundNetwork
        """Get network by name

        :param name: str
               Used to get network by name.
        :return: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
        """
        return super(NetworksClient, self).get_by_name(name)

    def create(
        self,
        name,  # type: str
        ip_range,  # type: str
        subnets=None,  # type: Optional[List[NetworkSubnet]]
        routes=None,  # type:  Optional[List[NetworkRoute]]
        labels=None,  # type:  Optional[Dict[str, str]]
    ):
        """Creates a network with range ip_range.

        :param name: str
                Name of the network
        :param ip_range: str
                IP range of the whole network which must span all included subnets and route destinations
        :param subnets: List[:class:`NetworkSubnet <hcloud.networks.domain.NetworkSubnet>`]
                Array of subnets allocated
        :param routes: List[:class:`NetworkRoute <hcloud.networks.domain.NetworkRoute>`]
                Array of routes set in this network
        :param labels: Dict[str, str] (optional)
                User-defined labels (key-value pairs)
        :return: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
        """
        data = {"name": name, "ip_range": ip_range}
        if subnets is not None:
            data["subnets"] = [
                {
                    "type": subnet.type,
                    "ip_range": subnet.ip_range,
                    "network_zone": subnet.network_zone,
                }
                for subnet in subnets
            ]
        if routes is not None:
            data["routes"] = [
                {"destination": route.destination, "gateway": route.gateway}
                for route in routes
            ]
        if labels is not None:
            data["labels"] = labels

        response = self._client.request(url="/networks", method="POST", json=data)

        return BoundNetwork(self, response["network"])

    def update(self, network, name=None, labels=None):
        # type:(Network,  Optional[str],  Optional[Dict[str, str]]) -> BoundNetwork
        """Updates a network. You can update a network’s name and a network’s labels.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param name: str (optional)
               New name to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
        """
        data = {}
        if name is not None:
            data.update({"name": name})
        if labels is not None:
            data.update({"labels": labels})
        response = self._client.request(
            url="/networks/{network_id}".format(network_id=network.id),
            method="PUT",
            json=data,
        )
        return BoundNetwork(self, response["network"])

    def delete(self, network):
        # type: (Network) -> BoundAction
        """Deletes a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :return: boolean
        """
        self._client.request(
            url="/networks/{network_id}".format(network_id=network.id), method="DELETE"
        )
        return True

    def get_actions_list(
        self, network, status=None, sort=None, page=None, per_page=None
    ):
        # type: (Network, Optional[List[str]], Optional[List[str]], Optional[int], Optional[int]) -> PageResults[List[BoundAction], Meta]
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
            url="/networks/{network_id}/actions".format(network_id=network.id),
            method="GET",
            params=params,
        )
        actions = [
            BoundAction(self._client.actions, action_data)
            for action_data in response["actions"]
        ]
        return add_meta_to_result(actions, response, "actions")

    def get_actions(self, network, status=None, sort=None):
        # type: (Network, Optional[List[str]], Optional[List[str]]) -> List[BoundAction]
        """Returns all action objects for a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return super(NetworksClient, self).get_actions(
            network, status=status, sort=sort
        )

    def add_subnet(self, network, subnet):
        # type: (Union[Network, BoundNetwork], NetworkSubnet) -> List[BoundAction]
        """Adds a subnet entry to a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param subnet: :class:`NetworkSubnet <hcloud.networks.domain.NetworkSubnet>`
                       The NetworkSubnet you want to add to the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {
            "type": subnet.type,
            "network_zone": subnet.network_zone,
        }
        if subnet.ip_range is not None:
            data["ip_range"] = subnet.ip_range
        if subnet.vswitch_id is not None:
            data["vswitch_id"] = subnet.vswitch_id

        response = self._client.request(
            url="/networks/{network_id}/actions/add_subnet".format(
                network_id=network.id
            ),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def delete_subnet(self, network, subnet):
        # type: (Union[Network, BoundNetwork], NetworkSubnet) -> List[BoundAction]
        """Removes a subnet entry from a network

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param subnet: :class:`NetworkSubnet <hcloud.networks.domain.NetworkSubnet>`
                       The NetworkSubnet you want to remove from the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {
            "ip_range": subnet.ip_range,
        }

        response = self._client.request(
            url="/networks/{network_id}/actions/delete_subnet".format(
                network_id=network.id
            ),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def add_route(self, network, route):
        # type: (Union[Network, BoundNetwork], NetworkRoute) -> List[BoundAction]
        """Adds a route entry to a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param route: :class:`NetworkRoute <hcloud.networks.domain.NetworkRoute>`
                    The NetworkRoute you want to add to the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {
            "destination": route.destination,
            "gateway": route.gateway,
        }

        response = self._client.request(
            url="/networks/{network_id}/actions/add_route".format(
                network_id=network.id
            ),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def delete_route(self, network, route):
        # type: (Union[Network, BoundNetwork], NetworkRoute) -> List[BoundAction]
        """Removes a route entry to a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param route: :class:`NetworkRoute <hcloud.networks.domain.NetworkRoute>`
                    The NetworkRoute you want to remove from the Network
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {
            "destination": route.destination,
            "gateway": route.gateway,
        }

        response = self._client.request(
            url="/networks/{network_id}/actions/delete_route".format(
                network_id=network.id
            ),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def change_ip_range(self, network, ip_range):
        # type: (Union[Network, BoundNetwork], str) -> List[BoundAction]
        """Changes the IP range of a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param ip_range: str
                    The new prefix for the whole network.
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {
            "ip_range": ip_range,
        }

        response = self._client.request(
            url="/networks/{network_id}/actions/change_ip_range".format(
                network_id=network.id
            ),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def change_protection(self, network, delete=None):
        # type: (Union[Network, BoundNetwork], Optional[bool]) -> BoundAction
        """Changes the protection configuration of a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param delete: boolean
               If True, prevents the network from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {}
        if delete is not None:
            data.update({"delete": delete})

        response = self._client.request(
            url="/networks/{network_id}/actions/change_protection".format(
                network_id=network.id
            ),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])
