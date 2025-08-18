from __future__ import annotations

from unittest import mock

import pytest

from hcloud import Client
from hcloud.certificates import (
    BoundCertificate,
    Certificate,
    CertificatesClient,
    ManagedCertificateStatus,
)


class TestBoundCertificate:
    @pytest.fixture()
    def bound_certificate(self, client: Client):
        return BoundCertificate(client.certificates, data=dict(id=14))

    def test_bound_certificate_init(self, certificate_response):
        bound_certificate = BoundCertificate(
            client=mock.MagicMock(), data=certificate_response["certificate"]
        )

        assert bound_certificate.id == 2323
        assert bound_certificate.name == "My Certificate"
        assert bound_certificate.type == "managed"
        assert (
            bound_certificate.fingerprint
            == "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f"
        )
        assert bound_certificate.certificate == "-----BEGIN CERTIFICATE-----\n..."
        assert len(bound_certificate.domain_names) == 3
        assert bound_certificate.domain_names[0] == "example.com"
        assert bound_certificate.domain_names[1] == "webmail.example.com"
        assert bound_certificate.domain_names[2] == "www.example.com"
        assert isinstance(bound_certificate.status, ManagedCertificateStatus)
        assert bound_certificate.status.issuance == "failed"
        assert bound_certificate.status.renewal == "scheduled"
        assert bound_certificate.status.error.code == "error_code"
        assert bound_certificate.status.error.message == "error message"

    def test_update(
        self,
        request_mock: mock.MagicMock,
        bound_certificate,
        response_update_certificate,
    ):
        request_mock.return_value = response_update_certificate

        certificate = bound_certificate.update(name="New name")

        request_mock.assert_called_with(
            method="PUT",
            url="/certificates/14",
            json={"name": "New name"},
        )

        assert certificate.id == 2323
        assert certificate.name == "New name"

    def test_delete(
        self,
        request_mock: mock.MagicMock,
        bound_certificate,
        action_response,
    ):
        request_mock.return_value = action_response

        delete_success = bound_certificate.delete()

        request_mock.assert_called_with(
            method="DELETE",
            url="/certificates/14",
        )

        assert delete_success is True

    def test_retry_issuance(
        self,
        request_mock: mock.MagicMock,
        bound_certificate,
        response_retry_issuance_action,
    ):
        request_mock.return_value = response_retry_issuance_action

        action = bound_certificate.retry_issuance()

        request_mock.assert_called_with(
            method="POST",
            url="/certificates/14/actions/retry",
        )

        assert action.id == 14
        assert action.command == "issue_certificate"


class TestCertificatesClient:
    @pytest.fixture()
    def certificates_client(self, client: Client):
        return CertificatesClient(client)

    def test_get_by_id(
        self,
        request_mock: mock.MagicMock,
        certificates_client: CertificatesClient,
        certificate_response,
    ):
        request_mock.return_value = certificate_response

        certificate = certificates_client.get_by_id(1)

        request_mock.assert_called_with(
            method="GET",
            url="/certificates/1",
        )
        assert certificate._client is certificates_client
        assert certificate.id == 2323
        assert certificate.name == "My Certificate"

    @pytest.mark.parametrize(
        "params",
        [
            {
                "name": "My Certificate",
                "label_selector": "k==v",
                "page": 1,
                "per_page": 10,
            },
            {"name": ""},
            {},
        ],
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        certificates_client: CertificatesClient,
        two_certificates_response,
        params,
    ):
        request_mock.return_value = two_certificates_response

        result = certificates_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/certificates",
            params=params,
        )

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
        "params", [{"name": "My Certificate", "label_selector": "label1"}, {}]
    )
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        certificates_client: CertificatesClient,
        two_certificates_response,
        params,
    ):
        request_mock.return_value = two_certificates_response

        certificates = certificates_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        request_mock.assert_called_with(
            method="GET",
            url="/certificates",
            params=params,
        )

        assert len(certificates) == 2

        certificates1 = certificates[0]
        certificates2 = certificates[1]

        assert certificates1._client is certificates_client
        assert certificates1.id == 2323
        assert certificates1.name == "My Certificate"

        assert certificates2._client is certificates_client
        assert certificates2.id == 2324
        assert certificates2.name == "My website cert"

    def test_get_by_name(
        self,
        request_mock: mock.MagicMock,
        certificates_client: CertificatesClient,
        one_certificates_response,
    ):
        request_mock.return_value = one_certificates_response

        certificates = certificates_client.get_by_name("My Certificate")

        params = {"name": "My Certificate"}

        request_mock.assert_called_with(
            method="GET",
            url="/certificates",
            params=params,
        )

        assert certificates._client is certificates_client
        assert certificates.id == 2323
        assert certificates.name == "My Certificate"

    def test_create(
        self,
        request_mock: mock.MagicMock,
        certificates_client: CertificatesClient,
        certificate_response,
    ):
        request_mock.return_value = certificate_response

        certificate = certificates_client.create(
            name="My Certificate",
            certificate="-----BEGIN CERTIFICATE-----\n...",
            private_key="-----BEGIN PRIVATE KEY-----\n...",
        )

        request_mock.assert_called_with(
            method="POST",
            url="/certificates",
            json={
                "name": "My Certificate",
                "certificate": "-----BEGIN CERTIFICATE-----\n...",
                "private_key": "-----BEGIN PRIVATE KEY-----\n...",
                "type": "uploaded",
            },
        )

        assert certificate.id == 2323
        assert certificate.name == "My Certificate"

    def test_create_managed(
        self,
        request_mock: mock.MagicMock,
        certificates_client: CertificatesClient,
        create_managed_certificate_response,
    ):
        request_mock.return_value = create_managed_certificate_response

        create_managed_certificate_rsp = certificates_client.create_managed(
            name="My Certificate", domain_names=["example.com", "*.example.org"]
        )

        request_mock.assert_called_with(
            method="POST",
            url="/certificates",
            json={
                "name": "My Certificate",
                "domain_names": ["example.com", "*.example.org"],
                "type": "managed",
            },
        )

        assert create_managed_certificate_rsp.certificate.id == 2323
        assert create_managed_certificate_rsp.certificate.name == "My Certificate"
        assert create_managed_certificate_rsp.action.id == 14
        assert create_managed_certificate_rsp.action.command == "issue_certificate"

    @pytest.mark.parametrize(
        "certificate",
        [Certificate(id=1), BoundCertificate(mock.MagicMock(), dict(id=1))],
    )
    def test_update(
        self,
        request_mock: mock.MagicMock,
        certificates_client: CertificatesClient,
        certificate,
        response_update_certificate,
    ):
        request_mock.return_value = response_update_certificate

        certificate = certificates_client.update(certificate, name="New name")

        request_mock.assert_called_with(
            method="PUT",
            url="/certificates/1",
            json={"name": "New name"},
        )

        assert certificate.id == 2323
        assert certificate.name == "New name"

    @pytest.mark.parametrize(
        "certificate",
        [Certificate(id=1), BoundCertificate(mock.MagicMock(), dict(id=1))],
    )
    def test_delete(
        self,
        request_mock: mock.MagicMock,
        certificates_client: CertificatesClient,
        certificate,
        action_response,
    ):
        request_mock.return_value = action_response

        delete_success = certificates_client.delete(certificate)

        request_mock.assert_called_with(
            method="DELETE",
            url="/certificates/1",
        )

        assert delete_success is True

    @pytest.mark.parametrize(
        "certificate",
        [Certificate(id=1), BoundCertificate(mock.MagicMock(), dict(id=1))],
    )
    def test_retry_issuance(
        self,
        request_mock: mock.MagicMock,
        certificates_client: CertificatesClient,
        certificate,
        response_retry_issuance_action,
    ):
        request_mock.return_value = response_retry_issuance_action

        action = certificates_client.retry_issuance(certificate)

        request_mock.assert_called_with(
            method="POST",
            url="/certificates/1/actions/retry",
        )

        assert action.id == 14
        assert action.command == "issue_certificate"
