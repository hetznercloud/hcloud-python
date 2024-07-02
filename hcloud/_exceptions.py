from __future__ import annotations

from typing import Any


class HCloudException(Exception):
    """There was an error while using the hcloud library"""


class APIException(HCloudException):
    """There was an error while performing an API Request"""

    def __init__(
        self,
        code: int | str,
        message: str,
        details: Any,
        *,
        trace_id: str | None = None,
    ):
        extras = [str(code)]
        if trace_id is not None:
            extras.append(trace_id)

        error = f"{message} ({', '.join(extras)})"

        super().__init__(error)
        self.code = code
        self.message = message
        self.details = details
        self.trace_id = trace_id
