# -*- coding: utf-8 -*-
from hcloud.actions.client import BoundAction
from hcloud.core.client import BoundModelBase, ClientEntityBase, GetEntityByNameMixin
from hcloud.core.domain import add_meta_to_result

from hcloud.firewalls.domain import (
    Firewall,
    CreateFirewallResponse,
    FirewallRule,
    FirewallResource,
    FirewallResourceLabelSelector,
)


class BoundFirewall(BoundModelBase):
    model = Firewall

    def __init__(self, client, data, complete=True):
        rules = data.get("rules", [])
        if rules:
            rules = [
                FirewallRule(
                    direction=rule["direction"],
                    source_ips=rule["source_ips"],
                    destination_ips=rule["destination_ips"],
                    protocol=rule["protocol"],
                    port=rule["port"],
                    description=rule["description"],
                )
                for rule in rules
            ]
            data["rules"] = rules

        applied_to = data.get("applied_to", [])
        if applied_to:
            from hcloud.servers.client import BoundServer

            ats = []
            for a in applied_to:
                if a["type"] == FirewallResource.TYPE_SERVER:
                    ats.append(
                        FirewallResource(
                            type=a["type"],
                            server=BoundServer(
                                client._client.servers, a["server"], complete=False
                            ),
                        )
                    )
                elif a["type"] == FirewallResource.TYPE_LABEL_SELECTOR:
                    ats.append(
                        FirewallResource(
                            type=a["type"],
                            label_selector=FirewallResourceLabelSelector(
                                selector=a["label_selector"]["selector"]
                            ),
                        )
                    )
            data["applied_to"] = ats

        super(BoundFirewall, self).__init__(client, data, complete)

    def get_actions_list(self, status=None, sort=None, page=None, per_page=None):
        # type: (Optional[List[str]], Optional[List[str]], Optional[int], Optional[int]) -> PageResult[BoundAction, Meta]
        """Returns all action objects for a Firewall.

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
        """Returns all action objects for a Firewall.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`

        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.get_actions(self, status, sort)

    def update(self, name=None, labels=None):
        # type: (Optional[str], Optional[Dict[str, str]], Optional[str]) -> BoundFirewall
        """Updates the name or labels of a Firewall.

        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str (optional)
               New Name to set
        :return: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>`
        """
        return self._client.update(self, labels, name)

    def delete(self):
        # type: () -> bool
        """Deletes a Firewall.

        :return: boolean
        """
        return self._client.delete(self)

    def set_rules(self, rules):
        # type: (List[FirewallRule]) -> List[BoundAction]
        """Sets the rules of a Firewall. All existing rules will be overwritten. Pass an empty rules array to remove all rules.
        :param rules: List[:class:`FirewallRule <hcloud.firewalls.domain.FirewallRule>`]
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """

        return self._client.set_rules(self, rules)

    def apply_to_resources(self, resources):
        # type: (List[FirewallResource]) -> List[BoundAction]
        """Applies one Firewall to multiple resources.
        :param resources: List[:class:`FirewallResource <hcloud.firewalls.domain.FirewallResource>`]
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.apply_to_resources(self, resources)

    def remove_from_resources(self, resources):
        # type: (List[FirewallResource]) -> List[BoundAction]
        """Removes one Firewall from multiple resources.
        :param resources: List[:class:`FirewallResource <hcloud.firewalls.domain.FirewallResource>`]
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.remove_from_resources(self, resources)


class FirewallsClient(ClientEntityBase, GetEntityByNameMixin):
    results_list_attribute_name = "firewalls"

    def get_actions_list(
        self,
        firewall,  # type: Firewall
        status=None,  # type: Optional[List[str]]
        sort=None,  # type: Optional[List[str]]
        page=None,  # type: Optional[int]
        per_page=None,  # type: Optional[int]
    ):
        # type: (...) -> PageResults[List[BoundAction], Meta]
        """Returns all action objects for a Firewall.

        :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>` or  :class:`Firewall <hcloud.firewalls.domain.Firewall>`
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
            url="/firewalls/{firewall_id}/actions".format(firewall_id=firewall.id),
            method="GET",
            params=params,
        )
        actions = [
            BoundAction(self._client.actions, action_data)
            for action_data in response["actions"]
        ]
        return add_meta_to_result(actions, response, "actions")

    def get_actions(
        self,
        firewall,  # type: Firewall
        status=None,  # type: Optional[List[str]]
        sort=None,  # type: Optional[List[str]]
    ):
        # type: (...) -> List[BoundAction]
        """Returns all action objects for a Firewall.

        :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>` or  :class:`Firewall <hcloud.firewalls.domain.Firewall>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`

        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return super(FirewallsClient, self).get_actions(
            firewall, status=status, sort=sort
        )

    def get_by_id(self, id):
        # type: (int) -> BoundFirewall
        """Returns a specific Firewall object.

        :param id: int
        :return: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>`
        """
        response = self._client.request(
            url="/firewalls/{firewall_id}".format(firewall_id=id), method="GET"
        )
        return BoundFirewall(self, response["firewall"])

    def get_list(
        self,
        label_selector=None,  # type: Optional[str]
        page=None,  # type: Optional[int]
        per_page=None,  # type: Optional[int]
        name=None,  # type: Optional[str]
        sort=None,  # type: Optional[List[str]]
    ):
        # type: (...) -> PageResults[List[BoundFirewall]]
        """Get a list of floating ips from this account

        :param label_selector: str (optional)
               Can be used to filter Firewalls by labels. The response will only contain Firewalls matching the label selector values.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :param name: str (optional)
               Can be used to filter networks by their name.
        :param sort: List[str] (optional)
               Choices: id name created (You can add one of ":asc", ":desc" to modify sort order. ( ":asc" is default))
        :return: (List[:class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params = {}

        if label_selector is not None:
            params["label_selector"] = label_selector
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if name is not None:
            params["name"] = name
        if sort is not None:
            params["sort"] = sort
        response = self._client.request(url="/firewalls", method="GET", params=params)
        firewalls = [
            BoundFirewall(self, firewall_data)
            for firewall_data in response["firewalls"]
        ]

        return self._add_meta_to_result(firewalls, response)

    def get_all(self, label_selector=None, name=None, sort=None):
        # type: (Optional[str], Optional[str],  Optional[List[str]]) -> List[BoundFirewall]
        """Get all floating ips from this account

        :param label_selector: str (optional)
               Can be used to filter Firewalls by labels. The response will only contain Firewalls matching the label selector values.
        :param name: str (optional)
               Can be used to filter networks by their name.
        :param sort: List[str] (optional)
               Choices: id name created (You can add one of ":asc", ":desc" to modify sort order. ( ":asc" is default))
        :return: List[:class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>`]
        """
        return super(FirewallsClient, self).get_all(
            label_selector=label_selector, name=name, sort=sort
        )

    def get_by_name(self, name):
        # type: (str) -> BoundFirewall
        """Get Firewall by name

        :param name: str
               Used to get Firewall by name.
        :return: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>`
        """
        return super(FirewallsClient, self).get_by_name(name)

    def create(
        self,
        name,  # type: str
        rules=None,  # type: Optional[List[FirewallRule]]
        labels=None,  # type: Optional[str]
        resources=None,  # type: Optional[List[FirewallResource]]
    ):
        # type: (...) -> CreateFirewallResponse
        """Creates a new Firewall.

        :param name: str
               Firewall Name
        :param rules: List[:class:`FirewallRule <hcloud.firewalls.domain.FirewallRule>`] (optional)
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param resources: List[:class:`FirewallResource <hcloud.firewalls.domain.FirewallResource>`] (optional)
        :return: :class:`CreateFirewallResponse <hcloud.firewalls.domain.CreateFirewallResponse>`
        """

        data = {"name": name}
        if labels is not None:
            data["labels"] = labels

        if rules is not None:
            data.update({"rules": []})
            for rule in rules:
                data["rules"].append(rule.to_payload())
        if resources is not None:
            data.update({"apply_to": []})
            for resource in resources:
                data["apply_to"].append(resource.to_payload())
        response = self._client.request(url="/firewalls", json=data, method="POST")

        actions = []
        if response.get("actions") is not None:
            actions = [
                BoundAction(self._client.actions, _) for _ in response["actions"]
            ]

        result = CreateFirewallResponse(
            firewall=BoundFirewall(self, response["firewall"]), actions=actions
        )
        return result

    def update(self, firewall, labels=None, name=None):
        # type: (Firewall,   Optional[Dict[str, str]], Optional[str]) -> BoundFirewall
        """Updates the description or labels of a Firewall.

        :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>` or  :class:`Firewall <hcloud.firewalls.domain.Firewall>`
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str (optional)
               New name to set
        :return: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>`
        """
        data = {}
        if labels is not None:
            data["labels"] = labels
        if name is not None:
            data["name"] = name

        response = self._client.request(
            url="/firewalls/{firewall_id}".format(firewall_id=firewall.id),
            method="PUT",
            json=data,
        )
        return BoundFirewall(self, response["firewall"])

    def delete(self, firewall):
        # type: (Firewall) -> bool
        """Deletes a Firewall.

        :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>` or  :class:`Firewall <hcloud.firewalls.domain.Firewall>`
        :return: boolean
        """
        self._client.request(
            url="/firewalls/{firewall_id}".format(firewall_id=firewall.id),
            method="DELETE",
        )
        # Return always true, because the API does not return an action for it. When an error occurs a HcloudAPIException will be raised
        return True

    def set_rules(self, firewall, rules):
        # type: (Firewall, List[FirewallRule]) -> List[BoundAction]
        """Sets the rules of a Firewall. All existing rules will be overwritten. Pass an empty rules array to remove all rules.

        :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>` or  :class:`Firewall <hcloud.firewalls.domain.Firewall>`
        :param rules: List[:class:`FirewallRule <hcloud.firewalls.domain.FirewallRule>`]
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        data = {"rules": []}
        for rule in rules:
            data["rules"].append(rule.to_payload())
        response = self._client.request(
            url="/firewalls/{firewall_id}/actions/set_rules".format(
                firewall_id=firewall.id
            ),
            method="POST",
            json=data,
        )
        return [BoundAction(self._client.actions, _) for _ in response["actions"]]

    def apply_to_resources(self, firewall, resources):
        # type: (Firewall, List[FirewallResource]) -> List[BoundAction]
        """Applies one Firewall to multiple resources.

        :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>` or  :class:`Firewall <hcloud.firewalls.domain.Firewall>`
        :param resources: List[:class:`FirewallResource <hcloud.firewalls.domain.FirewallResource>`]
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        data = {"apply_to": []}
        for resource in resources:
            data["apply_to"].append(resource.to_payload())
        response = self._client.request(
            url="/firewalls/{firewall_id}/actions/apply_to_resources".format(
                firewall_id=firewall.id
            ),
            method="POST",
            json=data,
        )
        return [BoundAction(self._client.actions, _) for _ in response["actions"]]

    def remove_from_resources(self, firewall, resources):
        # type: (Firewall, List[FirewallResource]) -> List[BoundAction]
        """Removes one Firewall from multiple resources.

        :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>` or  :class:`Firewall <hcloud.firewalls.domain.Firewall>`
        :param resources: List[:class:`FirewallResource <hcloud.firewalls.domain.FirewallResource>`]
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        data = {"remove_from": []}
        for resource in resources:
            data["remove_from"].append(resource.to_payload())
        response = self._client.request(
            url="/firewalls/{firewall_id}/actions/remove_from_resources".format(
                firewall_id=firewall.id
            ),
            method="POST",
            json=data,
        )
        return [BoundAction(self._client.actions, _) for _ in response["actions"]]
