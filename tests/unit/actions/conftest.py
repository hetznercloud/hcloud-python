import pytest


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
            "resources": [
                {
                    "id": 42,
                    "type": "server"
                }
            ],
            "error": {
                "code": "action_failed",
                "message": "Action failed"
            }
        }
    }
