from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any, Callable, NamedTuple

from .._utils import batched, waiter
from ..core import BoundModelBase, ClientEntityBase, Meta
from .domain import (
    Action,
    ActionFailedException,
    ActionGroupException,
    ActionTimeoutException,
)

if TYPE_CHECKING:
    from .._client import Client


class BoundAction(BoundModelBase, Action):
    _client: ActionsClient

    model = Action

    def wait_until_finished(
        self,
        max_retries: int | None = None,
        *,
        timeout: float | None = None,
    ) -> None:
        """Wait until the specific action has status=finished.

        :param max_retries: int Specify how many retries will be performed before an ActionTimeoutException will be raised.
        :param timeout: Timeout in seconds before an ActionTimeoutException will be raised.
        :raises: ActionFailedException when action is finished with status==error
        :raises: ActionTimeoutException when Action is still in status==running after max_retries or timeout is reached.
        """
        if max_retries is None:
            # pylint: disable=protected-access
            max_retries = self._client._client._poll_max_retries

        retries = 0
        wait = waiter(timeout)
        while True:
            self.reload()
            if self.status != Action.STATUS_RUNNING:
                break

            retries += 1
            if retries < max_retries:
                # pylint: disable=protected-access
                if not wait(self._client._client._poll_interval_func(retries)):
                    continue

            raise ActionTimeoutException(action=self)

        if self.status == Action.STATUS_ERROR:
            raise ActionFailedException(action=self)


class ActionsPageResult(NamedTuple):
    actions: list[BoundAction]
    meta: Meta


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

    def _get_list_by_ids(self, ids: list[int]) -> list[BoundAction]:
        """
        Get a list of Actions by their IDs.

        :param ids: List of Action IDs to get.
        :raises ValueError: Raise when Action IDs were not found.
        :return: List of Actions.
        """
        actions: list[BoundAction] = []

        for ids_batch in batched(ids, 25):
            params: dict[str, Any] = {
                "id": ids_batch,
            }

            response = self._client.request(
                method="GET",
                url="/actions",
                params=params,
            )

            actions.extend(
                BoundAction(self._client.actions, action_data)
                for action_data in response["actions"]
            )

        if len(ids) != len(actions):
            found_ids = [a.id for a in actions]
            not_found_ids = list(set(ids) - set(found_ids))

            raise ValueError(
                f"actions not found: {', '.join(str(o) for o in not_found_ids)}"
            )

        return actions

    def wait_for_function(
        self,
        handle_update: Callable[[BoundAction], None],
        actions: list[Action | BoundAction],
        *,
        timeout: float | None = None,
    ) -> list[BoundAction]:
        """
        Waits until all Actions succeed by polling the API at the interval defined by
        the client's poll interval and function. An Action is considered as complete
        when its status is either "success" or "error".

        The handle_update callback is called every time an Action is updated.

        :param handle_update: Function called every time an Action is updated.
        :param actions: List of Actions to wait for.
        :param timeout: Timeout in seconds.
        :raises: ActionFailedException when an Action failed.
        :return: List of succeeded Actions.
        """
        running: list[BoundAction] = list(actions)
        completed: list[BoundAction] = []

        retries = 0
        wait = waiter(timeout)
        while len(running) > 0:
            # pylint: disable=protected-access
            if wait(self._client._poll_interval_func(retries)):
                raise ActionGroupException(
                    failed=[ActionTimeoutException(action) for action in running],
                    completed=completed,
                )

            retries += 1

            running = self._get_list_by_ids([a.id for a in running])

            for update in running:
                if update.status != Action.STATUS_RUNNING:
                    running.remove(update)
                    completed.append(update)

                handle_update(update)

        return completed

    def wait_for(
        self,
        actions: list[Action | BoundAction],
        *,
        timeout: float | None = None,
    ) -> list[BoundAction]:
        """
        Waits until all Actions succeed by polling the API at the interval defined by
        the client's poll interval and function. An Action is considered as complete
        when its status is either "success" or "error".

        If a single Action fails, the function will stop waiting and raise ActionFailedException.

        :param actions: List of Actions to wait for.
        :param timeout: Timeout in seconds.
        :raises: ActionFailedException when an Action failed.
        :raises: TimeoutError when the Actions did not succeed before timeout.
        :return: List of succeeded Actions.
        """

        def handle_update(update: BoundAction) -> None:
            if update.status == Action.STATUS_ERROR:
                raise ActionFailedException(action=update)

        return self.wait_for_function(handle_update, actions, timeout=timeout)

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
