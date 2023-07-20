from __future__ import annotations

import pytest


@pytest.fixture()
def generic_action_list():
    return {
        "actions": [
            {
                "id": 1,
                "command": "start_server",
                "status": "success",
                "progress": 100,
                "started": "2016-01-30T23:55:00+00:00",
                "finished": "2016-01-30T23:56:00+00:00",
                "resources": [{"id": 42, "type": "server"}],
                "error": {"code": "action_failed", "message": "Action failed"},
            },
            {
                "id": 2,
                "command": "stop_server",
                "status": "success",
                "progress": 100,
                "started": "2016-01-30T23:55:00+00:00",
                "finished": "2016-01-30T23:56:00+00:00",
                "resources": [{"id": 42, "type": "server"}],
                "error": {"code": "action_failed", "message": "Action failed"},
            },
        ]
    }


@pytest.fixture()
def running_action():
    return {
        "action": {
            "id": 2,
            "command": "stop_server",
            "status": "running",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 42, "type": "server"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def successfully_action():
    return {
        "action": {
            "id": 2,
            "command": "stop_server",
            "status": "success",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 42, "type": "server"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }


@pytest.fixture()
def failed_action():
    return {
        "action": {
            "id": 2,
            "command": "stop_server",
            "status": "error",
            "progress": 100,
            "started": "2016-01-30T23:55:00+00:00",
            "finished": "2016-01-30T23:56:00+00:00",
            "resources": [{"id": 42, "type": "server"}],
            "error": {"code": "action_failed", "message": "Action failed"},
        }
    }
