from warnings import warn

from ..core.client import BoundModelBase, ClientEntityBase, GetEntityByNameMixin
from .domain import Iso


class BoundIso(BoundModelBase):
    model = Iso


class IsosClient(ClientEntityBase, GetEntityByNameMixin):
    results_list_attribute_name = "isos"

    def get_by_id(self, id):
        # type: (int) -> BoundIso
        """Get a specific ISO by its id

        :param id: int
        :return: :class:`BoundIso <hcloud.isos.client.BoundIso>`
        """
        response = self._client.request(url=f"/isos/{id}", method="GET")
        return BoundIso(self, response["iso"])

    def get_list(
        self,
        name=None,  # type: Optional[str]
        architecture=None,  # type: Optional[List[str]]
        include_wildcard_architecture=None,  # type: Optional[bool]
        include_architecture_wildcard=None,  # type: Optional[bool]
        page=None,  # type: Optional[int]
        per_page=None,  # type: Optional[int]
    ):
        # type: (...) -> PageResults[List[BoundIso], Meta]
        """Get a list of ISOs

        :param name: str (optional)
               Can be used to filter ISOs by their name.
        :param architecture: List[str] (optional)
               Can be used to filter ISOs by their architecture. Choices: x86 arm
        :param include_wildcard_architecture: bool (optional)
               Deprecated, please use `include_architecture_wildcard` instead.
        :param include_architecture_wildcard: bool (optional)
               Custom ISOs do not have an architecture set. You must also set this flag to True if you are filtering by
               architecture and also want custom ISOs.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundIso <hcloud.isos.client.BoundIso>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """

        if include_wildcard_architecture is not None:
            warn(
                "The `include_wildcard_architecture` argument is deprecated, please use the `include_architecture_wildcard` argument instead.",
                DeprecationWarning,
            )
            include_architecture_wildcard = include_wildcard_architecture

        params = {}
        if name is not None:
            params["name"] = name
        if architecture is not None:
            params["architecture"] = architecture
        if include_architecture_wildcard is not None:
            params["include_architecture_wildcard"] = include_architecture_wildcard
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url="/isos", method="GET", params=params)
        isos = [BoundIso(self, iso_data) for iso_data in response["isos"]]
        return self._add_meta_to_result(isos, response)

    def get_all(
        self,
        name=None,  # type: Optional[str]
        architecture=None,  # type: Optional[List[str]]
        include_wildcard_architecture=None,  # type: Optional[bool]
        include_architecture_wildcard=None,  # type: Optional[bool]
    ):
        # type: (...) -> List[BoundIso]
        """Get all ISOs

        :param name: str (optional)
               Can be used to filter ISOs by their name.
        :param architecture: List[str] (optional)
               Can be used to filter ISOs by their architecture. Choices: x86 arm
        :param include_wildcard_architecture: bool (optional)
               Deprecated, please use `include_architecture_wildcard` instead.
        :param include_architecture_wildcard: bool (optional)
               Custom ISOs do not have an architecture set. You must also set this flag to True if you are filtering by
               architecture and also want custom ISOs.
        :return: List[:class:`BoundIso <hcloud.isos.client.BoundIso>`]
        """

        if include_wildcard_architecture is not None:
            warn(
                "The `include_wildcard_architecture` argument is deprecated, please use the `include_architecture_wildcard` argument instead.",
                DeprecationWarning,
            )
            include_architecture_wildcard = include_wildcard_architecture

        return super().get_all(
            name=name,
            architecture=architecture,
            include_architecture_wildcard=include_architecture_wildcard,
        )

    def get_by_name(self, name):
        # type: (str) -> BoundIso
        """Get iso by name

        :param name: str
               Used to get iso by name.
        :return: :class:`BoundIso <hcloud.isos.client.BoundIso>`
        """
        return super().get_by_name(name)
