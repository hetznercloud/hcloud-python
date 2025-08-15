# pylint: disable=redefined-outer-name

from __future__ import annotations

from unittest import mock

import pytest

from hcloud import Client


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
    c._client_hetzner.request = request_mock
    return c


@pytest.fixture()
def generic_action():
    return {
        "action": {
            "id": 1,
            "command": "stop_server",
            "status": "running",
            "progress": 0,
            "started": "2016-01-30T23:50+00:00",
            "finished": None,
            "resources": [{"id": 42, "type": "server"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }
