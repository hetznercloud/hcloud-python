from __future__ import annotations

from typing import Any, NamedTuple

from ..actions import BoundAction
from ..core import BoundModelBase, Meta, ResourceClientBase
from .domain import CreatePlacementGroupResponse, PlacementGroup


class BoundPlacementGroup(BoundModelBase, PlacementGroup):
    _client: PlacementGroupsClient

    model = PlacementGroup

    def update(
        self,
        labels: dict[str, str] | None = None,
        name: str | None = None,
    ) -> BoundPlacementGroup:
        """Updates the name or labels of a Placement Group

        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str, (optional)
               New Name to set
        :return: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>`
        """
        return self._client.update(self, labels=labels, name=name)

    def delete(self) -> bool:
        """Deletes a Placement Group

        :return: boolean
        """
        return self._client.delete(self)


class PlacementGroupsPageResult(NamedTuple):
    placement_groups: list[BoundPlacementGroup]
    meta: Meta


class PlacementGroupsClient(ResourceClientBase):
    _base_url = "/placement_groups"

    def get_by_id(self, id: int) -> BoundPlacementGroup:
        """Returns a specific Placement Group object

        :param id: int
        :return: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>`
        """
        response = self._client.request(
            url=f"{self._base_url}/{id}",
            method="GET",
        )
        return BoundPlacementGroup(self, response["placement_group"])

    def get_list(
        self,
        label_selector: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        name: str | None = None,
        sort: list[str] | None = None,
        type: str | None = None,
    ) -> PlacementGroupsPageResult:
        """Get a list of Placement Groups

        :param label_selector: str (optional)
               Can be used to filter Placement Groups by labels. The response will only contain Placement Groups matching the label selector values.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :param name: str (optional)
               Can be used to filter Placement Groups by their name.
        :param sort: List[str] (optional)
               Choices: id name created (You can add one of ":asc", ":desc" to modify sort order. ( ":asc" is default))
        :return: (List[:class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>`], :class:`Meta <hcloud.core.domain.Meta>`)
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
        if type is not None:
            params["type"] = type
        response = self._client.request(url=self._base_url, method="GET", params=params)
        placement_groups = [
            BoundPlacementGroup(self, placement_group_data)
            for placement_group_data in response["placement_groups"]
        ]

        return PlacementGroupsPageResult(placement_groups, Meta.parse_meta(response))

    def get_all(
        self,
        label_selector: str | None = None,
        name: str | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundPlacementGroup]:
        """Get all Placement Groups

        :param label_selector: str (optional)
               Can be used to filter Placement Groups by labels. The response will only contain Placement Groups matching the label selector values.
        :param name: str (optional)
               Can be used to filter Placement Groups by their name.
        :param sort: List[str] (optional)
               Choices: id name created (You can add one of ":asc", ":desc" to modify sort order. ( ":asc" is default))
        :return: List[:class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>`]
        """
        return self._iter_pages(
            self.get_list,
            label_selector=label_selector,
            name=name,
            sort=sort,
        )

    def get_by_name(self, name: str) -> BoundPlacementGroup | None:
        """Get Placement Group by name

        :param name: str
               Used to get Placement Group by name
        :return: class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>`
        """
        return self._get_first_by(name=name)

    def create(
        self,
        name: str,
        type: str,
        labels: dict[str, str] | None = None,
    ) -> CreatePlacementGroupResponse:
        """Creates a new Placement Group.

        :param name: str
               Placement Group Name
        :param type: str
               Type of the Placement Group
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)

        :return: :class:`CreatePlacementGroupResponse <hcloud.placement_groups.domain.CreatePlacementGroupResponse>`
        """
        data: dict[str, Any] = {"name": name, "type": type}
        if labels is not None:
            data["labels"] = labels
        response = self._client.request(url=self._base_url, json=data, method="POST")

        action = None
        if response.get("action") is not None:
            action = BoundAction(self._parent.actions, response["action"])

        result = CreatePlacementGroupResponse(
            placement_group=BoundPlacementGroup(self, response["placement_group"]),
            action=action,
        )
        return result

    def update(
        self,
        placement_group: PlacementGroup | BoundPlacementGroup,
        labels: dict[str, str] | None = None,
        name: str | None = None,
    ) -> BoundPlacementGroup:
        """Updates the description or labels of a Placement Group.

        :param placement_group: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>` or :class:`PlacementGroup <hcloud.placement_groups.domain.PlacementGroup>`
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str (optional)
               New name to set
        :return: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>`
        """

        data: dict[str, Any] = {}
        if labels is not None:
            data["labels"] = labels
        if name is not None:
            data["name"] = name

        response = self._client.request(
            url=f"{self._base_url}/{placement_group.id}",
            method="PUT",
            json=data,
        )
        return BoundPlacementGroup(self, response["placement_group"])

    def delete(self, placement_group: PlacementGroup | BoundPlacementGroup) -> bool:
        """Deletes a Placement Group.

        :param placement_group: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>` or :class:`PlacementGroup <hcloud.placement_groups.domain.PlacementGroup>`
        :return: boolean
        """
        self._client.request(
            url=f"{self._base_url}/{placement_group.id}",
            method="DELETE",
        )
        return True
