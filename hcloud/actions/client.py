from __future__ import annotations

import time
import warnings
from typing import TYPE_CHECKING, Any, Literal, NamedTuple

from ..core import BoundModelBase, Meta, ResourceClientBase
from .domain import Action, ActionFailedException, ActionStatus, ActionTimeoutException

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

    def wait_until_finished(self, max_retries: int | None = None) -> None:
        """Wait until the specific action has status=finished.

        :param max_retries: int Specify how many retries will be performed before an ActionTimeoutException will be raised.
        :raises: ActionFailedException when action is finished with status==error
        :raises: ActionTimeoutException when Action is still in status==running after max_retries is reached.
        """
        if max_retries is None:
            # pylint: disable=protected-access
            max_retries = self._client._client._poll_max_retries

        retries = 0
        while True:
            self.reload()
            if self.status != Action.STATUS_RUNNING:
                break

            retries += 1
            if retries < max_retries:
                # pylint: disable=protected-access
                time.sleep(self._client._client._poll_interval_func(retries))
                continue

            raise ActionTimeoutException(action=self)

        if self.status == Action.STATUS_ERROR:
            raise ActionFailedException(action=self)


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
