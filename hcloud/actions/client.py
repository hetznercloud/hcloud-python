# -*- coding: utf-8 -*-
import time

from hcloud.core.client import ClientEntityBase, BoundModelBase
from hcloud.actions.domain import Action, ActionFailedException, ActionTimeoutException


class BoundAction(BoundModelBase):
    model = Action

    def wait_until_finished(self, max_retries=100):
        """Wait until the specific action has status="finished" (set Client.poll_interval to specify a delay between checks)

        :param max_retries: int
               Specify how many retries will be performed before an ActionTimeoutException will be raised
        :raises: ActionFailedException when action is finished with status=="error"
        :raises: ActionTimeoutException when Action is still in "running" state after max_retries reloads.
        """
        while self.status == Action.STATUS_RUNNING:
            if max_retries > 0:
                self.reload()
                time.sleep(self._client._client.poll_interval)
                max_retries = max_retries - 1
            else:
                raise ActionTimeoutException(action=self)

        if self.status == Action.STATUS_ERROR:
            raise ActionFailedException(action=self)


class ActionsClient(ClientEntityBase):
    results_list_attribute_name = "actions"

    def get_by_id(self, id):
        # type: (int) -> BoundAction
        """Get a specific action by its ID.

        :param id: int
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """

        response = self._client.request(
            url="/actions/{action_id}".format(action_id=id), method="GET"
        )
        return BoundAction(self, response["action"])

    def get_list(
        self,
        status=None,  # type: Optional[List[str]]
        sort=None,  # type: Optional[List[str]]
        page=None,  # type: Optional[int]
        per_page=None,  # type: Optional[int]
    ):
        # type: (...) -> PageResults[List[BoundAction]]
        """Get a list of actions from this account

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `command` `status` `progress`  `started` `finished` . You can add one of ":asc", ":desc" to modify sort order. ( ":asc" is default)
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundAction <hcloud.actions.client.BoundAction>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
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
        actions = [
            BoundAction(self, action_data) for action_data in response["actions"]
        ]
        return self._add_meta_to_result(actions, response)

    def get_all(self, status=None, sort=None):
        # type: (Optional[List[str]], Optional[List[str]]) -> List[BoundAction]
        """Get all actions of the account

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `command` `status` `progress`  `started` `finished` . You can add one of ":asc", ":desc" to modify sort order. ( ":asc" is default)
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return super(ActionsClient, self).get_all(status=status, sort=sort)
