from __future__ import annotations

from unittest import mock

import pytest

from hcloud.load_balancer_types import LoadBalancerTypesClient


class TestLoadBalancerTypesClient:
    @pytest.fixture()
    def load_balancer_types_client(self):
        return LoadBalancerTypesClient(client=mock.MagicMock())

    def test_get_by_id(self, load_balancer_types_client, load_balancer_type_response):
        load_balancer_types_client._client.request.return_value = (
            load_balancer_type_response
        )
        load_balancer_type = load_balancer_types_client.get_by_id(1)
        load_balancer_types_client._client.request.assert_called_with(
            url="/load_balancer_types/1", method="GET"
        )
        assert load_balancer_type._client is load_balancer_types_client
        assert load_balancer_type.id == 1
        assert load_balancer_type.name == "LB11"

    @pytest.mark.parametrize(
        "params", [{"name": "LB11", "page": 1, "per_page": 10}, {"name": ""}, {}]
    )
    def test_get_list(
        self, load_balancer_types_client, two_load_balancer_types_response, params
    ):
        load_balancer_types_client._client.request.return_value = (
            two_load_balancer_types_response
        )
        result = load_balancer_types_client.get_list(**params)
        load_balancer_types_client._client.request.assert_called_with(
            url="/load_balancer_types", method="GET", params=params
        )

        load_balancer_types = result.load_balancer_types
        assert result.meta is None

        assert len(load_balancer_types) == 2

        load_balancer_types1 = load_balancer_types[0]
        load_balancer_types2 = load_balancer_types[1]

        assert load_balancer_types1._client is load_balancer_types_client
        assert load_balancer_types1.id == 1
        assert load_balancer_types1.name == "LB11"

        assert load_balancer_types2._client is load_balancer_types_client
        assert load_balancer_types2.id == 2
        assert load_balancer_types2.name == "LB21"

    @pytest.mark.parametrize("params", [{"name": "LB21"}])
    def test_get_all(
        self, load_balancer_types_client, two_load_balancer_types_response, params
    ):
        load_balancer_types_client._client.request.return_value = (
            two_load_balancer_types_response
        )
        load_balancer_types = load_balancer_types_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        load_balancer_types_client._client.request.assert_called_with(
            url="/load_balancer_types", method="GET", params=params
        )

        assert len(load_balancer_types) == 2

        load_balancer_types1 = load_balancer_types[0]
        load_balancer_types2 = load_balancer_types[1]

        assert load_balancer_types1._client is load_balancer_types_client
        assert load_balancer_types1.id == 1
        assert load_balancer_types1.name == "LB11"

        assert load_balancer_types2._client is load_balancer_types_client
        assert load_balancer_types2.id == 2
        assert load_balancer_types2.name == "LB21"

    def test_get_by_name(
        self, load_balancer_types_client, one_load_balancer_types_response
    ):
        load_balancer_types_client._client.request.return_value = (
            one_load_balancer_types_response
        )
        load_balancer_type = load_balancer_types_client.get_by_name("LB21")

        params = {"name": "LB21"}

        load_balancer_types_client._client.request.assert_called_with(
            url="/load_balancer_types", method="GET", params=params
        )

        assert load_balancer_type._client is load_balancer_types_client
        assert load_balancer_type.id == 2
        assert load_balancer_type.name == "LB21"
