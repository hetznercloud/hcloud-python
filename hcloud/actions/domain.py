# -*- coding: utf-8 -*-
from hcloud.core.domain import BaseDomain

from hcloud.helpers.descriptors import ISODateTime


class Action(BaseDomain):
    """Action Domain
    Description of all fields: <https://docs.hetzner.cloud/#actions-get-one-action>
    """
    STATUS_RUNNING = "running"
    """Action Status running"""
    STATUS_SUCCESS = "success"
    """Action Status success"""
    STATUS_ERROR = "error"
    """Action Status error"""

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
    """The Action you was waiting for failed"""
    def __init__(self, action):
        self.action = action


class ActionTimeoutException(Exception):
    """The Action you was waiting for timeouted in hcloud-python."""
    def __init__(self, action):
        self.action = action
