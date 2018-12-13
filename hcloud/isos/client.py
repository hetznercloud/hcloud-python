# -*- coding: utf-8 -*-
from hcloud.core.client import BoundModelBase, ClientEntityBase

from hcloud.isos.domain import Iso


class BoundIso(BoundModelBase):
    model = Iso


class IsosClient(ClientEntityBase):
    results_list_attribute_name = 'isos'

    def get_by_id(self, id):
        # type: (int) -> BoundIso
        response = self._client.request(url="/isos/{iso_id}".format(iso_id=id), method="GET")
        return BoundIso(self, response['iso'])

    def get_list(self,
                 name=None,      # type: Optional[str]
                 page=None,      # type: Optional[int]
                 per_page=None,  # type: Optional[int]
                 ):
        # type: (...) -> PageResults[List[BoundIso], Meta]
        params = {}
        if name:
            params['name'] = name
        if page is not None:
            params['page'] = page
        if per_page is not None:
            params['per_page'] = per_page

        response = self._client.request(url="/isos", method="GET", params=params)
        isos = [BoundIso(self, iso_data) for iso_data in response['isos']]
        return self.add_meta_to_result(isos, response)

    def get_all(self, name=None):
        # type: (Optional[str]) -> List[BoundIso]
        return super(IsosClient, self).get_all(name=name)
