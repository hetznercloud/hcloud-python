from __future__ import annotations

from typing import TypedDict

__all__ = [
    "DNSPtr",
]


class DNSPtr(TypedDict):
    ip: str
    dns_ptr: str
