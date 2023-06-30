from datetime import datetime, timedelta, timezone

import pytest

from hcloud._compat import isoparse


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        (
            "2023-06-29T15:37:22",
            datetime(2023, 6, 29, 15, 37, 22),
        ),
        (
            "2023-06-29T15:37:22+00:00",
            datetime(2023, 6, 29, 15, 37, 22, tzinfo=timezone.utc),
        ),
        (
            "2023-06-29T15:37:22+02:12",
            datetime(
                2023, 6, 29, 15, 37, 22, tzinfo=timezone(timedelta(hours=2, minutes=12))
            ),
        ),
        (
            "2023-06-29T15:37:22Z",
            datetime(2023, 6, 29, 15, 37, 22, tzinfo=timezone.utc),
        ),
        (
            "2023-06-29T15:37:22z",
            datetime(2023, 6, 29, 15, 37, 22, tzinfo=timezone.utc),
        ),
    ],
)
def test_isoparse(value: str, expected: datetime):
    assert isoparse(value) == expected
