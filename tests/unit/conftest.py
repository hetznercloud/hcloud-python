import mock
import pytest


@pytest.fixture(autouse=True, scope='function')
def mocked_requests():
    patcher = mock.patch('hcloud.hcloud.requests')
    mocked_requests = patcher.start()
    yield mocked_requests
    patcher.stop()


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
