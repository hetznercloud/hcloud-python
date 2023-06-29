from ..actions.client import BoundAction
from ..core.client import BoundModelBase, ClientEntityBase, GetEntityByNameMixin
from .domain import CreatePlacementGroupResponse, PlacementGroup


class BoundPlacementGroup(BoundModelBase):
    model = PlacementGroup

    def update(self, labels=None, name=None):
        # type: (Optional[str], Optional[Dict[str, str]], Optional[str]) -> BoundPlacementGroup
        """Updates the name or labels of a Placement Group

        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str, (optional)
               New Name to set
        :return: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>`
        """
        return self._client.update(self, labels, name)

    def delete(self):
        # type: () -> bool
        """Deletes a Placement Group

        :return: boolean
        """
        return self._client.delete(self)


class PlacementGroupsClient(ClientEntityBase, GetEntityByNameMixin):
    results_list_attribute_name = "placement_groups"

    def get_by_id(self, id):
        # type: (int) -> BoundPlacementGroup
        """Returns a specific Placement Group object

        :param id: int
        :return: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>`
        """
        response = self._client.request(
            url=f"/placement_groups/{id}",
            method="GET",
        )
        return BoundPlacementGroup(self, response["placement_group"])

    def get_list(
        self,
        label_selector=None,  # type: Optional[str]
        page=None,  # type: Optional[int]
        per_page=None,  # type: Optional[int]
        name=None,  # type: Optional[str]
        sort=None,  # type: Optional[List[str]]
        type=None,  # type: Optional[str]
    ):
        # type: (...) -> PageResults[List[BoundPlacementGroup]]
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
        if type is not None:
            params["type"] = type
        response = self._client.request(
            url="/placement_groups", method="GET", params=params
        )
        placement_groups = [
            BoundPlacementGroup(self, placement_group_data)
            for placement_group_data in response["placement_groups"]
        ]

        return self._add_meta_to_result(placement_groups, response)

    def get_all(self, label_selector=None, name=None, sort=None):
        # type: (Optional[str], Optional[str],  Optional[List[str]]) -> List[BoundPlacementGroup]
        """Get all Placement Groups

        :param label_selector: str (optional)
               Can be used to filter Placement Groups by labels. The response will only contain Placement Groups matching the label selector values.
        :param name: str (optional)
               Can be used to filter Placement Groups by their name.
        :param sort: List[str] (optional)
               Choices: id name created (You can add one of ":asc", ":desc" to modify sort order. ( ":asc" is default))
        :return: List[:class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>`]
        """
        return super().get_all(label_selector=label_selector, name=name, sort=sort)

    def get_by_name(self, name):
        # type: (str) -> BoundPlacementGroup
        """Get Placement Group by name

        :param name: str
               Used to get Placement Group by name
        :return: class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>`
        """
        return super().get_by_name(name)

    def create(
        self,
        name,  # type: str
        type,  # type: str
        labels=None,  # type: Optional[Dict[str, str]]
    ):
        # type: (...) -> CreatePlacementGroupResponse
        """Creates a new Placement Group.

        :param name: str
               Placement Group Name
        :param type: str
               Type of the Placement Group
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)

        :return: :class:`CreatePlacementGroupResponse <hcloud.placement_groups.domain.CreatePlacementGroupResponse>`
        """
        data = {"name": name, "type": type}
        if labels is not None:
            data["labels"] = labels
        response = self._client.request(
            url="/placement_groups", json=data, method="POST"
        )

        action = None
        if response.get("action") is not None:
            action = BoundAction(self._client.action, response["action"])

        result = CreatePlacementGroupResponse(
            placement_group=BoundPlacementGroup(self, response["placement_group"]),
            action=action,
        )
        return result

    def update(self, placement_group, labels=None, name=None):
        # type: (PlacementGroup, Optional[Dict[str, str]], Optional[str]) -> BoundPlacementGroup
        """Updates the description or labels of a Placement Group.

        :param placement_group: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>` or :class:`PlacementGroup <hcloud.placement_groups.domain.PlacementGroup>`
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str (optional)
               New name to set
        :return: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>`
        """

        data = {}
        if labels is not None:
            data["labels"] = labels
        if name is not None:
            data["name"] = name

        response = self._client.request(
            url="/placement_groups/{placement_group_id}".format(
                placement_group_id=placement_group.id
            ),
            method="PUT",
            json=data,
        )
        return BoundPlacementGroup(self, response["placement_group"])

    def delete(self, placement_group):
        # type: (PlacementGroup) -> bool
        """Deletes a Placement Group.

        :param placement_group: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>` or :class:`PlacementGroup <hcloud.placement_groups.domain.PlacementGroup>`
        :return: boolean
        """
        self._client.request(
            url="/placement_groups/{placement_group_id}".format(
                placement_group_id=placement_group.id
            ),
            method="DELETE",
        )
        return True
