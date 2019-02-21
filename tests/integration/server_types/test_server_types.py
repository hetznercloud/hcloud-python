
class TestServerTypesClient(object):

    def test_get_by_id(self, hetzner_client):
        server_type = hetzner_client.server_types.get_by_id(1)
        assert server_type.id == 1
        assert server_type.name == "cx11"
        assert server_type.description == "CX11"
        assert server_type.cores == 1
        assert server_type.memory == 1
        assert server_type.disk == 25
        assert server_type.prices == [
            {
                "location": "fsn1",
                "price_hourly": {
                    "net": "1.0000000000",
                    "gross": "1.1900000000000000"
                },
                "price_monthly": {
                    "net": "1.0000000000",
                    "gross": "1.1900000000000000"
                }
            }
        ]
        assert server_type.storage_type == "local"
        assert server_type.cpu_type == "shared"

    def test_get_by_name(self, hetzner_client):
        server_type = hetzner_client.server_types.get_by_name("cx11")
        assert server_type.id == 1
        assert server_type.name == "cx11"
        assert server_type.description == "CX11"
        assert server_type.cores == 1
        assert server_type.memory == 1
        assert server_type.disk == 25
        assert server_type.prices == [
            {
                "location": "fsn1",
                "price_hourly": {
                    "net": "1.0000000000",
                    "gross": "1.1900000000000000"
                },
                "price_monthly": {
                    "net": "1.0000000000",
                    "gross": "1.1900000000000000"
                }
            }
        ]
        assert server_type.storage_type == "local"
        assert server_type.cpu_type == "shared"

    def test_get_list(self, hetzner_client):
        result = hetzner_client.server_types.get_list()
        server_types = result.server_types
        assert server_types[0].id == 1
        assert server_types[0].name == "cx11"
        assert server_types[0].description == "CX11"
        assert server_types[0].cores == 1
        assert server_types[0].memory == 1
        assert server_types[0].disk == 25
        assert server_types[0].prices == [
            {
                "location": "fsn1",
                "price_hourly": {
                    "net": "1.0000000000",
                    "gross": "1.1900000000000000"
                },
                "price_monthly": {
                    "net": "1.0000000000",
                    "gross": "1.1900000000000000"
                }
            }
        ]
        assert server_types[0].storage_type == "local"
        assert server_types[0].cpu_type == "shared"
