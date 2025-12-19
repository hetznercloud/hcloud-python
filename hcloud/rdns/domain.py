from __future__ import annotations

from typing import TypedDict


class DNSPtr(TypedDict):
    ip: str
    dns_ptr: str
