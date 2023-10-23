from __future__ import annotations

import datetime
from datetime import timezone
from unittest import mock

import pytest

from hcloud.isos import BoundIso, IsosClient


class TestBoundIso:
    @pytest.fixture()
    def bound_iso(self, hetzner_client):
        return BoundIso(client=hetzner_client.isos, data=dict(id=14))

    def test_bound_iso_init(self, iso_response):
        bound_iso = BoundIso(client=mock.MagicMock(), data=iso_response["iso"])

        assert bound_iso.id == 4711
        assert bound_iso.name == "FreeBSD-11.0-RELEASE-amd64-dvd1"
        assert bound_iso.description == "FreeBSD 11.0 x64"
        assert bound_iso.type == "public"
        assert bound_iso.architecture == "x86"
        with pytest.deprecated_call():
            assert bound_iso.deprecated == datetime.datetime(
                2018, 2, 28, 0, 0, tzinfo=timezone.utc
            )
        assert bound_iso.deprecation.announced == datetime.datetime(
            2018, 1, 28, 0, 0, tzinfo=timezone.utc
        )
        assert bound_iso.deprecation.unavailable_after == datetime.datetime(
            2018, 2, 28, 0, 0, tzinfo=timezone.utc
        )


class TestIsosClient:
    @pytest.fixture()
    def isos_client(self):
        return IsosClient(client=mock.MagicMock())

    def test_get_by_id(self, isos_client, iso_response):
        isos_client._client.request.return_value = iso_response
        iso = isos_client.get_by_id(1)
        isos_client._client.request.assert_called_with(url="/isos/1", method="GET")
        assert iso._client is isos_client
        assert iso.id == 4711
        assert iso.name == "FreeBSD-11.0-RELEASE-amd64-dvd1"

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"name": ""},
            {"name": "FreeBSD-11.0-RELEASE-amd64-dvd1", "page": 1, "per_page": 2},
        ],
    )
    def test_get_list(self, isos_client, two_isos_response, params):
        isos_client._client.request.return_value = two_isos_response
        result = isos_client.get_list(**params)
        isos_client._client.request.assert_called_with(
            url="/isos", method="GET", params=params
        )

        isos = result.isos
        assert result.meta is None

        assert len(isos) == 2

        isos1 = isos[0]
        isos2 = isos[1]

        assert isos1._client is isos_client
        assert isos1.id == 4711
        assert isos1.name == "FreeBSD-11.0-RELEASE-amd64-dvd1"

        assert isos2._client is isos_client
        assert isos2.id == 4712
        assert isos2.name == "FreeBSD-11.0-RELEASE-amd64-dvd1"

    @pytest.mark.parametrize(
        "params", [{}, {"name": "FreeBSD-11.0-RELEASE-amd64-dvd1"}]
    )
    def test_get_all(self, isos_client, two_isos_response, params):
        isos_client._client.request.return_value = two_isos_response
        isos = isos_client.get_all(**params)

        params.update({"page": 1, "per_page": 50})

        isos_client._client.request.assert_called_with(
            url="/isos", method="GET", params=params
        )

        assert len(isos) == 2

        isos1 = isos[0]
        isos2 = isos[1]

        assert isos1._client is isos_client
        assert isos1.id == 4711
        assert isos1.name == "FreeBSD-11.0-RELEASE-amd64-dvd1"

        assert isos2._client is isos_client
        assert isos2.id == 4712
        assert isos2.name == "FreeBSD-11.0-RELEASE-amd64-dvd1"

    def test_get_by_name(self, isos_client, one_isos_response):
        isos_client._client.request.return_value = one_isos_response
        iso = isos_client.get_by_name("FreeBSD-11.0-RELEASE-amd64-dvd1")

        params = {"name": "FreeBSD-11.0-RELEASE-amd64-dvd1"}

        isos_client._client.request.assert_called_with(
            url="/isos", method="GET", params=params
        )

        assert iso._client is isos_client
        assert iso.id == 4711
        assert iso.name == "FreeBSD-11.0-RELEASE-amd64-dvd1"
