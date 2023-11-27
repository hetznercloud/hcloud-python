from __future__ import annotations

from typing import Any


class HCloudException(Exception):
    """There was an error while using the hcloud library"""


class APIException(HCloudException):
    """There was an error while performing an API Request"""

    def __init__(self, code: int | str, message: str | None, details: Any):
        super().__init__(code if message is None and isinstance(code, str) else message)
        self.code = code
        self.message = message
        self.details = details
