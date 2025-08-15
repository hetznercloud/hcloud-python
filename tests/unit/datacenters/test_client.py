from __future__ import annotations

from unittest import mock  # noqa: F401

import pytest  # noqa: F401

from hcloud import Client
from hcloud.datacenters import BoundDatacenter, DatacentersClient, DatacenterServerTypes
from hcloud.locations import BoundLocation


class TestBoundDatacenter:
    def test_bound_datacenter_init(self, datacenter_response):
        bound_datacenter = BoundDatacenter(
            client=mock.MagicMock(), data=datacenter_response["datacenter"]
        )

        assert bound_datacenter.id == 1
        assert bound_datacenter.name == "fsn1-dc8"
        assert bound_datacenter.description == "Falkenstein 1 DC 8"
        assert bound_datacenter.complete is True

        assert isinstance(bound_datacenter.location, BoundLocation)
        assert bound_datacenter.location.id == 1
        assert bound_datacenter.location.name == "fsn1"
        assert bound_datacenter.location.complete is True

        assert isinstance(bound_datacenter.server_types, DatacenterServerTypes)
        assert len(bound_datacenter.server_types.supported) == 3
        assert bound_datacenter.server_types.supported[0].id == 1
        assert bound_datacenter.server_types.supported[0].complete is False
        assert bound_datacenter.server_types.supported[1].id == 2
        assert bound_datacenter.server_types.supported[1].complete is False
        assert bound_datacenter.server_types.supported[2].id == 3
        assert bound_datacenter.server_types.supported[2].complete is False

        assert len(bound_datacenter.server_types.available) == 3
        assert bound_datacenter.server_types.available[0].id == 1
        assert bound_datacenter.server_types.available[0].complete is False
        assert bound_datacenter.server_types.available[1].id == 2
        assert bound_datacenter.server_types.available[1].complete is False
        assert bound_datacenter.server_types.available[2].id == 3
        assert bound_datacenter.server_types.available[2].complete is False

        assert len(bound_datacenter.server_types.available_for_migration) == 3
        assert bound_datacenter.server_types.available_for_migration[0].id == 1
        assert (
            bound_datacenter.server_types.available_for_migration[0].complete is False
        )
        assert bound_datacenter.server_types.available_for_migration[1].id == 2
        assert (
            bound_datacenter.server_types.available_for_migration[1].complete is False
        )
        assert bound_datacenter.server_types.available_for_migration[2].id == 3
        assert (
            bound_datacenter.server_types.available_for_migration[2].complete is False
        )


class TestDatacentersClient:
    @pytest.fixture()
    def datacenters_client(self, client: Client):
        return DatacentersClient(client)

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        datacenters_client: DatacentersClient,
        datacenter_response,
    ):
        request_mock.return_value = datacenter_response

        datacenter = datacenters_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/datacenters/1",
        )
        assert datacenter._client is datacenters_client
        assert datacenter.id == 1
        assert datacenter.name == "fsn1-dc8"

    @pytest.mark.parametrize(
        "params", [{"name": "fsn1", "page": 1, "per_page": 10}, {"name": ""}, {}]
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        datacenters_client: DatacentersClient,
        two_datacenters_response,
        params,
    ):
        request_mock.return_value = two_datacenters_response

        result = datacenters_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/datacenters",
            params=params,
        )

        datacenters = result.datacenters
        assert result.meta is not None

        assert len(datacenters) == 2

        datacenter1 = datacenters[0]
        datacenter2 = datacenters[1]

        assert datacenter1._client is datacenters_client
        assert datacenter1.id == 1
        assert datacenter1.name == "fsn1-dc8"
        assert isinstance(datacenter1.location, BoundLocation)

        assert datacenter2._client is datacenters_client
        assert datacenter2.id == 2
        assert datacenter2.name == "nbg1-dc3"
        assert isinstance(datacenter2.location, BoundLocation)

    @pytest.mark.parametrize("params", [{"name": "fsn1"}, {}])
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        datacenters_client: DatacentersClient,
        two_datacenters_response,
        params,
    ):
        request_mock.return_value = two_datacenters_response

        datacenters = datacenters_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/datacenters",
            params=params,
        )

        assert len(datacenters) == 2

        datacenter1 = datacenters[0]
        datacenter2 = datacenters[1]

        assert datacenter1._client is datacenters_client
        assert datacenter1.id == 1
        assert datacenter1.name == "fsn1-dc8"
        assert isinstance(datacenter1.location, BoundLocation)

        assert datacenter2._client is datacenters_client
        assert datacenter2.id == 2
        assert datacenter2.name == "nbg1-dc3"
        assert isinstance(datacenter2.location, BoundLocation)

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        datacenters_client: DatacentersClient,
        one_datacenters_response,
    ):
        request_mock.return_value = one_datacenters_response

        datacenter = datacenters_client.get_by_name("fsn1-dc8")

        params = {"name": "fsn1-dc8"}

        request_mock.assert_called_with(
            method="GET",
            url="/datacenters",
            params=params,
        )

        assert datacenter._client is datacenters_client
        assert datacenter.id == 1
        assert datacenter.name == "fsn1-dc8"
        assert isinstance(datacenter.location, BoundLocation)
