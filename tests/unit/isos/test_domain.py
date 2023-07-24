from __future__ import annotations

import datetime
from datetime import timezone

from hcloud.isos import Iso


class TestIso:
    def test_deprecated_is_datetime(self):
        iso = Iso(id=1, deprecated="2016-01-30T23:50+00:00")
        assert iso.deprecated == datetime.datetime(
            2016, 1, 30, 23, 50, tzinfo=timezone.utc
        )
