from __future__ import annotations

from unittest import mock

import pytest

from hcloud import Client
from hcloud.load_balancer_types import LoadBalancerTypesClient


class TestLoadBalancerTypesClient:
    @pytest.fixture()
    def load_balancer_types_client(self, client: Client):
        return LoadBalancerTypesClient(client)

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        load_balancer_types_client: LoadBalancerTypesClient,
        load_balancer_type_response,
    ):
        request_mock.return_value = load_balancer_type_response

        load_balancer_type = load_balancer_types_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/load_balancer_types/1",
        )
        assert load_balancer_type._client is load_balancer_types_client
        assert load_balancer_type.id == 1
        assert load_balancer_type.name == "LB11"

    @pytest.mark.parametrize(
        "params", [{"name": "LB11", "page": 1, "per_page": 10}, {"name": ""}, {}]
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        load_balancer_types_client: LoadBalancerTypesClient,
        two_load_balancer_types_response,
        params,
    ):
        request_mock.return_value = two_load_balancer_types_response

        result = load_balancer_types_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/load_balancer_types",
            params=params,
        )

        load_balancer_types = result.load_balancer_types
        assert result.meta is not None

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
        self,
        request_mock: mock.MagicMock,
        load_balancer_types_client: LoadBalancerTypesClient,
        two_load_balancer_types_response,
        params,
    ):
        request_mock.return_value = two_load_balancer_types_response

        load_balancer_types = load_balancer_types_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/load_balancer_types",
            params=params,
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
        self,
        request_mock: mock.MagicMock,
        load_balancer_types_client: LoadBalancerTypesClient,
        one_load_balancer_types_response,
    ):
        request_mock.return_value = one_load_balancer_types_response

        load_balancer_type = load_balancer_types_client.get_by_name("LB21")

        params = {"name": "LB21"}

        request_mock.assert_called_with(
            method="GET",
            url="/load_balancer_types",
            params=params,
        )

        assert load_balancer_type._client is load_balancer_types_client
        assert load_balancer_type.id == 2
        assert load_balancer_type.name == "LB21"
