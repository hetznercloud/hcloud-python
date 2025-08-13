from __future__ import annotations

from unittest import mock

import pytest

from hcloud import Client
from hcloud.actions import (
    ActionFailedException,
    ActionTimeoutException,
    BoundAction,
    ResourceActionsClient,
)
from hcloud.core import ClientEntityBase

from ..conftest import assert_action1, assert_action2


class TestBoundAction:
    @pytest.fixture()
    def bound_action(self, client: Client, action1_running):
        # Speed up tests that run `wait_until_finished`
        client._poll_interval_func = lambda _: 0.0
        client._poll_max_retries = 3

        return BoundAction(
            client=client.actions,
            data=action1_running,
        )

    def test_wait_until_finished(
        self,
        request_mock: mock.MagicMock,
        bound_action: BoundAction,
        action1_running,
        action1_success,
    ):
        request_mock.side_effect = [
            {"action": action1_running},
            {"action": action1_success},
        ]
        bound_action.wait_until_finished()
        request_mock.assert_called_with(url="/actions/1", method="GET")

        assert bound_action.status == "success"
        assert request_mock.call_count == 2

    def test_wait_until_finished_error(
        self,
        request_mock: mock.MagicMock,
        bound_action: BoundAction,
        action1_running,
        action1_error,
    ):
        request_mock.side_effect = [
            {"action": action1_running},
            {"action": action1_error},
        ]
        with pytest.raises(ActionFailedException) as exception_info:
            bound_action.wait_until_finished()

        assert bound_action.status == "error"
        assert exception_info.value.action.id == 1
        assert request_mock.call_count == 2

    def test_wait_until_finished_max_retries(
        self,
        request_mock: mock.MagicMock,
        bound_action: BoundAction,
        action1_running,
    ):
        request_mock.side_effect = [
            {"action": action1_running},
            {"action": action1_running},
        ]
        with pytest.raises(ActionTimeoutException) as exception_info:
            bound_action.wait_until_finished(max_retries=1)

        assert bound_action.status == "running"
        assert exception_info.value.action.id == 1
        assert request_mock.call_count == 1


def resources_with_actions_client():
    """
    Allows us to run TestResourceActionsClient against all resource clients that have an
    resource actions client.
    """
    result = []
    client = Client("TOKEN")
    for var in vars(client):
        prop = getattr(client, var)
        # Save the property name when it is a resource client, and the resource client
        # has a resource actions client.
        if isinstance(prop, ClientEntityBase) and hasattr(prop, "actions"):
            result.append(var)

    return result


class TestResourceActionsClient:
    @pytest.fixture(params=resources_with_actions_client())
    def resource(self, request):
        return request.param

    @pytest.fixture()
    def actions_client(self, client: Client, resource: str):
        resource_client = getattr(client, resource)
        assert isinstance(resource_client.actions, ResourceActionsClient)
        return resource_client.actions

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        actions_client: ResourceActionsClient,
        resource: str,
        action_response,
    ):
        request_mock.return_value = action_response

        result = actions_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url=f"/{resource}/actions/1",
        )

        assert_action1(result, actions_client._client)

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"status": ["running"], "sort": ["status"], "page": 2, "per_page": 10},
        ],
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        actions_client: ResourceActionsClient,
        resource: str,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        result = actions_client.get_list(**params)

        request_mock.assert_called_with(
            url=f"/{resource}/actions",
            method="GET",
            params=params,
        )

        assert result.meta is not None

        assert len(result.actions) == 2
        assert_action1(result.actions[0], actions_client._client)
        assert_action2(result.actions[1], actions_client._client)

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"status": ["running"], "sort": ["status"]},
        ],
    )
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        actions_client: ResourceActionsClient,
        resource: str,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        result = actions_client.get_all(**params)

        request_mock.assert_called_with(
            url=f"/{resource}/actions",
            method="GET",
            params={**params, "page": 1, "per_page": 50},
        )

        assert len(result) == 2
        assert_action1(result[0], actions_client._client)
        assert_action2(result[1], actions_client._client)


class TestResourceClientActions:
    @pytest.fixture(params=resources_with_actions_client())
    def resource(self, request):
        if request.param == "primary_ips":
            pytest.skip("not implemented yet")
        return request.param

    @pytest.fixture()
    def resource_client(self, client: Client, resource: str):
        return getattr(client, resource)

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"status": ["running"], "sort": ["status"], "page": 2, "per_page": 10},
        ],
    )
    def test_get_actions_list(
        self,
        request_mock: mock.MagicMock,
        resource_client,
        resource: str,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        result = resource_client.get_actions_list(mock.MagicMock(id=1), **params)

        request_mock.assert_called_with(
            url=f"/{resource}/1/actions",
            method="GET",
            params=params,
        )

        assert result.meta is not None

        assert len(result.actions) == 2
        assert_action1(result.actions[0], resource_client._client)
        assert_action2(result.actions[1], resource_client._client)

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"status": ["running"], "sort": ["status"]},
        ],
    )
    def test_get_actions(
        self,
        request_mock: mock.MagicMock,
        resource_client,
        resource: str,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        result = resource_client.get_actions(mock.MagicMock(id=1), **params)

        request_mock.assert_called_with(
            url=f"/{resource}/1/actions",
            method="GET",
            params={**params, "page": 1, "per_page": 50},
        )

        assert len(result) == 2
        assert_action1(result[0], resource_client._client)
        assert_action2(result[1], resource_client._client)


class TestActionsClient:
    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        client: Client,
        action_response,
    ):
        request_mock.return_value = action_response

        result = client.actions.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/actions/1",
        )
        assert_action1(result, client)

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"status": ["running"], "sort": ["status"], "page": 2, "per_page": 10},
        ],
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        client: Client,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        with pytest.deprecated_call():
            result = client.actions.get_list(**params)

        request_mock.assert_called_with(
            url="/actions",
            method="GET",
            params=params,
        )

        assert result.meta is not None

        assert len(result.actions) == 2
        assert_action1(result.actions[0], client)
        assert_action2(result.actions[1], client)

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"status": ["running"], "sort": ["status"]},
        ],
    )
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        client: Client,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        with pytest.deprecated_call():
            result = client.actions.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            url="/actions",
            method="GET",
            params=params,
        )

        assert len(result) == 2
        assert_action1(result[0], client)
        assert_action2(result[1], client)
