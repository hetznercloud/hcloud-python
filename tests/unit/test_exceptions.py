from __future__ import annotations

import pytest

from hcloud import (
    APIException,
    HCloudException,
)
from hcloud.actions import Action, ActionFailedException, ActionTimeoutException

running_action = Action(
    id=12345,
    command="action_command",
    status=Action.STATUS_RUNNING,
)

failed_action = Action(
    id=12345,
    command="action_command",
    status=Action.STATUS_ERROR,
    error={"code": "action_failed", "message": "Action failed"},
)


@pytest.mark.parametrize(
    ("exception", "expected"),
    [
        (
            # Should never be raised by itself
            HCloudException(),
            "",
        ),
        (
            # Should never be raised by itself
            HCloudException("A test error"),
            "A test error",
        ),
        (
            APIException(code="conflict", message="API error message", details=None),
            "API error message (conflict)",
        ),
        (
            APIException(
                code="conflict",
                message="API error message",
                details=None,
                correlation_id="fddea8fabd02fb21",
            ),
            "API error message (conflict, fddea8fabd02fb21)",
        ),
        (
            ActionFailedException(failed_action),
            "The pending action failed: Action failed (action_failed, 12345)",
        ),
        (
            ActionTimeoutException(running_action),
            "The pending action timed out (action_command, 12345)",
        ),
    ],
)
def test_exceptions(exception, expected):
    assert str(exception) == expected
