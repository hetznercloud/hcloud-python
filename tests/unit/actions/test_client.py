from __future__ import annotations

import inspect
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
from hcloud.certificates import CertificatesClient
from hcloud.core import ResourceClientBase
from hcloud.firewalls import FirewallsClient
from hcloud.floating_ips import FloatingIPsClient
from hcloud.images import ImagesClient
from hcloud.load_balancers import LoadBalancersClient
from hcloud.networks import NetworksClient
from hcloud.primary_ips import PrimaryIPsClient
from hcloud.servers import ServersClient
from hcloud.volumes import VolumesClient

from ..conftest import assert_bound_action1, assert_bound_action2

resource_clients_with_actions = {
    "certificates": CertificatesClient,
    "firewalls": FirewallsClient,
    "floating_ips": FloatingIPsClient,
    "images": ImagesClient,
    "load_balancers": LoadBalancersClient,
    "networks": NetworksClient,
    "primary_ips": PrimaryIPsClient,
    "servers": ServersClient,
    "volumes": VolumesClient,
}


def test_resource_clients_with_actions(client: Client):
    """
    Ensure that the list of resource clients above is up to date.
    """
    members = inspect.getmembers(
        client,
        predicate=lambda p: isinstance(p, ResourceClientBase) and hasattr(p, "actions"),
    )
    for name, member in members:
        assert name in resource_clients_with_actions
        assert member.__class__ is resource_clients_with_actions[name]

    assert len(members) == len(resource_clients_with_actions)


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
    """
    /<resource>/actions
    /<resource>/actions/<id>
    """

    @pytest.fixture(params=resource_clients_with_actions.keys())
    def resource(self, request) -> str:
        return request.param

    @pytest.fixture()
    def resource_client(self, client: Client, resource: str) -> ResourceActionsClient:
        """
        Extract the resource actions client from the client.
        """
        return getattr(client, resource).actions

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        resource_client: ResourceActionsClient,
        resource: str,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url=f"/{resource}/actions/1",
        )

        assert_bound_action1(action, resource_client._parent.actions)

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
        resource_client: ResourceActionsClient,
        resource: str,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        result = resource_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url=f"/{resource}/actions",
            params=params,
        )

        assert result.meta is not None

        actions = result.actions
        assert len(actions) == 2
        assert_bound_action1(actions[0], resource_client._parent.actions)
        assert_bound_action2(actions[1], resource_client._parent.actions)

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
        resource_client: ResourceActionsClient,
        resource: str,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        actions = resource_client.get_all(**params)

        request_mock.assert_called_with(
            method="GET",
            url=f"/{resource}/actions",
            params={**params, "page": 1, "per_page": 50},
        )

        assert len(actions) == 2
        assert_bound_action1(actions[0], resource_client._parent.actions)
        assert_bound_action2(actions[1], resource_client._parent.actions)


class TestResourceObjectActionsClient:
    """
    /<resource>/<id>/actions
    """

    @pytest.fixture(params=resource_clients_with_actions.keys())
    def resource(self, request):
        if request.param == "primary_ips":
            pytest.skip("not implemented yet")
        return request.param

    @pytest.fixture()
    def resource_client(self, client: Client, resource: str) -> ResourceClientBase:
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
        resource_client: ResourceClientBase,
        resource: str,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        result = resource_client.get_actions_list(mock.MagicMock(id=1), **params)

        request_mock.assert_called_with(
            method="GET",
            url=f"/{resource}/1/actions",
            params=params,
        )

        assert result.meta is not None

        actions = result.actions
        assert len(actions) == 2
        assert_bound_action1(actions[0], resource_client._parent.actions)
        assert_bound_action2(actions[1], resource_client._parent.actions)

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
        resource_client: ResourceClientBase,
        resource: str,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        actions = resource_client.get_actions(mock.MagicMock(id=1), **params)

        request_mock.assert_called_with(
            method="GET",
            url=f"/{resource}/1/actions",
            params={**params, "page": 1, "per_page": 50},
        )

        assert len(actions) == 2
        assert_bound_action1(actions[0], resource_client._parent.actions)
        assert_bound_action2(actions[1], resource_client._parent.actions)


class TestActionsClient:
    @pytest.fixture()
    def actions_client(self, client: Client) -> ActionsClient:
        return client.actions

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
        assert_bound_action1(action, actions_client)

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
        assert_bound_action1(actions[0], actions_client)
        assert_bound_action2(actions[1], actions_client)

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
        assert_bound_action1(actions[0], actions_client)
        assert_bound_action2(actions[1], actions_client)
