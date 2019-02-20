class TestDatacentersClient(object):
    def test_get_by_id(self, hetzner_client):
        datacenter = hetzner_client.datacenters.get_by_id(1)
        assert datacenter.id == 1
        assert datacenter.name == "fsn1-dc8"
        assert datacenter.description == "Falkenstein 1 DC 8"

    def test_get_by_name(self, hetzner_client):
        datacenter = hetzner_client.datacenters.get_by_name("fsn1-dc8")
        assert datacenter.id == 1
        assert datacenter.name == "fsn1-dc8"
        assert datacenter.description == "Falkenstein 1 DC 8"

    def test_get_list(self, hetzner_client):
        result = hetzner_client.datacenters.get_list()
        datacenters = result.datacenters
        assert datacenters[0].id == 1
        assert datacenters[0].name == "fsn1-dc8"
        assert datacenters[0].description == "Falkenstein 1 DC 8"
