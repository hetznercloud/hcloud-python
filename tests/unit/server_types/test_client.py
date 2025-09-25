from __future__ import annotations

from datetime import datetime, timezone
from unittest import mock

import pytest

from hcloud import Client
from hcloud.server_types import BoundServerType, ServerTypesClient


class TestBoundServerType:
    @pytest.fixture()
    def bound_server_type(self, client: Client):
        return BoundServerType(client.server_types, data=dict(id=14))

    def test_init(self, server_type_response):
        o = BoundServerType(
            client=mock.MagicMock(), data=server_type_response["server_type"]
        )

        assert o.id == 1
        assert o.name == "cx11"
        assert o.description == "CX11"
        assert o.category == "Shared vCPU"
        assert o.cores == 1
        assert o.memory == 1
        assert o.disk == 25
        assert o.storage_type == "local"
        assert o.cpu_type == "shared"
        assert o.architecture == "x86"
        assert len(o.locations) == 2
        assert o.locations[0].location.id == 1
        assert o.locations[0].location.name == "nbg1"
        assert o.locations[0].deprecation is None
        assert o.locations[1].location.id == 2
        assert o.locations[1].location.name == "fsn1"
        assert (
            o.locations[1].deprecation.announced.isoformat()
            == "2023-06-01T00:00:00+00:00"
        )
        assert (
            o.locations[1].deprecation.unavailable_after.isoformat()
            == "2023-09-01T00:00:00+00:00"
        )

        with pytest.deprecated_call():
            assert o.deprecated is True
            assert o.deprecation is not None
            assert o.deprecation.announced == datetime(2023, 6, 1, tzinfo=timezone.utc)
            assert o.deprecation.unavailable_after == datetime(
                2023, 9, 1, tzinfo=timezone.utc
            )
            assert o.included_traffic == 21990232555520


class TestServerTypesClient:
    @pytest.fixture()
    def server_types_client(self, client: Client):
        return ServerTypesClient(client)

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        server_types_client: ServerTypesClient,
        server_type_response,
    ):
        request_mock.return_value = server_type_response

        server_type = server_types_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/server_types/1",
        )
        assert server_type._client is server_types_client
        assert server_type.id == 1
        assert server_type.name == "cx11"

    @pytest.mark.parametrize(
        "params", [{"name": "cx11", "page": 1, "per_page": 10}, {"name": ""}, {}]
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        server_types_client: ServerTypesClient,
        two_server_types_response,
        params,
    ):
        request_mock.return_value = two_server_types_response

        result = server_types_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/server_types",
            params=params,
        )

        server_types = result.server_types
        assert result.meta is not None

        assert len(server_types) == 2

        server_types1 = server_types[0]
        server_types2 = server_types[1]

        assert server_types1._client is server_types_client
        assert server_types1.id == 1
        assert server_types1.name == "cx11"

        assert server_types2._client is server_types_client
        assert server_types2.id == 2
        assert server_types2.name == "cx21"

    @pytest.mark.parametrize("params", [{"name": "cx11"}])
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        server_types_client: ServerTypesClient,
        two_server_types_response,
        params,
    ):
        request_mock.return_value = two_server_types_response

        server_types = server_types_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/server_types",
            params=params,
        )

        assert len(server_types) == 2

        server_types1 = server_types[0]
        server_types2 = server_types[1]

        assert server_types1._client is server_types_client
        assert server_types1.id == 1
        assert server_types1.name == "cx11"

        assert server_types2._client is server_types_client
        assert server_types2.id == 2
        assert server_types2.name == "cx21"

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        server_types_client: ServerTypesClient,
        one_server_types_response,
    ):
        request_mock.return_value = one_server_types_response

        server_type = server_types_client.get_by_name("cx11")

        params = {"name": "cx11"}

        request_mock.assert_called_with(
            method="GET",
            url="/server_types",
            params=params,
        )

        assert server_type._client is server_types_client
        assert server_type.id == 1
        assert server_type.name == "cx11"
