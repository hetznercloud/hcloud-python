from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

from .._exceptions import HCloudException
from ..core import BaseDomain

if TYPE_CHECKING:
    from .client import BoundAction

__all__ = [
    "ActionStatus",
    "Action",
    "ActionResource",
    "ActionError",
    "ActionException",
    "ActionFailedException",
    "ActionTimeoutException",
]

ActionStatus = Literal[
    "running",
    "success",
    "error",
]


class Action(BaseDomain):
    """Action Domain

    :param id: int ID of an action
    :param command: Command executed in the action
    :param status: Status of the action
    :param progress: Progress of action in percent
    :param started: Point in time when the action was started
    :param datetime,None finished: Point in time when the action was finished. Only set if the action is finished otherwise None
    :param resources: Resources the action relates to
    :param error: Error message for the action if error occurred, otherwise None.
    """

    STATUS_RUNNING = "running"
    """Action Status running"""
    STATUS_SUCCESS = "success"
    """Action Status success"""
    STATUS_ERROR = "error"
    """Action Status error"""

    __api_properties__ = (
        "id",
        "command",
        "status",
        "progress",
        "resources",
        "error",
        "started",
        "finished",
    )
    __slots__ = __api_properties__

    def __init__(
        self,
        id: int,
        command: str | None = None,
        status: ActionStatus | None = None,
        progress: int | None = None,
        started: str | None = None,
        finished: str | None = None,
        resources: list[ActionResource] | None = None,
        error: ActionError | None = None,
    ):
        self.id = id
        self.command = command

        self.status = status
        self.progress = progress
        self.started = self._parse_datetime(started)
        self.finished = self._parse_datetime(finished)
        self.resources = resources
        self.error = error


class ActionResource(TypedDict):
    id: int
    type: str


class ActionError(TypedDict):
    code: str
    message: str
    details: dict[str, Any]


class ActionException(HCloudException):
    """A generic action exception"""

    def __init__(self, action: Action | BoundAction):
        assert self.__doc__ is not None
        message = self.__doc__

        extras = []
        if (
            action.error is not None
            and "code" in action.error
            and "message" in action.error
        ):
            message += f": {action.error['message']}"

            extras.append(action.error["code"])
        else:
            if action.command is not None:
                extras.append(action.command)

        extras.append(str(action.id))
        message += f" ({', '.join(extras)})"

        super().__init__(message)
        self.message = message
        self.action = action


class ActionFailedException(ActionException):
    """The pending action failed"""


class ActionTimeoutException(ActionException):
    """The pending action timed out"""
