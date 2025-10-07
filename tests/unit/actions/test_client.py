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
from hcloud.certificates import BoundCertificate, CertificatesClient
from hcloud.core import BoundModelBase, ResourceClientBase
from hcloud.firewalls import BoundFirewall, FirewallsClient
from hcloud.floating_ips import BoundFloatingIP, FloatingIPsClient
from hcloud.images import BoundImage, ImagesClient
from hcloud.load_balancers import BoundLoadBalancer, LoadBalancersClient
from hcloud.networks import BoundNetwork, NetworksClient
from hcloud.primary_ips import BoundPrimaryIP, PrimaryIPsClient
from hcloud.servers import BoundServer, ServersClient
from hcloud.volumes import BoundVolume, VolumesClient
from hcloud.zones import BoundZone, ZonesClient

from ..conftest import assert_bound_action1, assert_bound_action2

resources_with_actions: dict[str, tuple[ResourceClientBase, BoundModelBase]] = {
    "certificates": (CertificatesClient, BoundCertificate),
    "firewalls": (FirewallsClient, BoundFirewall),
    "floating_ips": (FloatingIPsClient, BoundFloatingIP),
    "images": (ImagesClient, BoundImage),
    "load_balancers": (LoadBalancersClient, BoundLoadBalancer),
    "networks": (NetworksClient, BoundNetwork),
    "primary_ips": (PrimaryIPsClient, BoundPrimaryIP),
    "servers": (ServersClient, BoundServer),
    "volumes": (VolumesClient, BoundVolume),
    "zones": (ZonesClient, BoundZone),
}


def test_resources_with_actions(client: Client):
    """
    Ensure that the list of resource clients above is up to date.
    """
    members = inspect.getmembers(
        client,
        predicate=lambda p: isinstance(p, ResourceClientBase) and hasattr(p, "actions"),
    )
    for name, member in members:
        assert name in resources_with_actions

        resource_client_class, _ = resources_with_actions[name]
        assert member.__class__ is resource_client_class

    assert len(members) == len(resources_with_actions)


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

    @pytest.fixture(params=resources_with_actions.keys())
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

    @pytest.fixture(params=resources_with_actions.keys())
    def resource(self, request):
        if request.param == "primary_ips":
            pytest.skip("not implemented yet")
        return request.param

    @pytest.fixture()
    def resource_client(self, client: Client, resource: str) -> ResourceClientBase:
        return getattr(client, resource)

    @pytest.fixture()
    def bound_model(self, client: Client, resource: str) -> BoundModelBase:
        _, bound_model_class = resources_with_actions[resource]
        resource_client = getattr(client, resource)
        return bound_model_class(resource_client, data={"id": 1})

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
        bound_model: BoundModelBase,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        result = resource_client.get_actions_list(bound_model, **params)

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
        bound_model: BoundModelBase,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        actions = resource_client.get_actions(bound_model, **params)

        request_mock.assert_called_with(
            method="GET",
            url=f"/{resource}/1/actions",
            params={**params, "page": 1, "per_page": 50},
        )

        assert len(actions) == 2
        assert_bound_action1(actions[0], resource_client._parent.actions)
        assert_bound_action2(actions[1], resource_client._parent.actions)


class TestBoundModelActions:
    """
    /<resource>/<id>/actions
    """

    @pytest.fixture(params=resources_with_actions.keys())
    def resource(self, request):
        if request.param == "primary_ips":
            pytest.skip("not implemented yet")
        return request.param

    @pytest.fixture()
    def bound_model(self, client: Client, resource: str) -> ResourceClientBase:
        _, bound_model_class = resources_with_actions[resource]
        resource_client = getattr(client, resource)
        return bound_model_class(resource_client, data={"id": 1})

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
        bound_model: BoundModelBase,
        resource: str,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        result = bound_model.get_actions_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url=f"/{resource}/1/actions",
            params=params,
        )

        assert result.meta is not None

        actions = result.actions
        assert len(actions) == 2
        assert_bound_action1(actions[0], bound_model._client._parent.actions)
        assert_bound_action2(actions[1], bound_model._client._parent.actions)

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
        bound_model: BoundModelBase,
        resource: str,
        action_list_response,
        params,
    ):
        request_mock.return_value = action_list_response

        actions = bound_model.get_actions(**params)

        request_mock.assert_called_with(
            method="GET",
            url=f"/{resource}/1/actions",
            params={**params, "page": 1, "per_page": 50},
        )

        assert len(actions) == 2
        assert_bound_action1(actions[0], bound_model._client._parent.actions)
        assert_bound_action2(actions[1], bound_model._client._parent.actions)


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
