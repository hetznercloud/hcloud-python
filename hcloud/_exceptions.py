from __future__ import annotations

from typing import Any


class HCloudException(Exception):
    """There was an error while using the hcloud library"""


class APIException(HCloudException):
    """There was an error while performing an API Request"""

    def __init__(self, code: int | str, message: str, details: Any):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details
