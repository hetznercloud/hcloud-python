# pylint: disable=protected-access

from __future__ import annotations

from unittest import mock

import pytest
from dateutil.parser import isoparse

from hcloud import Client
from hcloud.zones import (
    BoundZone,
    BoundZoneRRSet,
    Zone,
    ZoneAuthoritativeNameservers,
    ZonePrimaryNameserver,
    ZoneRecord,
    ZoneRRSet,
    ZonesClient,
)

from ..conftest import BoundModelTestCase, assert_bound_action1


def assert_bound_zone1(o: BoundZone, client: ZonesClient):
    assert isinstance(o, BoundZone)
    assert o._client is client
    assert o.id == 42
    assert o.name == "example1.com"


def assert_bound_zone2(o: BoundZone, client: ZonesClient):
    assert isinstance(o, BoundZone)
    assert o._client is client
    assert o.id == 43
    assert o.name == "example2.com"


def assert_bound_zone_rrset1(o: BoundZoneRRSet, client: ZonesClient):
    assert isinstance(o, BoundZoneRRSet)
    assert o._client is client
    assert o.name == "www"
    assert o.type == "A"
    assert o.id == "www/A"


def assert_bound_zone_rrset2(o: BoundZoneRRSet, client: ZonesClient):
    assert isinstance(o, BoundZoneRRSet)
    assert o._client is client
    assert o.name == "blog"
    assert o.type == "A"
    assert o.id == "blog/A"


class TestZonesClient:
    @pytest.fixture()
    def resource_client(self, client: Client) -> ZonesClient:
        return client.zones

    def test_get_using_id(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone_response,
    ):
        request_mock.return_value = zone_response

        result = resource_client.get(42)

        request_mock.assert_called_with(
            method="GET",
            url="/zones/42",
        )

        assert_bound_zone1(result, resource_client)
        assert result.created == isoparse("2016-01-30T23:55:00+00:00")
        assert result.mode == "primary"
        assert result.ttl == 10800
        assert result.protection == {"delete": False}
        assert result.labels == {"key": "value"}
        assert result.primary_nameservers[0].address == "198.51.100.1"
        assert result.primary_nameservers[0].port == 53
        assert result.primary_nameservers[1].address == "203.0.113.1"
        assert result.primary_nameservers[1].port == 53

        assert (
            result.authoritative_nameservers.assigned[0] == "hydrogen.ns.hetzner.com."
        )
        assert (
            result.authoritative_nameservers.delegated[0] == "hydrogen.ns.hetzner.com."
        )
        assert result.authoritative_nameservers.delegation_last_check == isoparse(
            "2016-01-30T23:55:00+00:00"
        )
        assert result.authoritative_nameservers.delegation_status == "valid"

        assert result.record_count == 0
        assert result.status == "ok"
        assert result.registrar == "hetzner"

    def test_get_using_name(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone_response,
    ):
        request_mock.return_value = zone_response

        result = resource_client.get("example.com")

        request_mock.assert_called_with(
            method="GET",
            url="/zones/example.com",
        )

        assert_bound_zone1(result, resource_client)

    @pytest.mark.parametrize(
        "params",
        [
            {"mode": "primary"},
            {"label_selector": "key=value", "page": 2, "per_page": 10, "sort": "id"},
            {"name": "example.com"},
            {},
        ],
    )
    def test_get_list(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone_list_response,
        params,
    ):
        request_mock.return_value = zone_list_response

        resp = resource_client.get_list(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/zones",
            params=params,
        )

        assert resp.meta is not None

        assert len(resp.zones) == 2
        assert_bound_zone1(resp.zones[0], resource_client)
        assert_bound_zone2(resp.zones[1], resource_client)

    @pytest.mark.parametrize(
        "params",
        [
            {"label_selector": "key=value"},
            {},
        ],
    )
    def test_get_all(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone_list_response,
        params,
    ):
        request_mock.return_value = zone_list_response

        result = resource_client.get_all(**params)

        request_mock.assert_called_with(
            method="GET",
            url="/zones",
            params={**params, "page": 1, "per_page": 50},
        )

        assert len(result) == 2
        assert_bound_zone1(result[0], resource_client)
        assert_bound_zone2(result[1], resource_client)

    def test_create(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone_create_response,
    ):
        request_mock.return_value = zone_create_response

        resp = resource_client.create(
            name="example.com",
            mode="primary",
            ttl=3600,
            labels={"key": "value"},
            primary_nameservers=[
                ZonePrimaryNameserver(address="198.51.100.1", port=53),
                ZonePrimaryNameserver(address="203.0.113.1"),
            ],
            rrsets=[ZoneRRSet(name="www", type="A", records=[ZoneRecord("127.0.0.1")])],
        )

        request_mock.assert_called_with(
            url="/zones",
            method="POST",
            json={
                "name": "example.com",
                "mode": "primary",
                "ttl": 3600,
                "labels": {"key": "value"},
                "primary_nameservers": [
                    {"address": "198.51.100.1", "port": 53},
                    {"address": "203.0.113.1"},
                ],
                "rrsets": [
                    {"name": "www", "type": "A", "records": [{"value": "127.0.0.1"}]}
                ],
            },
        )

        assert_bound_zone1(resp.zone, resource_client)
        assert_bound_action1(resp.action, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_update(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        zone_response,
    ):
        request_mock.return_value = zone_response

        result = resource_client.update(zone, labels={"key": "new value"})

        request_mock.assert_called_with(
            method="PUT",
            url=f"/zones/{zone.id_or_name}",
            json={"labels": {"key": "new value"}},
        )

        assert_bound_zone1(result, resource_client)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_delete(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        action_response,
    ):
        request_mock.return_value = action_response

        resp = resource_client.delete(zone)

        request_mock.assert_called_with(
            method="DELETE",
            url=f"/zones/{zone.id_or_name}",
        )

        assert_bound_action1(resp.action, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_export_zonefile(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
    ):
        request_mock.return_value = {"zonefile": "content"}

        resp = resource_client.export_zonefile(zone)

        request_mock.assert_called_with(
            method="GET",
            url=f"/zones/{zone.id_or_name}/zonefile",
        )

        assert resp.zonefile == "content"

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_import_zonefile(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.import_zonefile(zone, "content")

        request_mock.assert_called_with(
            method="POST",
            url=f"/zones/{zone.id_or_name}/actions/import_zonefile",
            json={"zonefile": "content"},
        )

        assert_bound_action1(action, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_change_protection(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.change_protection(zone, delete=True)

        request_mock.assert_called_with(
            method="POST",
            url=f"/zones/{zone.id_or_name}/actions/change_protection",
            json={"delete": True},
        )

        assert_bound_action1(action, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_change_primary_nameservers(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.change_primary_nameservers(
            zone,
            primary_nameservers=[
                ZonePrimaryNameserver(address="198.51.100.1", port=53),
                ZonePrimaryNameserver(address="203.0.113.1"),
            ],
        )

        request_mock.assert_called_with(
            method="POST",
            url=f"/zones/{zone.id_or_name}/actions/change_primary_nameservers",
            json={
                "primary_nameservers": [
                    {"address": "198.51.100.1", "port": 53},
                    {"address": "203.0.113.1"},
                ]
            },
        )

        assert_bound_action1(action, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_change_ttl(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        action_response,
    ):
        request_mock.return_value = action_response

        action = resource_client.change_ttl(zone, 3600)

        request_mock.assert_called_with(
            method="POST",
            url=f"/zones/{zone.id_or_name}/actions/change_ttl",
            json={"ttl": 3600},
        )

        assert_bound_action1(action, resource_client._parent.actions)

    # ============ RRSETS ============

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_get_rrset(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        zone_rrset_response,
    ):
        request_mock.return_value = zone_rrset_response

        result = resource_client.get_rrset(zone, "www", "A")

        request_mock.assert_called_with(
            method="GET",
            url=f"/zones/{zone.id_or_name}/rrsets/www/A",
        )

        assert_bound_zone_rrset1(result, resource_client)
        assert result.ttl == 3600
        assert result.protection == {"change": False}
        assert result.labels == {"key": "value"}
        assert result.records[0].value == "198.51.100.1"
        assert result.records[0].comment == "web server"

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    @pytest.mark.parametrize(
        "params",
        [
            {"type": ["A"]},
            {"label_selector": "key=value", "page": 2, "per_page": 10, "sort": "id"},
            {"name": "www"},
            {},
        ],
    )
    def test_get_rrset_list(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        zone_rrset_list_response,
        params,
    ):
        request_mock.return_value = zone_rrset_list_response

        resp = resource_client.get_rrset_list(zone, **params)

        request_mock.assert_called_with(
            method="GET",
            url=f"/zones/{zone.id_or_name}/rrsets",
            params=params,
        )

        assert resp.meta is not None

        assert len(resp.rrsets) == 2
        assert_bound_zone_rrset1(resp.rrsets[0], resource_client)
        assert_bound_zone_rrset2(resp.rrsets[1], resource_client)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    @pytest.mark.parametrize(
        "params",
        [
            {"label_selector": "key=value"},
            {},
        ],
    )
    def test_get_rrset_all(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        zone_rrset_list_response,
        params,
    ):
        request_mock.return_value = zone_rrset_list_response

        result = resource_client.get_rrset_all(zone, **params)

        request_mock.assert_called_with(
            method="GET",
            url=f"/zones/{zone.id_or_name}/rrsets",
            params={**params, "page": 1, "per_page": 50},
        )

        assert len(result) == 2
        assert_bound_zone_rrset1(result[0], resource_client)
        assert_bound_zone_rrset2(result[1], resource_client)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    def test_create_rrset(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        zone_rrset_create_response,
    ):
        request_mock.return_value = zone_rrset_create_response

        resp = resource_client.create_rrset(
            zone,
            name="www",
            type="A",
            ttl=3600,
            labels={"key": "value"},
            records=[
                ZoneRecord("198.51.100.1", "web server"),
                ZoneRecord("127.0.0.1"),
            ],
        )

        request_mock.assert_called_with(
            method="POST",
            url=f"/zones/{zone.id_or_name}/rrsets",
            json={
                "name": "www",
                "type": "A",
                "ttl": 3600,
                "labels": {"key": "value"},
                "records": [
                    {"value": "198.51.100.1", "comment": "web server"},
                    {"value": "127.0.0.1"},
                ],
            },
        )

        assert_bound_zone_rrset1(resp.rrset, resource_client)
        assert_bound_action1(resp.action, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    @pytest.mark.parametrize(
        "rrset",
        [
            ZoneRRSet(name="www", type="A"),
            BoundZoneRRSet(client=mock.MagicMock(), data={"id": "www/A"}),
        ],
    )
    def test_update_rrset(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        rrset: ZoneRRSet,
        zone_rrset_response,
    ):
        rrset.zone = zone

        request_mock.return_value = zone_rrset_response

        result = resource_client.update_rrset(rrset, labels={"key": "new value"})

        request_mock.assert_called_with(
            method="PUT",
            url=f"/zones/{zone.id_or_name}/rrsets/www/A",
            json={"labels": {"key": "new value"}},
        )

        assert_bound_zone_rrset1(result, resource_client)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    @pytest.mark.parametrize(
        "rrset",
        [
            ZoneRRSet(name="www", type="A"),
            BoundZoneRRSet(client=mock.MagicMock(), data={"id": "www/A"}),
        ],
    )
    def test_delete_rrset(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        rrset: ZoneRRSet,
        action_response,
    ):
        rrset.zone = zone

        request_mock.return_value = action_response

        resp = resource_client.delete_rrset(rrset)

        request_mock.assert_called_with(
            method="DELETE",
            url=f"/zones/{zone.id_or_name}/rrsets/www/A",
        )

        assert_bound_action1(resp.action, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    @pytest.mark.parametrize(
        "rrset",
        [
            ZoneRRSet(name="www", type="A"),
            BoundZoneRRSet(client=mock.MagicMock(), data={"id": "www/A"}),
        ],
    )
    def test_change_rrset_protection(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        rrset: ZoneRRSet,
        action_response,
    ):
        rrset.zone = zone

        request_mock.return_value = action_response

        action = resource_client.change_rrset_protection(rrset, change=True)

        request_mock.assert_called_with(
            method="POST",
            url=f"/zones/{zone.id_or_name}/rrsets/{rrset.name}/{rrset.type}/actions/change_protection",
            json={"change": True},
        )

        assert_bound_action1(action, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    @pytest.mark.parametrize(
        "rrset",
        [
            ZoneRRSet(name="www", type="A"),
            BoundZoneRRSet(client=mock.MagicMock(), data={"id": "www/A"}),
        ],
    )
    def test_change_rrset_ttl(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        rrset: ZoneRRSet,
        action_response,
    ):
        rrset.zone = zone

        request_mock.return_value = action_response

        action = resource_client.change_rrset_ttl(rrset, ttl=3600)

        request_mock.assert_called_with(
            method="POST",
            url=f"/zones/{zone.id_or_name}/rrsets/{rrset.name}/{rrset.type}/actions/change_ttl",
            json={"ttl": 3600},
        )

        assert_bound_action1(action, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    @pytest.mark.parametrize(
        "rrset",
        [
            ZoneRRSet(name="www", type="A"),
            BoundZoneRRSet(client=mock.MagicMock(), data={"id": "www/A"}),
        ],
    )
    def test_add_rrset_records(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        rrset: ZoneRRSet,
        action_response,
    ):
        rrset.zone = zone

        request_mock.return_value = action_response

        action = resource_client.add_rrset_records(
            rrset,
            records=[
                ZoneRecord("198.51.100.1", "web server"),
                ZoneRecord("127.0.0.1"),
            ],
            ttl=300,
        )

        request_mock.assert_called_with(
            method="POST",
            url=f"/zones/{zone.id_or_name}/rrsets/{rrset.name}/{rrset.type}/actions/add_records",
            json={
                "records": [
                    {"value": "198.51.100.1", "comment": "web server"},
                    {"value": "127.0.0.1"},
                ],
                "ttl": 300,
            },
        )

        assert_bound_action1(action, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    @pytest.mark.parametrize(
        "rrset",
        [
            ZoneRRSet(name="www", type="A"),
            BoundZoneRRSet(client=mock.MagicMock(), data={"id": "www/A"}),
        ],
    )
    def test_remove_rrset_records(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        rrset: ZoneRRSet,
        action_response,
    ):
        rrset.zone = zone

        request_mock.return_value = action_response

        action = resource_client.remove_rrset_records(
            rrset,
            records=[
                ZoneRecord("198.51.100.1", "web server"),
                ZoneRecord("127.0.0.1"),
            ],
        )

        request_mock.assert_called_with(
            method="POST",
            url=f"/zones/{zone.id_or_name}/rrsets/{rrset.name}/{rrset.type}/actions/remove_records",
            json={
                "records": [
                    {"value": "198.51.100.1", "comment": "web server"},
                    {"value": "127.0.0.1"},
                ]
            },
        )

        assert_bound_action1(action, resource_client._parent.actions)

    @pytest.mark.parametrize(
        "zone",
        [
            Zone(name="example.com"),
            BoundZone(client=mock.MagicMock(), data={"id": 42}),
        ],
    )
    @pytest.mark.parametrize(
        "rrset",
        [
            ZoneRRSet(name="www", type="A"),
            BoundZoneRRSet(client=mock.MagicMock(), data={"id": "www/A"}),
        ],
    )
    def test_set_rrset_records(
        self,
        request_mock: mock.MagicMock,
        resource_client: ZonesClient,
        zone: Zone,
        rrset: ZoneRRSet,
        action_response,
    ):
        rrset.zone = zone

        request_mock.return_value = action_response

        action = resource_client.set_rrset_records(
            rrset,
            records=[
                ZoneRecord("198.51.100.1", "web server"),
                ZoneRecord("127.0.0.1"),
            ],
        )

        request_mock.assert_called_with(
            method="POST",
            url=f"/zones/{zone.id_or_name}/rrsets/{rrset.name}/{rrset.type}/actions/set_records",
            json={
                "records": [
                    {"value": "198.51.100.1", "comment": "web server"},
                    {"value": "127.0.0.1"},
                ]
            },
        )

        assert_bound_action1(action, resource_client._parent.actions)


class TestBoundZone(BoundModelTestCase):
    methods = [
        BoundZone.update,
        BoundZone.delete,
        BoundZone.import_zonefile,
        BoundZone.export_zonefile,
        BoundZone.change_primary_nameservers,
        BoundZone.change_ttl,
        BoundZone.change_protection,
        BoundZone.get_rrset_all,
        BoundZone.get_rrset_list,
        BoundZone.get_rrset,
        BoundZone.create_rrset,
        # With rrset sub resource
        (BoundZone.update_rrset, {"sub_resource": True}),
        (BoundZone.delete_rrset, {"sub_resource": True}),
        (BoundZone.change_rrset_protection, {"sub_resource": True}),
        (BoundZone.change_rrset_ttl, {"sub_resource": True}),
        (BoundZone.add_rrset_records, {"sub_resource": True}),
        (BoundZone.remove_rrset_records, {"sub_resource": True}),
        (BoundZone.set_rrset_records, {"sub_resource": True}),
    ]

    @pytest.fixture()
    def resource_client(self, client: Client):
        return client.zones

    @pytest.fixture()
    def bound_model(self, resource_client: ZonesClient, zone1):
        return BoundZone(resource_client, data=zone1)

    def test_init(self, resource_client: ZonesClient, bound_model: BoundZone):
        o = bound_model

        assert_bound_zone1(o, resource_client)

        assert o.id == 42
        assert o.name == "example1.com"
        assert o.created == isoparse("2016-01-30T23:55:00+00:00")
        assert o.mode == "primary"
        assert o.ttl == 10800
        assert o.protection == {"delete": False}
        assert o.labels == {"key": "value"}
        assert len(o.primary_nameservers) == 2

        assert isinstance(o.primary_nameservers[0], ZonePrimaryNameserver)
        assert o.primary_nameservers[0].address == "198.51.100.1"
        assert o.primary_nameservers[0].port == 53
        assert isinstance(o.primary_nameservers[1], ZonePrimaryNameserver)
        assert o.primary_nameservers[1].address == "203.0.113.1"
        assert o.primary_nameservers[1].port == 53

        assert isinstance(o.authoritative_nameservers, ZoneAuthoritativeNameservers)
        assert o.authoritative_nameservers.assigned == [
            "hydrogen.ns.hetzner.com.",
            "oxygen.ns.hetzner.com.",
            "helium.ns.hetzner.de.",
        ]
        assert o.authoritative_nameservers.delegated == [
            "hydrogen.ns.hetzner.com.",
            "oxygen.ns.hetzner.com.",
            "helium.ns.hetzner.de.",
        ]
        assert o.authoritative_nameservers.delegation_last_check == isoparse(
            "2016-01-30T23:55:00+00:00"
        )
        assert o.authoritative_nameservers.delegation_status == "valid"

        assert o.record_count == 0
        assert o.status == "ok"
        assert o.registrar == "hetzner"


class TestBoundZoneRRSet(BoundModelTestCase):
    methods = [
        BoundZoneRRSet.update_rrset,
        BoundZoneRRSet.delete_rrset,
        BoundZoneRRSet.change_rrset_protection,
        BoundZoneRRSet.change_rrset_ttl,
        BoundZoneRRSet.add_rrset_records,
        BoundZoneRRSet.remove_rrset_records,
        BoundZoneRRSet.set_rrset_records,
    ]

    @pytest.fixture()
    def resource_client(self, client: Client):
        return client.zones

    @pytest.fixture()
    def bound_model(self, resource_client: ZonesClient, zone_rrset1):
        return BoundZoneRRSet(resource_client, data=zone_rrset1)

    def test_init(self, resource_client: ZonesClient, bound_model: BoundZoneRRSet):
        o = bound_model

        assert_bound_zone_rrset1(o, resource_client)

        assert o.id == "www/A"
        assert o.name == "www"
        assert o.type == "A"
        assert o.ttl == 3600
        assert o.labels == {"key": "value"}
        assert o.protection == {"change": False}
        assert len(o.records) == 1

        assert isinstance(o.records[0], ZoneRecord)
        assert o.records[0].value == "198.51.100.1"
        assert o.records[0].comment == "web server"

        assert isinstance(o.zone, BoundZone)
        assert o.zone.id == 42
