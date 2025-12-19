"""
The `exp.zone` module is a namespace that holds experimental features for the `hcloud-python`
library, breaking changes may occur within minor releases.
"""

from __future__ import annotations

__all__ = [
    "is_txt_record_quoted",
    "format_txt_record",
]


def is_txt_record_quoted(value: str) -> bool:
    """
    Check whether a TXT record is already quoted.

    - hello world	=> false
    - "hello world"	=> true
    """
    return value.startswith('"') and value.endswith('"')


def format_txt_record(value: str) -> str:
    """
    Format a TXT record by splitting it in quoted strings of 255 characters.
    Existing quotes will be escaped.

    - hello world	=> "hello world"
    - hello "world"	=> "hello \"world\""
    """
    value = value.replace('"', '\\"')

    parts = []
    for start in range(0, len(value), 255):
        end = min(start + 255, len(value))
        parts.append('"' + value[start:end] + '"')
    value = " ".join(parts)

    return value
