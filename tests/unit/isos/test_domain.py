from __future__ import annotations

from datetime import datetime, timezone

import pytest

from hcloud.isos import Iso


class TestIso:
    @pytest.fixture()
    def deprecated_iso(self):
        return Iso(
            **{
                "id": 10433,
                "name": "vyos-1.4-rolling-202111150317-amd64.iso",
                "description": "VyOS 1.4 (amd64)",
                "type": "public",
                "deprecation": {
                    "announced": "2023-10-05T08:27:01Z",
                    "unavailable_after": "2023-11-05T08:27:01Z",
                },
                "architecture": "x86",
                "deprecated": "2023-11-05T08:27:01Z",
            }
        )

    def test_deprecation(self, deprecated_iso: Iso):
        with pytest.deprecated_call():
            assert deprecated_iso.deprecated == datetime(
                2023, 11, 5, 8, 27, 1, tzinfo=timezone.utc
            )
        assert deprecated_iso.deprecation is not None
        assert deprecated_iso.deprecation.announced == datetime(
            2023, 10, 5, 8, 27, 1, tzinfo=timezone.utc
        )
        assert deprecated_iso.deprecation.unavailable_after == datetime(
            2023, 11, 5, 8, 27, 1, tzinfo=timezone.utc
        )
