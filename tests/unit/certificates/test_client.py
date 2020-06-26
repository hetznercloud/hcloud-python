import pytest
import mock

from hcloud.certificates.client import CertificatesClient, BoundCertificate
from hcloud.certificates.domain import Certificate


class TestBoundCertificate(object):

    @pytest.fixture()
    def bound_certificate(self, hetzner_client):
        return BoundCertificate(client=hetzner_client.certificates, data=dict(id=14))

    def test_bound_certificate_init(self, certificate_response):
        bound_certificate = BoundCertificate(
            client=mock.MagicMock(),
            data=certificate_response['certificate']
        )

        assert bound_certificate.id == 2323
        assert bound_certificate.name == "My Certificate"
        assert bound_certificate.fingerprint == "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f"
        assert bound_certificate.certificate == "-----BEGIN CERTIFICATE-----\n..."
        assert len(bound_certificate.domain_names) == 3
        assert bound_certificate.domain_names[0] == "example.com"
        assert bound_certificate.domain_names[1] == "webmail.example.com"
        assert bound_certificate.domain_names[2] == "www.example.com"

    def test_update(self, hetzner_client, bound_certificate, response_update_certificate):
        hetzner_client.request.return_value = response_update_certificate
        certificate = bound_certificate.update(name="New name")
        hetzner_client.request.assert_called_with(url="/certificates/14", method="PUT", json={"name": "New name"})

        assert certificate.id == 2323
        assert certificate.name == "New name"

    def test_delete(self, hetzner_client, bound_certificate, generic_action):
        hetzner_client.request.return_value = generic_action
        delete_success = bound_certificate.delete()
        hetzner_client.request.assert_called_with(url="/certificates/14", method="DELETE")

        assert delete_success is True


class TestCertificatesClient(object):

    @pytest.fixture()
    def certificates_client(self):
        return CertificatesClient(client=mock.MagicMock())

    def test_get_by_id(self, certificates_client, certificate_response):
        certificates_client._client.request.return_value = certificate_response
        certificate = certificates_client.get_by_id(1)
        certificates_client._client.request.assert_called_with(url="/certificates/1", method="GET")
        assert certificate._client is certificates_client
        assert certificate.id == 2323
        assert certificate.name == "My Certificate"

    @pytest.mark.parametrize(
        "params",
        [
            {'name': "My Certificate", "label_selector": "k==v", 'page': 1, 'per_page': 10},
            {'name': ""},
            {}
        ]
    )
    def test_get_list(self, certificates_client, two_certificates_response, params):
        certificates_client._client.request.return_value = two_certificates_response
        result = certificates_client.get_list(**params)
        certificates_client._client.request.assert_called_with(url="/certificates", method="GET", params=params)

        certificates = result.certificates
        assert len(certificates) == 2

        certificates1 = certificates[0]
        certificates2 = certificates[1]

        assert certificates1._client is certificates_client
        assert certificates1.id == 2323
        assert certificates1.name == "My Certificate"

        assert certificates2._client is certificates_client
        assert certificates2.id == 2324
        assert certificates2.name == "My website cert"

    @pytest.mark.parametrize(
        "params",
        [
            {'name': "My Certificate", 'label_selector': "label1"},
            {}
        ]
    )
    def test_get_all(self, certificates_client, two_certificates_response, params):
        certificates_client._client.request.return_value = two_certificates_response
        certificates = certificates_client.get_all(**params)

        params.update({'page': 1, 'per_page': 50})
        certificates_client._client.request.assert_called_with(url="/certificates", method="GET", params=params)

        assert len(certificates) == 2

        certificates1 = certificates[0]
        certificates2 = certificates[1]

        assert certificates1._client is certificates_client
        assert certificates1.id == 2323
        assert certificates1.name == "My Certificate"

        assert certificates2._client is certificates_client
        assert certificates2.id == 2324
        assert certificates2.name == "My website cert"

    def test_get_by_name(self, certificates_client, one_certificates_response):
        certificates_client._client.request.return_value = one_certificates_response
        certificates = certificates_client.get_by_name("My Certificate")

        params = {'name': "My Certificate"}
        certificates_client._client.request.assert_called_with(url="/certificates", method="GET", params=params)

        assert certificates._client is certificates_client
        assert certificates.id == 2323
        assert certificates.name == "My Certificate"

    def test_create(self, certificates_client, certificate_response):
        certificates_client._client.request.return_value = certificate_response
        certificate = certificates_client.create(name="My Certificate", certificate="-----BEGIN CERTIFICATE-----\n...", private_key="-----BEGIN PRIVATE KEY-----\n...")
        certificates_client._client.request.assert_called_with(url="/certificates", method="POST", json={"name": "My Certificate", "certificate": "-----BEGIN CERTIFICATE-----\n...", "private_key": "-----BEGIN PRIVATE KEY-----\n..."})

        assert certificate.id == 2323
        assert certificate.name == "My Certificate"

    @pytest.mark.parametrize("certificate", [Certificate(id=1), BoundCertificate(mock.MagicMock(), dict(id=1))])
    def test_update(self, certificates_client, certificate, response_update_certificate):
        certificates_client._client.request.return_value = response_update_certificate
        certificate = certificates_client.update(certificate, name="New name")
        certificates_client._client.request.assert_called_with(url="/certificates/1", method="PUT", json={"name": "New name"})

        assert certificate.id == 2323
        assert certificate.name == "New name"

    @pytest.mark.parametrize("certificate", [Certificate(id=1), BoundCertificate(mock.MagicMock(), dict(id=1))])
    def test_delete(self, certificates_client, certificate, generic_action):
        certificates_client._client.request.return_value = generic_action
        delete_success = certificates_client.delete(certificate)
        certificates_client._client.request.assert_called_with(url="/certificates/1", method="DELETE")

        assert delete_success is True
