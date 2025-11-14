from __future__ import annotations

import pytest

from hcloud.exp.zone import format_txt_record, is_txt_record_quoted


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("hello world", False),
        ('"hello world', False),
        ('"hello world"', True),
    ],
)
def test_is_txt_record_quoted(value: str, expected: bool):
    assert is_txt_record_quoted(value) == expected


MANY_A = "a" * 255
SOME_B = "b" * 10


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("", ""),
        ('""', '"\\"\\""'),
        ("hello world", '"hello world"'),
        ("hello\nworld", '"hello\nworld"'),
        ('hello "world"', '"hello \\"world\\""'),
        ('hello "world', '"hello \\"world"'),
        (MANY_A + SOME_B, f'"{MANY_A}" "{SOME_B}"'),
    ],
)
def test_format_txt_record(value: str, expected: str):
    assert format_txt_record(value) == expected
