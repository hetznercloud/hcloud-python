from __future__ import annotations

from unittest import mock

import pytest

from hcloud import Client
from hcloud.actions import (
    ActionFailedException,
    ActionsClient,
    ActionTimeoutException,
    BoundAction,
    ResourceActionsClient,
)

from ..conftest import assert_bound_action1, assert_bound_action2


class TestBoundAction:
    @pytest.fixture()
    def bound_running_action(self, client: Client, action1_running):
        return BoundAction(client=client.actions, data=action1_running)

    def test_wait_until_finished(
        self,
        request_mock: mock.MagicMock,
        bound_running_action,
        action1_running,
        action1_success,
    ):
        request_mock.side_effect = [
            {"action": action1_running},
            {"action": action1_success},
        ]

        bound_running_action.wait_until_finished()

        request_mock.assert_called_with(
            method="GET",
            url="/actions/1",
        )

        assert bound_running_action.status == "success"
        assert bound_running_action.id == 1

        assert request_mock.call_count == 2

    def test_wait_until_finished_with_error(
        self,
        request_mock: mock.MagicMock,
        bound_running_action,
        action1_running,
        action1_error,
    ):
        request_mock.side_effect = [
            {"action": action1_running},
            {"action": action1_error},
        ]

        with pytest.raises(ActionFailedException) as exc:
            bound_running_action.wait_until_finished()

        assert bound_running_action.status == "error"
        assert bound_running_action.id == 1
        assert exc.value.action.id == 1

        assert request_mock.call_count == 2

    def test_wait_until_finished_max_retries(
        self,
        request_mock: mock.MagicMock,
        bound_running_action,
        action1_running,
        action1_success,
    ):
        request_mock.side_effect = [
            {"action": action1_running},
            {"action": action1_running},
            {"action": action1_success},
        ]

        with pytest.raises(ActionTimeoutException) as exc:
            bound_running_action.wait_until_finished(max_retries=1)

        assert bound_running_action.status == "running"
        assert bound_running_action.id == 1
        assert exc.value.action.id == 1

        assert request_mock.call_count == 1


class TestResourceActionsClient:
    @pytest.fixture()
    def actions_client(self, client: Client):
        return ResourceActionsClient(client, resource="/resource")

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        actions_client: ActionsClient,
        action_response,
    ):
        request_mock.return_value = action_response

        action = actions_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/resource/actions/1",
        )

        assert_bound_action1(action, actions_client._parent.actions)

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"status": ["active"], "sort": ["status"], "page": 2, "per_page": 10},
        ],
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        actions_client: ActionsClient,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        result = actions_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/resource/actions",
            params=params,
        )

        assert result.meta is not None

        actions = result.actions
        assert len(actions) == 2
        assert_bound_action1(actions[0], actions_client._parent.actions)
        assert_bound_action2(actions[1], actions_client._parent.actions)

    @pytest.mark.parametrize("params", [{}, {"status": ["active"], "sort": ["status"]}])
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        actions_client: ActionsClient,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        actions = actions_client.get_all(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/resource/actions",
            params={**params, "page": 1, "per_page": 50},
        )

        assert len(actions) == 2
        assert_bound_action1(actions[0], actions_client._parent.actions)
        assert_bound_action2(actions[1], actions_client._parent.actions)


class TestActionsClient:
    @pytest.fixture()
    def actions_client(self, client: Client):
        return ActionsClient(client)

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        actions_client: ActionsClient,
        action_response,
    ):
        request_mock.return_value = action_response

        action = actions_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/actions/1",
        )
        assert_bound_action1(action, actions_client._parent.actions)

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"status": ["active"], "sort": ["status"], "page": 2, "per_page": 10},
        ],
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        actions_client: ActionsClient,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        with pytest.deprecated_call():
            result = actions_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/actions",
            params=params,
        )

        assert result.meta is not None

        actions = result.actions
        assert len(actions) == 2
        assert_bound_action1(actions[0], actions_client._parent.actions)
        assert_bound_action2(actions[1], actions_client._parent.actions)

    @pytest.mark.parametrize("params", [{}, {"status": ["active"], "sort": ["status"]}])
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        actions_client: ActionsClient,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        with pytest.deprecated_call():
            actions = actions_client.get_all(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/actions",
            params={**params, "page": 1, "per_page": 50},
        )

        assert len(actions) == 2
        assert_bound_action1(actions[0], actions_client._parent.actions)
        assert_bound_action2(actions[1], actions_client._parent.actions)
