from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

from ..actions import ActionsPageResult, BoundAction, ResourceActionsClient
from ..core import BoundModelBase, ClientEntityBase, Meta
from .domain import (
    CreateFirewallResponse,
    Firewall,
    FirewallResource,
    FirewallResourceAppliedToResources,
    FirewallResourceLabelSelector,
    FirewallRule,
)

if TYPE_CHECKING:
    from .._client import Client


class BoundFirewall(BoundModelBase, Firewall):
    _client: FirewallsClient

    model = Firewall

    def __init__(self, client: FirewallsClient, data: dict, complete: bool = True):
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
            # pylint: disable=import-outside-toplevel
            from ..servers import BoundServer

            data_applied_to = []
            for firewall_resource in applied_to:
                applied_to_resources = None
                if firewall_resource.get("applied_to_resources"):
                    applied_to_resources = [
                        FirewallResourceAppliedToResources(
                            type=resource["type"],
                            server=(
                                BoundServer(
                                    client._client.servers,
                                    resource.get("server"),
                                    complete=False,
                                )
                                if resource.get("server") is not None
                                else None
                            ),
                        )
                        for resource in firewall_resource.get("applied_to_resources")
                    ]

                if firewall_resource["type"] == FirewallResource.TYPE_SERVER:
                    data_applied_to.append(
                        FirewallResource(
                            type=firewall_resource["type"],
                            server=BoundServer(
                                client._client.servers,
                                firewall_resource["server"],
                                complete=False,
                            ),
                            applied_to_resources=applied_to_resources,
                        )
                    )
                elif firewall_resource["type"] == FirewallResource.TYPE_LABEL_SELECTOR:
                    data_applied_to.append(
                        FirewallResource(
                            type=firewall_resource["type"],
                            label_selector=FirewallResourceLabelSelector(
                                selector=firewall_resource["label_selector"]["selector"]
                            ),
                            applied_to_resources=applied_to_resources,
                        )
                    )

            data["applied_to"] = data_applied_to

        super().__init__(client, data, complete)

    def get_actions_list(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
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

    def get_actions(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """Returns all action objects for a Firewall.

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
    ) -> BoundFirewall:
        """Updates the name or labels of a Firewall.

        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str (optional)
               New Name to set
        :return: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>`
        """
        return self._client.update(self, labels, name)

    def delete(self) -> bool:
        """Deletes a Firewall.

        :return: boolean
        """
        return self._client.delete(self)

    def set_rules(self, rules: list[FirewallRule]) -> list[BoundAction]:
        """Sets the rules of a Firewall. All existing rules will be overwritten. Pass an empty rules array to remove all rules.
        :param rules: List[:class:`FirewallRule <hcloud.firewalls.domain.FirewallRule>`]
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """

        return self._client.set_rules(self, rules)

    def apply_to_resources(
        self,
        resources: list[FirewallResource],
    ) -> list[BoundAction]:
        """Applies one Firewall to multiple resources.
        :param resources: List[:class:`FirewallResource <hcloud.firewalls.domain.FirewallResource>`]
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.apply_to_resources(self, resources)

    def remove_from_resources(
        self,
        resources: list[FirewallResource],
    ) -> list[BoundAction]:
        """Removes one Firewall from multiple resources.
        :param resources: List[:class:`FirewallResource <hcloud.firewalls.domain.FirewallResource>`]
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.remove_from_resources(self, resources)


class FirewallsPageResult(NamedTuple):
    firewalls: list[BoundFirewall]
    meta: Meta | None


class FirewallsClient(ClientEntityBase):
    _client: Client

    actions: ResourceActionsClient
    """Firewalls scoped actions client

    :type: :class:`ResourceActionsClient <hcloud.actions.client.ResourceActionsClient>`
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.actions = ResourceActionsClient(client, "/firewalls")

    def get_actions_list(
        self,
        firewall: Firewall | BoundFirewall,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
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
            url=f"/firewalls/{firewall.id}/actions",
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
        firewall: Firewall | BoundFirewall,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """Returns all action objects for a Firewall.

        :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>` or  :class:`Firewall <hcloud.firewalls.domain.Firewall>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`

        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._iter_pages(
            self.get_actions_list,
            firewall,
            status=status,
            sort=sort,
        )

    def get_by_id(self, id: int) -> BoundFirewall:
        """Returns a specific Firewall object.

        :param id: int
        :return: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>`
        """
        response = self._client.request(url=f"/firewalls/{id}", method="GET")
        return BoundFirewall(self, response["firewall"])

    def get_list(
        self,
        label_selector: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        name: str | None = None,
        sort: list[str] | None = None,
    ) -> FirewallsPageResult:
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
        params: dict[str, Any] = {}

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

        return FirewallsPageResult(firewalls, Meta.parse_meta(response))

    def get_all(
        self,
        label_selector: str | None = None,
        name: str | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundFirewall]:
        """Get all floating ips from this account

        :param label_selector: str (optional)
               Can be used to filter Firewalls by labels. The response will only contain Firewalls matching the label selector values.
        :param name: str (optional)
               Can be used to filter networks by their name.
        :param sort: List[str] (optional)
               Choices: id name created (You can add one of ":asc", ":desc" to modify sort order. ( ":asc" is default))
        :return: List[:class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>`]
        """
        return self._iter_pages(
            self.get_list,
            label_selector=label_selector,
            name=name,
            sort=sort,
        )

    def get_by_name(self, name: str) -> BoundFirewall | None:
        """Get Firewall by name

        :param name: str
               Used to get Firewall by name.
        :return: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>`
        """
        return self._get_first_by(name=name)

    def create(
        self,
        name: str,
        rules: list[FirewallRule] | None = None,
        labels: str | None = None,
        resources: list[FirewallResource] | None = None,
    ) -> CreateFirewallResponse:
        """Creates a new Firewall.

        :param name: str
               Firewall Name
        :param rules: List[:class:`FirewallRule <hcloud.firewalls.domain.FirewallRule>`] (optional)
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param resources: List[:class:`FirewallResource <hcloud.firewalls.domain.FirewallResource>`] (optional)
        :return: :class:`CreateFirewallResponse <hcloud.firewalls.domain.CreateFirewallResponse>`
        """

        data: dict[str, Any] = {"name": name}
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
                BoundAction(self._client.actions, action_data)
                for action_data in response["actions"]
            ]

        result = CreateFirewallResponse(
            firewall=BoundFirewall(self, response["firewall"]), actions=actions
        )
        return result

    def update(
        self,
        firewall: Firewall | BoundFirewall,
        labels: dict[str, str] | None = None,
        name: str | None = None,
    ) -> BoundFirewall:
        """Updates the description or labels of a Firewall.

        :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>` or  :class:`Firewall <hcloud.firewalls.domain.Firewall>`
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str (optional)
               New name to set
        :return: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>`
        """
        data: dict[str, Any] = {}
        if labels is not None:
            data["labels"] = labels
        if name is not None:
            data["name"] = name

        response = self._client.request(
            url=f"/firewalls/{firewall.id}",
            method="PUT",
            json=data,
        )
        return BoundFirewall(self, response["firewall"])

    def delete(self, firewall: Firewall | BoundFirewall) -> bool:
        """Deletes a Firewall.

        :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>` or  :class:`Firewall <hcloud.firewalls.domain.Firewall>`
        :return: boolean
        """
        self._client.request(
            url=f"/firewalls/{firewall.id}",
            method="DELETE",
        )
        # Return always true, because the API does not return an action for it. When an error occurs a HcloudAPIException will be raised
        return True

    def set_rules(
        self,
        firewall: Firewall | BoundFirewall,
        rules: list[FirewallRule],
    ) -> list[BoundAction]:
        """Sets the rules of a Firewall. All existing rules will be overwritten. Pass an empty rules array to remove all rules.

        :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>` or  :class:`Firewall <hcloud.firewalls.domain.Firewall>`
        :param rules: List[:class:`FirewallRule <hcloud.firewalls.domain.FirewallRule>`]
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        data: dict[str, Any] = {"rules": []}
        for rule in rules:
            data["rules"].append(rule.to_payload())
        response = self._client.request(
            url=f"/firewalls/{firewall.id}/actions/set_rules",
            method="POST",
            json=data,
        )
        return [
            BoundAction(self._client.actions, action_data)
            for action_data in response["actions"]
        ]

    def apply_to_resources(
        self,
        firewall: Firewall | BoundFirewall,
        resources: list[FirewallResource],
    ) -> list[BoundAction]:
        """Applies one Firewall to multiple resources.

        :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>` or  :class:`Firewall <hcloud.firewalls.domain.Firewall>`
        :param resources: List[:class:`FirewallResource <hcloud.firewalls.domain.FirewallResource>`]
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        data: dict[str, Any] = {"apply_to": []}
        for resource in resources:
            data["apply_to"].append(resource.to_payload())
        response = self._client.request(
            url=f"/firewalls/{firewall.id}/actions/apply_to_resources",
            method="POST",
            json=data,
        )
        return [
            BoundAction(self._client.actions, action_data)
            for action_data in response["actions"]
        ]

    def remove_from_resources(
        self,
        firewall: Firewall | BoundFirewall,
        resources: list[FirewallResource],
    ) -> list[BoundAction]:
        """Removes one Firewall from multiple resources.

        :param firewall: :class:`BoundFirewall <hcloud.firewalls.client.BoundFirewall>` or  :class:`Firewall <hcloud.firewalls.domain.Firewall>`
        :param resources: List[:class:`FirewallResource <hcloud.firewalls.domain.FirewallResource>`]
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        data: dict[str, Any] = {"remove_from": []}
        for resource in resources:
            data["remove_from"].append(resource.to_payload())
        response = self._client.request(
            url=f"/firewalls/{firewall.id}/actions/remove_from_resources",
            method="POST",
            json=data,
        )
        return [
            BoundAction(self._client.actions, action_data)
            for action_data in response["actions"]
        ]
