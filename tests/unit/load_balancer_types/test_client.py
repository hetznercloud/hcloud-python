from __future__ import annotations

from unittest import mock

import pytest
from dateutil.parser import isoparse

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
        load_balancer_type1,
    ):
        request_mock.return_value = {
            "load_balancer_type": load_balancer_type1,
        }

        result = load_balancer_types_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/load_balancer_types/1",
        )

        assert result._client is load_balancer_types_client
        assert result.id == 1
        assert result.name == "lb11"
        assert result.description == "LB11"
        assert result.max_connections == 10000
        assert result.max_services == 5
        assert result.max_targets == 25
        assert result.max_assigned_certificates == 10
        assert result.prices == [
            {
                "location": "fsn1",
                "price_hourly": {"net": "0.0120", "gross": "0.0120"},
                "price_monthly": {"net": "7.4900", "gross": "7.4900"},
                "price_per_tb_traffic": {"net": "1.0000", "gross": "1.0000"},
                "included_traffic": 21990232555520,
            }
        ]
        assert result.deprecation.announced == isoparse("2023-06-01T00:00:00+00:00")
        assert result.deprecation.unavailable_after == isoparse(
            "2023-09-01T00:00:00+00:00"
        )

    @pytest.mark.parametrize(
        "params", [{"name": "lb11", "page": 1, "per_page": 10}, {"name": ""}, {}]
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        load_balancer_types_client: LoadBalancerTypesClient,
        load_balancer_type1,
        load_balancer_type2,
        params,
    ):
        request_mock.return_value = {
            "load_balancer_types": [load_balancer_type1, load_balancer_type2],
        }

        result = load_balancer_types_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/load_balancer_types",
            params=params,
        )

        assert result.meta is not None
        assert len(result.load_balancer_types) == 2

        assert result.load_balancer_types[0]._client is load_balancer_types_client
        assert result.load_balancer_types[0].id == 1
        assert result.load_balancer_types[0].name == "lb11"

        assert result.load_balancer_types[1]._client is load_balancer_types_client
        assert result.load_balancer_types[1].id == 2
        assert result.load_balancer_types[1].name == "lb21"

    @pytest.mark.parametrize("params", [{"name": "lb11"}])
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        load_balancer_types_client: LoadBalancerTypesClient,
        load_balancer_type1,
        load_balancer_type2,
        params,
    ):
        request_mock.return_value = {
            "load_balancer_types": [load_balancer_type1, load_balancer_type2]
        }

        result = load_balancer_types_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/load_balancer_types",
            params=params,
        )

        assert len(result) == 2

        assert result[0]._client is load_balancer_types_client
        assert result[0].id == 1
        assert result[0].name == "lb11"

        assert result[1]._client is load_balancer_types_client
        assert result[1].id == 2
        assert result[1].name == "lb21"

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        load_balancer_types_client: LoadBalancerTypesClient,
        load_balancer_type1,
    ):
        request_mock.return_value = {
            "load_balancer_types": [load_balancer_type1],
        }

        result = load_balancer_types_client.get_by_name("lb11")

        request_mock.assert_called_with(
            method="GET",
            url="/load_balancer_types",
            params={"name": "lb11"},
        )

        assert result._client is load_balancer_types_client
        assert result.id == 1
        assert result.name == "lb11"
