# pylint: disable=redefined-outer-name

from __future__ import annotations

from collections.abc import Generator
from unittest import mock
from warnings import warn

import pytest

from hcloud import Client
from hcloud.actions import ActionsClient, BoundAction


@pytest.fixture(autouse=True, scope="session")
def patch_package_version():
    with mock.patch("hcloud._client.__version__", "0.0.0"):
        yield


@pytest.fixture()
def request_mock() -> mock.MagicMock:
    return mock.MagicMock()


@pytest.fixture()
def client(request_mock) -> Client:
    c = Client(
        token="TOKEN",
        # Speed up tests that use `_poll_interval_func`
        poll_interval=0.0,
        poll_max_retries=3,
    )
    c._client.request = request_mock
    return c


def assert_bound_action1(o: BoundAction, client: ActionsClient):
    assert o.id == 1
    assert o.command == "command"
    assert o._client == client


def assert_bound_action2(o: BoundAction, client: ActionsClient):
    assert o.id == 2
    assert o.command == "command"
    assert o._client == client


@pytest.fixture()
def action1_running():
    return {
        "id": 1,
        "command": "command",
        "status": "running",
        "progress": 0,
        "started": "2016-01-30T23:50+00:00",
        "finished": None,
        "resources": [{"id": 42, "type": "resource"}],
        "error": None,
    }


@pytest.fixture()
def action2_running():
    return {
        "id": 2,
        "command": "command",
        "status": "running",
        "progress": 20,
        "started": "2016-01-30T23:50+00:00",
        "finished": None,
        "resources": [{"id": 43, "type": "resource"}],
        "error": None,
    }


@pytest.fixture()
def action1_success(action1_running):
    return {
        **action1_running,
        "status": "success",
        "progress": 100,
        "finished": "2016-01-31T00:10+00:00",
    }


@pytest.fixture()
def action2_success(action2_running):
    return {
        **action2_running,
        "status": "success",
        "progress": 100,
        "finished": "2016-01-31T00:10+00:00",
    }


@pytest.fixture()
def action1_error(action1_running):
    return {
        **action1_running,
        "status": "error",
        "progress": 100,
        "finished": "2016-01-31T00:10+00:00",
        "error": {"code": "action_failed", "message": "Action failed"},
    }


@pytest.fixture()
def action2_error(action2_running):
    return {
        **action2_running,
        "status": "error",
        "progress": 100,
        "finished": "2016-01-31T00:10+00:00",
        "error": {"code": "action_failed", "message": "Action failed"},
    }


@pytest.fixture()
def action_response(action1_running):
    return {
        "action": action1_running,
    }


@pytest.fixture()
def action_list_response(action1_running, action2_running):
    return {
        "actions": [
            action1_running,
            action2_running,
        ],
    }


@pytest.fixture()
def hetzner_client() -> Generator[Client]:
    warn("DEPRECATED")
    client = Client(token="token")
    patcher = mock.patch.object(client, "request")
    patcher.start()
    yield client
    patcher.stop()
