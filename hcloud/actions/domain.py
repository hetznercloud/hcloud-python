# -*- coding: utf-8 -*-
from hcloud.core.domain import BaseDomain

from hcloud.helpers.descriptors import ISODateTime


class Action(BaseDomain):
    STATUS_RUNNING = "running"
    STATUS_SUCCESS = "success"
    STATUS_ERROR = "error"

    started = ISODateTime()
    finished = ISODateTime()

    __slots__ = (
        "id",
        "command",
        "status",
        "progress",
        "resources",
        "error",
    )

    def __init__(
        self,
        id,
        command=None,
        status=None,
        progress=None,
        started=None,
        finished=None,
        resources=None,
        error=None
    ):
        self.id = id
        self.command = command
        self.status = status
        self.progress = progress
        self.started = started
        self.finished = finished
        self.resources = resources
        self.error = error


class ActionFailedException(Exception):
    def __init__(self, action):
        self.action = action


class ActionTimeoutException(Exception):
    def __init__(self, action):
        self.action = action
