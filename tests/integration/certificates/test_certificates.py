import mock
import pytest

from hcloud.certificates.client import BoundCertificate
from hcloud.certificates.domain import Certificate


class TestBoundCertificate(object):
    @pytest.fixture()
    def bound_certificate(self, hetzner_client):
        return BoundCertificate(client=hetzner_client.certificates, data=dict(id=897))

    def test_update(self, bound_certificate):
        certificate = bound_certificate.update(name="new-name")

        assert certificate.id == 897
        assert certificate.name == "new-name"

    def test_delete(self, bound_certificate):
        delete_success = bound_certificate.delete()

        assert delete_success is True


class TestCertificatesClient(object):
    def test_get_by_id(self, hetzner_client):
        certificate = hetzner_client.certificates.get_by_id(1)
        assert certificate.id == 897
        assert certificate.name == "my website cert"
        assert certificate.fingerprint == "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f"
        assert certificate.certificate == "-----BEGIN CERTIFICATE-----\n..."
        assert len(certificate.domain_names) == 3
        assert certificate.domain_names[0] == "example.com"
        assert certificate.domain_names[1] == "webmail.example.com"
        assert certificate.domain_names[2] == "www.example.com"

    def test_get_by_name(self, hetzner_client):
        certificate = hetzner_client.certificates.get_by_name("my website cert")
        assert certificate.id == 897
        assert certificate.name == "my website cert"
        assert certificate.fingerprint == "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f"
        assert certificate.certificate == "-----BEGIN CERTIFICATE-----\n..."
        assert len(certificate.domain_names) == 3
        assert certificate.domain_names[0] == "example.com"
        assert certificate.domain_names[1] == "webmail.example.com"
        assert certificate.domain_names[2] == "www.example.com"

    def test_get_list(self, hetzner_client):
        certificates = hetzner_client.certificates.get_all()
        assert certificates[0].id == 897
        assert certificates[0].name == "my website cert"
        assert certificates[0].fingerprint == "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f"
        assert certificates[0].certificate == "-----BEGIN CERTIFICATE-----\n..."
        assert len(certificates[0].domain_names) == 3
        assert certificates[0].domain_names[0] == "example.com"
        assert certificates[0].domain_names[1] == "webmail.example.com"
        assert certificates[0].domain_names[2] == "www.example.com"

    def test_create(self, hetzner_client):
        certificate = hetzner_client.certificates.create(name="my website cert", certificate="-----BEGIN CERTIFICATE-----\n...", private_key="-----BEGIN PRIVATE KEY-----\n...")

        assert certificate.id == 897
        assert certificate.name == "my website cert"

    @pytest.mark.parametrize("certificate", [Certificate(id=1), BoundCertificate(mock.MagicMock(), dict(id=1))])
    def test_update(self, hetzner_client, certificate):
        certificate = hetzner_client.certificates.update(certificate, name="new-name")

        assert certificate.id == 897
        assert certificate.name == "new-name"

    @pytest.mark.parametrize("certificate", [Certificate(id=1), BoundCertificate(mock.MagicMock(), dict(id=1))])
    def test_delete(self, hetzner_client, certificate):
        delete_success = hetzner_client.certificates.delete(certificate)

        assert delete_success is True
