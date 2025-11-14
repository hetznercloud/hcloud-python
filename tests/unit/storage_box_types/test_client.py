# pylint: disable=protected-access

from __future__ import annotations

from unittest import mock

import pytest
from dateutil.parser import isoparse

from hcloud import Client
from hcloud.storage_box_types import (
    BoundStorageBoxType,
    StorageBoxTypesClient,
)


def assert_bound_model(
    o: BoundStorageBoxType,
    client: StorageBoxTypesClient,
):
    assert isinstance(o, BoundStorageBoxType)
    assert o._client is client
    assert o.id == 42
    assert o.name == "bx11"


class TestClient:
    @pytest.fixture()
    def resource_client(self, client: Client) -> StorageBoxTypesClient:
        return client.storage_box_types

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxTypesClient,
        storage_box_type1,
    ):
        request_mock.return_value = {"storage_box_type": storage_box_type1}

        result = resource_client.get_by_id(42)

        request_mock.assert_called_with(
            method="GET",
            url="/storage_box_types/42",
        )

        assert_bound_model(result, resource_client)
        assert result.description == "BX11"
        assert result.snapshot_limit == 10
        assert result.automatic_snapshot_limit == 10
        assert result.subaccounts_limit == 100
        assert result.size == 1099511627776
        assert result.prices == [
            {
                "location": "fsn1",
                "price_hourly": {"gross": "0.0051", "net": "0.0051"},
                "price_monthly": {"gross": "3.2000", "net": "3.2000"},
                "setup_fee": {"gross": "0.0000", "net": "0.0000"},
            }
        ]
        assert result.deprecation.announced == isoparse("2023-06-01T00:00:00+00:00")
        assert result.deprecation.unavailable_after == isoparse(
            "2023-09-01T00:00:00+00:00"
        )

    @pytest.mark.parametrize(
        "params",
        [
            {"name": "bx11", "page": 1, "per_page": 10},
            {},
        ],
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxTypesClient,
        storage_box_type1,
        storage_box_type2,
        params,
    ):
        request_mock.return_value = {
            "storage_box_types": [storage_box_type1, storage_box_type2]
        }

        result = resource_client.get_list(**params)

        request_mock.assert_called_with(
            url="/storage_box_types",
            method="GET",
            params=params,
        )

        assert result.meta is not None
        assert len(result.storage_box_types) == 2

        result1 = result.storage_box_types[0]
        result2 = result.storage_box_types[1]

        assert result1._client is resource_client
        assert result1.id == 42
        assert result1.name == "bx11"

        assert result2._client is resource_client
        assert result2.id == 43
        assert result2.name == "bx21"

    @pytest.mark.parametrize(
        "params",
        [
            {"name": "bx11"},
            {},
        ],
    )
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxTypesClient,
        storage_box_type1,
        storage_box_type2,
        params,
    ):
        request_mock.return_value = {
            "storage_box_types": [storage_box_type1, storage_box_type2]
        }

        result = resource_client.get_all(**params)

        request_mock.assert_called_with(
            url="/storage_box_types",
            method="GET",
            params={**params, "page": 1, "per_page": 50},
        )

        assert len(result) == 2

        result1 = result[0]
        result2 = result[1]

        assert result1._client is resource_client
        assert result1.id == 42
        assert result1.name == "bx11"

        assert result2._client is resource_client
        assert result2.id == 43
        assert result2.name == "bx21"

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        resource_client: StorageBoxTypesClient,
        storage_box_type1,
    ):
        request_mock.return_value = {"storage_box_types": [storage_box_type1]}

        result = resource_client.get_by_name("bx11")

        params = {"name": "bx11"}

        request_mock.assert_called_with(
            method="GET",
            url="/storage_box_types",
            params=params,
        )

        assert_bound_model(result, resource_client)
