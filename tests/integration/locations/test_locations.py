class TestLocationsClient(object):
    def test_get_by_id(self, hetzner_client):
        location = hetzner_client.locations.get_by_id(1)
        assert location.id == 1
        assert location.name == "fsn1"
        assert location.description == "Falkenstein DC Park 1"

    def test_get_all(self, hetzner_client):
        locations = hetzner_client.locations.get_all()
        assert locations[0].id == 1
        assert locations[0].name == "fsn1"
        assert locations[0].description == "Falkenstein DC Park 1"
