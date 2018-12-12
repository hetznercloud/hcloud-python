class TestIsosClient(object):
    def test_get_by_id(self, hetzner_client):
        iso = hetzner_client.isos.get_by_id(1)
        assert iso.id == 4711
        assert iso.name == "FreeBSD-11.0-RELEASE-amd64-dvd1"
        assert iso.description == "FreeBSD 11.0 x64"
        assert iso.type == "public"

    def test_get_all(self, hetzner_client):
        isos = hetzner_client.isos.get_all()
        assert isos[0].id == 4711
        assert isos[0].name == "FreeBSD-11.0-RELEASE-amd64-dvd1"
        assert isos[0].description == "FreeBSD 11.0 x64"
        assert isos[0].type == "public"
