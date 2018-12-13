# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase

from hcloud.actions.domain import Action


class BoundAction(BoundModelBase):
    model = Action


class ActionsClient(ClientEntityBase):
    results_list_attribute_name = 'actions'

    def get_by_id(self, id):
        # type: (int) -> BoundAction
        response = self._client.request(url="/actions/{action_id}".format(action_id=id), method="GET")
        return BoundAction(self, response['action'])

    def get_list(self,
                 status=None,    # type: Optional[List[str]]
                 sort=None,      # type: Optional[List[str]]
                 page=None,      # type: Optional[int]
                 per_page=None,  # type: Optional[int]
                 ):
        # type: (...) -> PageResults[List[BoundAction]]
        params = {}
        if status is not None:
            params["status"] = status
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url="/actions", method="GET", params=params)
        actions = [BoundAction(self, action_data) for action_data in response['actions']]
        return self.add_meta_to_result(actions, response)

    def get_all(self, status=None, sort=None):
        # type: (Optional[List[str]], Optional[List[str]]) -> List[BoundAction]
        return super(ActionsClient, self).get_all(status=status, sort=sort)
