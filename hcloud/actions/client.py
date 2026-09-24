from __future__ import annotations

import warnings
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Literal, NamedTuple

from .._utils import batched, waiter
from ..core import BoundModelBase, Meta, ResourceClientBase
from .domain import (
    Action,
    ActionFailedException,
    ActionStatus,
    ActionTimeoutException,
)

if TYPE_CHECKING:
    from .._client import Client


__all__ = [
    "ActionsClient",
    "ActionsPageResult",
    "BoundAction",
    "ResourceActionsClient",
    "ActionSort",
]


class BoundAction(BoundModelBase[Action], Action):
    _client: ActionsClient

    model = Action

    def wait_until_finished(
        self,
        max_retries: int | None = None,
        *,
        timeout: float | None = None,
    ) -> None:
        """
        Waits until the Action is finished by polling the API at the interval defined by
        the client's poll interval and function. An Action is considered as finished
        when its status is either "success" or "error".

        If the Action fails (its status is "error"), the function will stop waiting
        and raise ActionFailedException.

        :param timeout:
            Duration in seconds before an ActionTimeoutException will be raised when polling actions from the API.
        :param max_retries:
            Max retries before an ActionTimeoutException will be raised when polling actions from the API.

        :raises: ActionTimeoutException when an Action is still running after max_retries or timeout is reached.
        :raises: ActionFailedException when an Action failed.
        """

        def handle_update(update: BoundAction) -> None:
            self.data_model = update.data_model

            if update.status == Action.STATUS_ERROR:
                raise ActionFailedException(action=update)

        try:
            self._client.wait_for_function(
                handle_update,
                [self],
                timeout=timeout,
                max_retries=max_retries,
            )
        except* ActionTimeoutException as group:
            raise group.exceptions[0]


ActionSort = Literal[
    "id",
    "id:asc",
    "id:desc",
    "command",
    "command:asc",
    "command:desc",
    "status",
    "status:asc",
    "status:desc",
    "started",
    "started:asc",
    "started:desc",
    "finished",
    "finished:asc",
    "finished:desc",
]


class ActionsPageResult(NamedTuple):
    actions: list[BoundAction]
    meta: Meta


class ResourceClientBaseActionsMixin(ResourceClientBase):
    def _get_action_by_id(
        self,
        base_url: str,
        id: int,
    ) -> BoundAction:
        response = self._client.request(
            method="GET",
            url=f"{base_url}/actions/{id}",
        )
        return BoundAction(
            client=self._parent.actions,
            data=response["action"],
        )

    def _get_actions_list(
        self,
        base_url: str,
        status: list[ActionStatus] | None = None,
        sort: list[ActionSort] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
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
            method="GET",
            url=f"{base_url}/actions",
            params=params,
        )
        return ActionsPageResult(
            actions=[BoundAction(self._parent.actions, o) for o in response["actions"]],
            meta=Meta.parse_meta(response),
        )


class ResourceActionsClient(
    ResourceClientBaseActionsMixin,
    ResourceClientBase,
):
    _resource: str

    def __init__(self, client: ResourceClientBase | Client, resource: str | None):
        if isinstance(client, ResourceClientBase):
            super().__init__(client._parent)
            # Use the same base client as the the resource base client. Allows us to
            # choose the base client outside of the ResourceActionsClient.
            self._client = client._client
        else:
            # Backward compatibility, defaults to the parent ("top level") base client (`_client`).
            super().__init__(client)

        self._resource = resource or ""

    def get_by_id(self, id: int) -> BoundAction:
        """
        Returns a specific Action by its ID.

        :param id: ID of the Action.
        """
        return self._get_action_by_id(self._resource, id)

    def get_list(
        self,
        status: list[ActionStatus] | None = None,
        sort: list[ActionSort] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """
        Returns a paginated list of Actions.

        :param status: Filter the Actions by status.
        :param sort: Sort Actions by field and direction.
        :param page: Page number to get.
        :param per_page: Maximum number of Actions returned per page.
        """
        return self._get_actions_list(
            self._resource,
            status=status,
            sort=sort,
            page=page,
            per_page=per_page,
        )

    def get_all(
        self,
        status: list[ActionStatus] | None = None,
        sort: list[ActionSort] | None = None,
    ) -> list[BoundAction]:
        """
        Returns all Actions.

        :param status: Filter the Actions by status.
        :param sort: Sort Actions by field and direction.
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
                "sort": ["status", "id"],
            }

            response = self._client.request(
                method="GET",
                url="/actions",
                params=params,
            )

            actions.extend(
                BoundAction(self._parent.actions, o) for o in response["actions"]
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
        max_retries: int | None = None,
    ) -> list[BoundAction]:
        """
        Waits until all Actions are finished by polling the API at the interval defined
        by the client's poll interval and function. An Action is considered as finished
        when its status is either "success" or "error".

        The handle_update callback is called every time an Action is updated.

        :param handle_update:
            Function called every time an Action is updated.
        :param actions:
            List of Actions to wait for.
        :param timeout:
            Duration in seconds before an ActionTimeoutException will be raised when polling actions from the API.
        :param max_retries:
            Max retries before an ActionTimeoutException will be raised when polling actions from the API.

        :raises: ActionTimeoutException when an Action is still running after max_retries or timeout is reached.

        :return: List of finished Actions.
        """
        if timeout is None:
            # pylint: disable=protected-access
            timeout = self._client._poll_timeout
        if max_retries is None:
            # pylint: disable=protected-access
            max_retries = self._client._poll_max_retries

        running: list[BoundAction] = actions.copy()  # type: ignore[assignment]
        completed: list[BoundAction] = []

        retries = 0
        wait = waiter(timeout)
        while len(running) > 0:
            if max_retries is not None and retries > max_retries:
                raise ExceptionGroup(
                    "The actions timed out after",
                    [ActionTimeoutException(action) for action in running],
                )

            # pylint: disable=protected-access
            if wait(self._client._poll_interval_func(retries)):
                raise ExceptionGroup(
                    "The actions timed out",
                    [ActionTimeoutException(action) for action in running],
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
        max_retries: int | None = None,
    ) -> list[BoundAction]:
        """
        Waits until all Actions are finished by polling the API at the interval defined
        by the client's poll interval and function. An Action is considered as finished
        when its status is either "success" or "error".

        If a single Action fails (its status is "error"), the function will stop waiting
        and raise ActionFailedException.

        :param actions:
            List of Actions to wait for.
        :param timeout:
            Duration in seconds before an ActionTimeoutException will be raised when polling actions from the API.
        :param max_retries:
            Max retries before an ActionTimeoutException will be raised when polling actions from the API.

        :raises: ActionTimeoutException when an Action is still running after max_retries or timeout is reached.
        :raises: ActionFailedException when an Action failed.

        :return: List of succeeded Actions.
        """

        def handle_update(update: BoundAction) -> None:
            if update.status == Action.STATUS_ERROR:
                raise ActionFailedException(action=update)

        return self.wait_for_function(
            handle_update,
            actions,
            timeout=timeout,
            max_retries=max_retries,
        )

    def get_list(
        self,
        status: list[ActionStatus] | None = None,
        sort: list[ActionSort] | None = None,
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
        status: list[ActionStatus] | None = None,
        sort: list[ActionSort] | None = None,
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
