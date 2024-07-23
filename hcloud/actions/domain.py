from __future__ import annotations

from typing import TYPE_CHECKING

from dateutil.parser import isoparse

from .._exceptions import HCloudException
from ..core import BaseDomain

if TYPE_CHECKING:
    from .client import BoundAction


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
        status: str | None = None,
        progress: int | None = None,
        started: str | None = None,
        finished: str | None = None,
        resources: list[dict] | None = None,
        error: dict | None = None,
    ):
        self.id = id
        self.command = command

        self.status = status
        self.progress = progress
        self.started = isoparse(started) if started else None
        self.finished = isoparse(finished) if finished else None
        self.resources = resources
        self.error = error


class ActionException(HCloudException):
    """A generic action exception"""

    def __init__(self, action: Action | BoundAction):
        assert self.__doc__ is not None
        message = self.__doc__
        if action.error is not None and "message" in action.error:
            message += f": {action.error['message']}"

        super().__init__(message)
        self.message = message
        self.action = action


class ActionFailedException(ActionException):
    """The pending action failed"""


class ActionTimeoutException(ActionException):
    """The pending action timed out"""
