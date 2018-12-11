# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase

from hcloud.datacenters.domain import Datacenter, DatacenterServerTypes
from hcloud.locations.client import BoundLocation
from hcloud.server_types.client import BoundServerType


class BoundDatacenter(BoundModelBase):
    model = Datacenter

    def __init__(self, client, data):
        location = data.get("location")
        if location is not None:
            data['location'] = BoundLocation(client._client.locations, location)

        server_types = data.get("server_types")
        if server_types is not None:
            DatacenterServerTypes
            available = [BoundServerType(client._client.server_types, {"id": server_type}, complete=False) for server_type in server_types['available']]
            supported = [BoundServerType(client._client.server_types, {"id": server_type}, complete=False) for server_type in server_types['supported']]
            available_for_migration = [BoundServerType(client._client.server_types, {"id": server_type}, complete=False) for server_type in server_types['available_for_migration']]
            data['server_types'] = DatacenterServerTypes(available=available, supported=supported, available_for_migration=available_for_migration)

        super(BoundDatacenter, self).__init__(client, data)


class DatacentersClient(ClientEntityBase):

    def get_by_id(self, id):
        # type: (int) -> datacenters.client.BoundDatacenter
        response = self._client.request(url="/datacenters/{datacenter_id}".format(datacenter_id=id), method="GET")
        return BoundDatacenter(self, response['datacenter'])

    def get_all(self, name=None):
        # type: (Optional[str]) -> List[BoundAction]
        params = {}
        if name is not None:
            params.update({"name": name})

        response = self._client.request(url="/datacenters", method="GET", params=params)
        return [BoundDatacenter(self, datacenter_data) for datacenter_data in response['datacenters']]
