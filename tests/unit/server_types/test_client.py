import pytest
import mock


from hcloud.server_types.client import ServerTypesClient


class TestServerTypesClient(object):

    @pytest.fixture()
    def server_types_client(self):
        return ServerTypesClient(client=mock.MagicMock())

    def test_get_by_id(self, server_types_client, server_type_response):
        server_types_client._client.request.return_value = server_type_response
        server_type = server_types_client.get_by_id(1)
        server_types_client._client.request.assert_called_with(url="/server_types/1", method="GET")
        assert server_type._client is server_types_client
        assert server_type.id == 1
        assert server_type.name == "cx11"

    def test_get_all_no_params(self, server_types_client, two_server_types_response):
        server_types_client._client.request.return_value = two_server_types_response
        server_types = server_types_client.get_all()
        server_types_client._client.request.assert_called_with(url="/server_types", method="GET", params={})

        assert len(server_types) == 2

        server_types1 = server_types[0]
        server_types2 = server_types[1]

        assert server_types1._client is server_types_client
        assert server_types1.id == 1
        assert server_types1.name == "cx11"

        assert server_types2._client is server_types_client
        assert server_types2.id == 2
        assert server_types2.name == "cx21"

    @pytest.mark.parametrize("params", [{'name': "cx11"}])
    def test_get_all_with_params(self, server_types_client, params):
        server_types_client.get_all(**params)
        server_types_client._client.request.assert_called_with(url="/server_types", method="GET", params=params)

