from __future__ import annotations

import pytest

from hcloud.datacenters import Datacenter, DatacenterServerTypes


@pytest.mark.parametrize(
    "value",
    [
        (Datacenter(id=1),),
        (DatacenterServerTypes(available=[], available_for_migration=[], supported=[])),
    ],
)
def test_eq(value):
    assert value == value
