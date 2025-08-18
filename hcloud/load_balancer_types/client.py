from __future__ import annotations

from typing import Any, NamedTuple

from ..core import BoundModelBase, Meta, ResourceClientBase
from .domain import LoadBalancerType


class BoundLoadBalancerType(BoundModelBase, LoadBalancerType):
    _client: LoadBalancerTypesClient

    model = LoadBalancerType


class LoadBalancerTypesPageResult(NamedTuple):
    load_balancer_types: list[BoundLoadBalancerType]
    meta: Meta


class LoadBalancerTypesClient(ResourceClientBase):
    _base_url = "/load_balancer_types"

    def get_by_id(self, id: int) -> BoundLoadBalancerType:
        """Returns a specific Load Balancer Type.

        :param id: int
        :return: :class:`BoundLoadBalancerType <hcloud.load_balancer_type.client.BoundLoadBalancerType>`
        """
        response = self._client.request(
            url=f"{self._base_url}/{id}",
            method="GET",
        )
        return BoundLoadBalancerType(self, response["load_balancer_type"])

    def get_list(
        self,
        name: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> LoadBalancerTypesPageResult:
        """Get a list of Load Balancer types

        :param name: str (optional)
               Can be used to filter Load Balancer type by their name.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundLoadBalancerType <hcloud.load_balancer_types.client.BoundLoadBalancerType>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url=self._base_url, method="GET", params=params)
        load_balancer_types = [
            BoundLoadBalancerType(self, load_balancer_type_data)
            for load_balancer_type_data in response["load_balancer_types"]
        ]
        return LoadBalancerTypesPageResult(
            load_balancer_types, Meta.parse_meta(response)
        )

    def get_all(self, name: str | None = None) -> list[BoundLoadBalancerType]:
        """Get all Load Balancer types

        :param name: str (optional)
               Can be used to filter Load Balancer type by their name.
        :return: List[:class:`BoundLoadBalancerType <hcloud.load_balancer_types.client.BoundLoadBalancerType>`]
        """
        return self._iter_pages(self.get_list, name=name)

    def get_by_name(self, name: str) -> BoundLoadBalancerType | None:
        """Get Load Balancer type by name

        :param name: str
               Used to get Load Balancer type by name.
        :return: :class:`BoundLoadBalancerType <hcloud.load_balancer_types.client.BoundLoadBalancerType>`
        """
        return self._get_first_by(name=name)
