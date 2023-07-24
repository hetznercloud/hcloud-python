from __future__ import annotations

from unittest import mock  # noqa: F401

import pytest  # noqa: F401

from hcloud.locations import LocationsClient


class TestLocationsClient:
    @pytest.fixture()
    def locations_client(self):
        return LocationsClient(client=mock.MagicMock())

    def test_get_by_id(self, locations_client, location_response):
        locations_client._client.request.return_value = location_response
        location = locations_client.get_by_id(1)
        locations_client._client.request.assert_called_with(
            url="/locations/1", method="GET"
        )
        assert location._client is locations_client
        assert location.id == 1
        assert location.name == "fsn1"
        assert location.network_zone == "eu-central"

    @pytest.mark.parametrize(
        "params", [{"name": "fsn1", "page": 1, "per_page": 10}, {"name": ""}, {}]
    )
    def test_get_list(self, locations_client, two_locations_response, params):
        locations_client._client.request.return_value = two_locations_response
        result = locations_client.get_list(**params)
        locations_client._client.request.assert_called_with(
            url="/locations", method="GET", params=params
        )

        locations = result.locations
        assert result.meta is None

        assert len(locations) == 2

        location1 = locations[0]
        location2 = locations[1]

        assert location1._client is locations_client
        assert location1.id == 1
        assert location1.name == "fsn1"
        assert location1.network_zone == "eu-central"

        assert location2._client is locations_client
        assert location2.id == 2
        assert location2.name == "nbg1"
        assert location2.network_zone == "eu-central"

    @pytest.mark.parametrize("params", [{"name": "fsn1"}, {}])
    def test_get_all(self, locations_client, two_locations_response, params):
        locations_client._client.request.return_value = two_locations_response
        locations = locations_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        locations_client._client.request.assert_called_with(
            url="/locations", method="GET", params=params
        )

        assert len(locations) == 2

        location1 = locations[0]
        location2 = locations[1]

        assert location1._client is locations_client
        assert location1.id == 1
        assert location1.name == "fsn1"
        assert location1.network_zone == "eu-central"

        assert location2._client is locations_client
        assert location2.id == 2
        assert location2.name == "nbg1"
        assert location2.network_zone == "eu-central"

    def test_get_by_name(self, locations_client, one_locations_response):
        locations_client._client.request.return_value = one_locations_response
        location = locations_client.get_by_name("fsn1")

        params = {"name": "fsn1"}

        locations_client._client.request.assert_called_with(
            url="/locations", method="GET", params=params
        )

        assert location._client is locations_client
        assert location.id == 1
        assert location.name == "fsn1"
        assert location.network_zone == "eu-central"
