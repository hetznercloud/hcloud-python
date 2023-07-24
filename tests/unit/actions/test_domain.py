from __future__ import annotations

import datetime
from datetime import timezone

import pytest

from hcloud.actions import (
    Action,
    ActionException,
    ActionFailedException,
    ActionTimeoutException,
)


class TestAction:
    def test_started_finished_is_datetime(self):
        action = Action(
            id=1, started="2016-01-30T23:50+00:00", finished="2016-03-30T23:50+00:00"
        )
        assert action.started == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
        assert action.finished == datetime.datetime(
            2016, 3, 30, 23, 50, tzinfo=timezone.utc
        )


def test_action_exceptions():
    with pytest.raises(
        ActionException,
        match=r"The pending action failed: Server does not exist anymore",
    ):
        raise ActionFailedException(
            action=Action(
                **{
                    "id": 1084730887,
                    "command": "change_server_type",
                    "status": "error",
                    "progress": 100,
                    "resources": [{"id": 34574042, "type": "server"}],
                    "error": {
                        "code": "server_does_not_exist_anymore",
                        "message": "Server does not exist anymore",
                    },
                    "started": "2023-07-06T14:52:42+00:00",
                    "finished": "2023-07-06T14:53:08+00:00",
                }
            )
        )

    with pytest.raises(ActionException, match=r"The pending action timed out"):
        raise ActionTimeoutException(
            action=Action(
                **{
                    "id": 1084659545,
                    "command": "create_server",
                    "status": "running",
                    "progress": 50,
                    "started": "2023-07-06T13:58:38+00:00",
                    "finished": None,
                    "resources": [{"id": 34572291, "type": "server"}],
                    "error": None,
                }
            )
        )
