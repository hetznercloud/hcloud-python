# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase, GetEntityByNameMixin
from hcloud.core.domain import add_meta_to_result

from hcloud.actions.client import BoundAction
from hcloud.networks.domain import Network


class BoundNetwork(BoundModelBase):
    model = Network

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

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
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


class NetworksClient(ClientEntityBase, GetEntityByNameMixin):
    results_list_attribute_name = 'networks'

    def get_by_id(self, id):
        # type: (int) -> BoundNetwork
        """Get a specific network

        :param id: int
        :return: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>
        """
        response = self._client.request(url="/networks/{network_id}".format(network_id=id), method="GET")
        return BoundNetwork(self, response['network'])

    def get_list(self,
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
        if name:
            params['name'] = name
        if label_selector:
            params['label_selector'] = label_selector
        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page

        response = self._client.request(url="/networks", method="GET", params=params)

        ass_networks = [BoundNetwork(self, network_data) for network_data in response['networks']]
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
        return super(NetworksClient, self).get_all(name=name, label_selector=label_selector)

    def get_by_name(self, name):
        # type: (str) -> BoundNetwork
        """Get network by name

        :param name: str
               Used to get network by name.
        :return: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>`
        """
        return super(NetworksClient, self).get_by_name(name)

    def create(self):
        #  TODO
        pass

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
        response = self._client.request(url="/networks/{network_id}".format(network_id=network.id), method="PUT", json=data)
        return BoundNetwork(self, response['network'])

    def delete(self, network):
        # type: (Network) -> BoundAction
        """Deletes a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(url="/networks/{network_id}".format(network_id=network.id), method="DELETE")
        return BoundAction(self._client.actions, response['action'])

    def get_actions_list(self, network, status=None, sort=None, page=None, per_page=None):
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

        response = self._client.request(url="/networks/{network_id}/actions".format(network_id=network.id), method="GET",
                                        params=params)
        actions = [BoundAction(self._client.actions, action_data) for action_data in response['actions']]
        return add_meta_to_result(actions, response, 'actions')

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
        return super(NetworksClient, self).get_actions(network, status=status, sort=sort)
