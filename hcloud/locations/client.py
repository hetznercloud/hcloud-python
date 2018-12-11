# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase

from hcloud.locations.domain import Location


class BoundLocation(BoundModelBase):
    model = Location


class LocationsClient(ClientEntityBase):

    def get_by_id(self, id):
        # type: (int) -> locations.client.BoundLocation
        response = self._client.request(url="/locations/{location_id}".format(location_id=id), method="GET")
        return BoundLocation(self, response['location'])

    def get_all(self, name=None):
        # type: # type: (Optional[str]) -> List[BoundAction]
        params = {}
        if name is not None:
            params.update({"name": name})

        response = self._client.request(url="/locations", method="GET", params=params)
        return [BoundLocation(self, location_data) for location_data in response['locations']]
