from hcloud.core.client import ClientEntityBase, BoundModelBase
from hcloud.server_types.domain import ServerType


class BoundServerType(BoundModelBase):
    model = ServerType


class ServerTypesClient(ClientEntityBase):

    def get_by_id(self, id):
        # type: (int) -> server_types.client.BoundServerType
        response = self._client.request(url="/server_types/{server_type_id}".format(server_type_id=id), method="GET")
        return BoundServerType(self, response['server_type'])

    def get_all(self, name=None):
        # type: (Optional[str]) -> List[server_types.client.BoundServerType]
        params = {}
        if name:
            params['name'] = name

        response = self._client.request(url="/server_types", method="GET", params=params)
        return [BoundServerType(self, server_type_data) for server_type_data in response['server_types']]
