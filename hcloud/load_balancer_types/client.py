from hcloud.core.client import ClientEntityBase, BoundModelBase, GetEntityByNameMixin
from hcloud.load_balancer_types.domain import LoadBalancerType


class BoundLoadBalancerType(BoundModelBase):
    model = LoadBalancerType


class LoadBalancerTypesClient(ClientEntityBase, GetEntityByNameMixin):
    results_list_attribute_name = "load_balancer_types"

    def get_by_id(self, id):
        # type: (int) -> load_balancer_types.client.BoundLoadBalancerType
        """Returns a specific Load Balancer Type.

        :param id: int
        :return: :class:`BoundLoadBalancerType <hcloud.load_balancer_type.client.BoundLoadBalancerType>`
        """
        response = self._client.request(
            url="/load_balancer_types/{load_balancer_type_id}".format(
                load_balancer_type_id=id
            ),
            method="GET",
        )
        return BoundLoadBalancerType(self, response["load_balancer_type"])

    def get_list(self, name=None, page=None, per_page=None):
        # type: (Optional[str], Optional[int], Optional[int]) -> PageResults[List[BoundLoadBalancerType], Meta]
        """Get a list of Load Balancer types

        :param name: str (optional)
               Can be used to filter Load Balancer type by their name.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundLoadBalancerType <hcloud.load_balancer_types.client.BoundLoadBalancerType>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params = {}
        if name is not None:
            params["name"] = name
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(
            url="/load_balancer_types", method="GET", params=params
        )
        load_balancer_types = [
            BoundLoadBalancerType(self, load_balancer_type_data)
            for load_balancer_type_data in response["load_balancer_types"]
        ]
        return self._add_meta_to_result(load_balancer_types, response)

    def get_all(self, name=None):
        # type: (Optional[str]) -> List[BoundLoadBalancerType]
        """Get all Load Balancer types

        :param name: str (optional)
               Can be used to filter Load Balancer type by their name.
        :return: List[:class:`BoundLoadBalancerType <hcloud.load_balancer_types.client.BoundLoadBalancerType>`]
        """
        return super(LoadBalancerTypesClient, self).get_all(name=name)

    def get_by_name(self, name):
        # type: (str) -> BoundLoadBalancerType
        """Get Load Balancer type by name

        :param name: str
               Used to get Load Balancer type by name.
        :return: :class:`BoundLoadBalancerType <hcloud.load_balancer_types.client.BoundLoadBalancerType>`
        """
        return super(LoadBalancerTypesClient, self).get_by_name(name)
