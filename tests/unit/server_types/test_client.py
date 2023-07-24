from __future__ import annotations

from datetime import datetime, timezone
from unittest import mock

import pytest

from hcloud.server_types import BoundServerType, ServerTypesClient


class TestBoundServerType:
    @pytest.fixture()
    def bound_server_type(self, hetzner_client):
        return BoundServerType(client=hetzner_client.server_types, data=dict(id=14))

    def test_bound_server_type_init(self, server_type_response):
        bound_server_type = BoundServerType(
            client=mock.MagicMock(), data=server_type_response["server_type"]
        )

        assert bound_server_type.id == 1
        assert bound_server_type.name == "cx11"
        assert bound_server_type.description == "CX11"
        assert bound_server_type.cores == 1
        assert bound_server_type.memory == 1
        assert bound_server_type.disk == 25
        assert bound_server_type.storage_type == "local"
        assert bound_server_type.cpu_type == "shared"
        assert bound_server_type.architecture == "x86"
        assert bound_server_type.deprecated is True
        assert bound_server_type.deprecation is not None
        assert bound_server_type.deprecation.announced == datetime(
            2023, 6, 1, tzinfo=timezone.utc
        )
        assert bound_server_type.deprecation.unavailable_after == datetime(
            2023, 9, 1, tzinfo=timezone.utc
        )
        assert bound_server_type.included_traffic == 21990232555520


class TestServerTypesClient:
    @pytest.fixture()
    def server_types_client(self):
        return ServerTypesClient(client=mock.MagicMock())

    def test_get_by_id(self, server_types_client, server_type_response):
        server_types_client._client.request.return_value = server_type_response
        server_type = server_types_client.get_by_id(1)
        server_types_client._client.request.assert_called_with(
            url="/server_types/1", method="GET"
        )
        assert server_type._client is server_types_client
        assert server_type.id == 1
        assert server_type.name == "cx11"

    @pytest.mark.parametrize(
        "params", [{"name": "cx11", "page": 1, "per_page": 10}, {"name": ""}, {}]
    )
    def test_get_list(self, server_types_client, two_server_types_response, params):
        server_types_client._client.request.return_value = two_server_types_response
        result = server_types_client.get_list(**params)
        server_types_client._client.request.assert_called_with(
            url="/server_types", method="GET", params=params
        )

        server_types = result.server_types
        assert result.meta is None

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
    def test_get_all(self, server_types_client, two_server_types_response, params):
        server_types_client._client.request.return_value = two_server_types_response
        server_types = server_types_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        server_types_client._client.request.assert_called_with(
            url="/server_types", method="GET", params=params
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

    def test_get_by_name(self, server_types_client, one_server_types_response):
        server_types_client._client.request.return_value = one_server_types_response
        server_type = server_types_client.get_by_name("cx11")

        params = {"name": "cx11"}

        server_types_client._client.request.assert_called_with(
            url="/server_types", method="GET", params=params
        )

        assert server_type._client is server_types_client
        assert server_type.id == 1
        assert server_type.name == "cx11"
