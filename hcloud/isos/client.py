# -*- coding: utf-8 -*-
from hcloud.core.client import BoundModelBase, ClientEntityBase

from hcloud.isos.domain import Iso


class BoundIso(BoundModelBase):
    model = Iso


class IsosClient(ClientEntityBase):

    def get_by_id(self, id):
        # type: (int) -> BoundIso
        response = self._client.request(url="/isos/{iso_id}".format(iso_id=id), method="GET")
        return BoundIso(self, response['iso'])

    def get_all(self, name=None):
        # type: (Optional[str]) -> List[BoundIso]
        params = {}
        if name:
            params['name'] = name

        response = self._client.request(url="/isos", method="GET", params=params)
        return [BoundIso(self, iso_data) for iso_data in response['isos']]
