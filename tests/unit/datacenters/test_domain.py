from __future__ import annotations

import warnings

import pytest

from hcloud.datacenters import Datacenter, DatacenterServerTypes

warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest.mark.parametrize(
    "value",
    [
        (Datacenter(id=1),),
        (DatacenterServerTypes(available=[], available_for_migration=[], supported=[])),
    ],
)
def test_eq(value):
    assert value.__eq__(value)
