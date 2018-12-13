# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase

from hcloud.locations.domain import Location


class BoundLocation(BoundModelBase):
    model = Location


class LocationsClient(ClientEntityBase):
    results_list_attribute_name = 'locations'

    def get_by_id(self, id):
        # type: (int) -> locations.client.BoundLocation
        response = self._client.request(url="/locations/{location_id}".format(location_id=id), method="GET")
        return BoundLocation(self, response['location'])

    def get_list(self, name=None, page=None, per_page=None):
        # type: (Optional[str], Optional[int], Optional[int]) -> PageResult[List[BoundLocation], Meta]
        params = {}
        if name is not None:
            params["name"] = name
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url="/locations", method="GET", params=params)
        locations = [BoundLocation(self, location_data) for location_data in response['locations']]
        return self.add_meta_to_result(locations, response)

    def get_all(self, name=None):
        # type: (Optional[str]) -> List[BoundLocation]
        return super(LocationsClient, self).get_all(name=name)
