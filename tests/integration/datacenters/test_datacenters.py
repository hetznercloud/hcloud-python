class TestDatacentersClient(object):
    def test_get_by_id(self, hetzner_client):
        datacenter = hetzner_client.datacenters.get_by_id(1)
        assert datacenter.id == 1
        assert datacenter.name == "fsn1-dc8"
        assert datacenter.description == "Falkenstein 1 DC 8"

    def test_get_all(self, hetzner_client):
        datacenters = hetzner_client.datacenters.get_all()
        assert datacenters[0].id == 1
        assert datacenters[0].name == "fsn1-dc8"
        assert datacenters[0].description == "Falkenstein 1 DC 8"
