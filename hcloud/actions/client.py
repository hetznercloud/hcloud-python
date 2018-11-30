# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase

from hcloud.actions.domain import Action


class BoundAction(BoundModelBase):
    model = Action


class ActionsClient(ClientEntityBase):

    def get_by_id(self, id):
        # type: (int) -> actions.client.BoundAction
        response = self._client.request(url="/actions/{action_id}".format(action_id=id), method="GET")
        return BoundAction(self, response['action'])

    def get_all(self, status=None, sort=None):
        # type: # type: (Optional[List[str], Optional[List[str]]) -> List[BoundAction]
        params = {}
        if status is not None:
            params.update({"status": status})
        if sort is not None:
            params.update({"sort": sort})

        response = self._client.request(url="/actions", method="GET", params=params)
        return [BoundAction(self, action_data) for action_data in response['actions']]
