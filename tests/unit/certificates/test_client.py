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

from ..conftest import BoundModelTestCase


class TestBoundCertificate(BoundModelTestCase):
    methods = [
        BoundCertificate.update,
        BoundCertificate.delete,
        BoundCertificate.retry_issuance,
    ]

    @pytest.fixture()
    def resource_client(self, client: Client):
        return client.certificates

    @pytest.fixture()
    def bound_model(self, resource_client, certificate_response):
        return BoundCertificate(
            resource_client, data=certificate_response["certificate"]
        )

    def test_init(self, bound_model: BoundCertificate):
        o = bound_model
        assert o.id == 2323
        assert o.name == "My Certificate"
        assert o.type == "managed"
        assert o.fingerprint == "03:c7:55:9b:2a:d1:04:17:09:f6:d0:7f:18:34:63:d4:3e:5f"
        assert o.certificate == "-----BEGIN CERTIFICATE-----\n..."
        assert len(o.domain_names) == 3
        assert o.domain_names[0] == "example.com"
        assert o.domain_names[1] == "webmail.example.com"
        assert o.domain_names[2] == "www.example.com"
        assert isinstance(o.status, ManagedCertificateStatus)
        assert o.status.issuance == "failed"
        assert o.status.renewal == "scheduled"
        assert o.status.error.code == "error_code"
        assert o.status.error.message == "error message"


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
