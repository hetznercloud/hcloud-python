from __future__ import annotations

import time
import warnings
from typing import TYPE_CHECKING, Any, NamedTuple

from ..core import BoundModelBase, ClientEntityBase, Meta
from .domain import Action, ActionFailedException, ActionTimeoutException

if TYPE_CHECKING:
    from .._client import Client


class BoundAction(BoundModelBase, Action):
    _client: ActionsClient

    model = Action

    def wait_until_finished(self, max_retries: int = 100) -> None:
        """Wait until the specific action has status="finished" (set Client.poll_interval to specify a delay between checks)

        :param max_retries: int
               Specify how many retries will be performed before an ActionTimeoutException will be raised
        :raises: ActionFailedException when action is finished with status=="error"
        :raises: ActionTimeoutException when Action is still in "running" state after max_retries reloads.
        """
        while self.status == Action.STATUS_RUNNING:
            if max_retries > 0:
                self.reload()
                # pylint: disable=protected-access
                time.sleep(self._client._client.poll_interval)
                max_retries = max_retries - 1
            else:
                raise ActionTimeoutException(action=self)

        if self.status == Action.STATUS_ERROR:
            raise ActionFailedException(action=self)


class ActionsPageResult(NamedTuple):
    actions: list[BoundAction]
    meta: Meta | None


class ResourceActionsClient(ClientEntityBase):
    _resource: str

    def __init__(self, client: Client, resource: str | None):
        super().__init__(client)
        self._resource = resource or ""

    def get_by_id(self, id: int) -> BoundAction:
        """Get a specific action by its ID.

        :param id: int
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"{self._resource}/actions/{id}",
            method="GET",
        )
        return BoundAction(self._client.actions, response["action"])

    def get_list(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """Get a list of actions.

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
        params: dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(
            url=f"{self._resource}/actions",
            method="GET",
            params=params,
        )
        actions = [
            BoundAction(self._client.actions, action_data)
            for action_data in response["actions"]
        ]
        return ActionsPageResult(actions, Meta.parse_meta(response))

    def get_all(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """Get all actions.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `command` `status` `progress`  `started` `finished` . You can add one of ":asc", ":desc" to modify sort order. ( ":asc" is default)
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._iter_pages(self.get_list, status=status, sort=sort)


class ActionsClient(ResourceActionsClient):
    def __init__(self, client: Client):
        super().__init__(client, None)

    def get_list(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """
        .. deprecated:: 1.28
            Use :func:`client.<resource>.actions.get_list` instead,
            e.g. using :attr:`hcloud.certificates.client.CertificatesClient.actions`.

            `Starting 1 October 2023, it will no longer be available. <https://docs.hetzner.cloud/changelog#2023-07-20-actions-list-endpoint-is-deprecated>`_
        """
        warnings.warn(
            "The 'client.actions.get_list' method is deprecated, please use the "
            "'client.<resource>.actions.get_list' method instead (e.g. "
            "'client.certificates.actions.get_list').",
            DeprecationWarning,
            stacklevel=2,
        )
        return super().get_list(status=status, sort=sort, page=page, per_page=per_page)

    def get_all(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """
        .. deprecated:: 1.28
            Use :func:`client.<resource>.actions.get_all` instead,
            e.g. using :attr:`hcloud.certificates.client.CertificatesClient.actions`.

            `Starting 1 October 2023, it will no longer be available. <https://docs.hetzner.cloud/changelog#2023-07-20-actions-list-endpoint-is-deprecated>`_
        """
        warnings.warn(
            "The 'client.actions.get_all' method is deprecated, please use the "
            "'client.<resource>.actions.get_all' method instead (e.g. "
            "'client.certificates.actions.get_all').",
            DeprecationWarning,
            stacklevel=2,
        )
        return super().get_all(status=status, sort=sort)
