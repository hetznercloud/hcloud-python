# pylint: disable=redefined-outer-name

from __future__ import annotations

from unittest import mock

import pytest

from hcloud import Client
from hcloud.actions import BoundAction


@pytest.fixture()
def request_mock():
    return mock.MagicMock()


@pytest.fixture()
def client(request_mock):
    c = Client(token="TOKEN")
    c.request = request_mock
    return c


def assert_action1(o: BoundAction, client: Client):
    assert o.id == 1
    assert o.command == "command"
    assert o._client == client.actions


def assert_action2(o: BoundAction, client: Client):
    assert o.id == 2
    assert o.command == "command"
    assert o._client == client.actions


@pytest.fixture()
def action1_running():
    return {
        "id": 1,
        "command": "command",
        "status": "running",
        "progress": 20,
        "started": "2025-01-30T23:50+00:00",
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
        "progress": 40,
        "started": "2025-01-30T23:50+00:00",
        "finished": None,
        "resources": [{"id": 666, "type": "resource"}],
        "error": None,
    }


@pytest.fixture()
def action1_success(action1_running):
    return {
        **action1_running,
        "status": "success",
        "progress": 100,
        "finished": "2025-01-30T10:40+00:00",
    }


@pytest.fixture()
def action2_success(action2_running):
    return {
        **action2_running,
        "status": "success",
        "progress": 100,
        "finished": "2025-01-30T10:40+00:00",
    }


@pytest.fixture()
def action1_error(action1_running):
    return {
        **action1_running,
        "status": "error",
        "progress": 100,
        "finished": "2025-01-30T10:40+00:00",
        "error": {"code": "action_failed", "message": "Action failed"},
    }


@pytest.fixture()
def action2_error(action2_running):
    return {
        **action2_running,
        "status": "error",
        "progress": 100,
        "finished": "2025-01-30T10:40+00:00",
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
        ]
    }
