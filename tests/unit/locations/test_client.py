import pytest  # noqa: F401
import mock  # noqa: F401

from hcloud.locations.client import LocationsClient


class TestLocationsClient(object):

    @pytest.fixture()
    def locations_client(self):
        return LocationsClient(client=mock.MagicMock())

    def test_get_by_id(self, locations_client, location_response):
        locations_client._client.request.return_value = location_response
        location = locations_client.get_by_id(1)
        locations_client._client.request.assert_called_with(url="/locations/1", method="GET")
        assert location._client is locations_client
        assert location.id == 1
        assert location.name == "fsn1"

    def test_get_all_no_params(self, locations_client, two_locations_response):
        locations_client._client.request.return_value = two_locations_response
        locations = locations_client.get_all()
        locations_client._client.request.assert_called_with(url="/locations", method="GET", params={})

        assert len(locations) == 2

        location1 = locations[0]
        location2 = locations[1]

        assert location1._client is locations_client
        assert location1.id == 1
        assert location1.name == "fsn1"

        assert location2._client is locations_client
        assert location2.id == 2
        assert location2.name == "nbg1"

    @pytest.mark.parametrize("params", [{'name': "fsn1"}])
    def test_get_all_with_params(self, locations_client, params):
        locations_client.get_all(**params)
        locations_client._client.request.assert_called_with(url="/locations", method="GET", params=params)
