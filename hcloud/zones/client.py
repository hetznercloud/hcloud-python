from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

from ..actions import ActionsPageResult, BoundAction, ResourceActionsClient
from ..core import BoundModelBase, Meta, ResourceClientBase
from .domain import (
    CreateZoneResponse,
    CreateZoneRRSetResponse,
    DeleteZoneResponse,
    DeleteZoneRRSetResponse,
    ExportZonefileResponse,
    Zone,
    ZoneAuthoritativeNameservers,
    ZoneMode,
    ZonePrimaryNameserver,
    ZoneRecord,
    ZoneRRSet,
    ZoneRRSetType,
)

if TYPE_CHECKING:
    from .._client import Client


class BoundZone(BoundModelBase, Zone):
    _client: ZonesClient

    model = Zone

    def __init__(
        self,
        client: ZonesClient,
        data: dict[str, Any],
        complete: bool = True,
    ):
        raw = data.get("primary_nameservers")
        if raw is not None:
            data["primary_nameservers"] = [
                ZonePrimaryNameserver.from_dict(o) for o in raw
            ]

        raw = data.get("authoritative_nameservers")
        if raw:
            data["authoritative_nameservers"] = ZoneAuthoritativeNameservers.from_dict(
                raw
            )

        super().__init__(client, data, complete)

    def update(
        self,
        *,
        labels: dict[str, str] | None = None,
    ) -> BoundZone:
        """
        Updates the Zone.

        See https://docs.hetzner.cloud/reference/cloud#zones-update-a-zone

        :param labels: User-defined labels (key/value pairs) for the Resource.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.update(self, labels=labels)

    def delete(self) -> DeleteZoneResponse:
        """
        Deletes the Zone.

        See https://docs.hetzner.cloud/reference/cloud#zones-delete-a-zone

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.delete(self)

    def export_zonefile(self) -> ExportZonefileResponse:
        """
        Returns a generated Zone file in BIND (RFC 1034/1035) format.

        See https://docs.hetzner.cloud/reference/cloud#zones-export-a-zone-file

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.export_zonefile(self)

    def get_actions_list(
        self,
        *,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """
        Returns all Actions for the Zone for a specific page.

        See https://docs.hetzner.cloud/reference/cloud#zones-list-zones

        :param status: Filter the actions by status. The response will only contain actions matching the specified statuses.
        :param sort: Sort resources by field and direction.
        :param page: Page number to return.
        :param per_page: Maximum number of entries returned per page.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.get_actions_list(
            self,
            status=status,
            sort=sort,
            page=page,
            per_page=per_page,
        )

    def get_actions(
        self,
        *,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """
        Returns all Actions for the Zone.

        See https://docs.hetzner.cloud/reference/cloud#zones-list-zones

        :param status: Filter the actions by status. The response will only contain actions matching the specified statuses.
        :param sort: Sort resources by field and direction.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.get_actions(
            self,
            status=status,
            sort=sort,
        )

    def import_zonefile(
        self,
        zonefile: str,
    ) -> BoundAction:
        """
        Imports a zone file, replacing all resource record sets (ZoneRRSet).

        See https://docs.hetzner.cloud/reference/cloud#zone-actions-import-a-zone-file

        :param zonefile: Zone file to import.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.import_zonefile(self, zonefile=zonefile)

    def change_protection(
        self,
        *,
        delete: bool | None = None,
    ) -> BoundAction:
        """
        Changes the protection of the Zone.

        See https://docs.hetzner.cloud/reference/cloud#zone-actions-change-a-zones-protection

        :param delete: Prevents the Zone from being deleted.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.change_protection(self, delete=delete)

    def change_ttl(
        self,
        ttl: int,
    ) -> BoundAction:
        """
        Changes the TTL of the Zone.

        See https://docs.hetzner.cloud/reference/cloud#zone-actions-change-a-zones-default-ttl

        :param ttl: Default Time To Live (TTL) of the Zone.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.change_ttl(self, ttl=ttl)

    def change_primary_nameservers(
        self,
        primary_nameservers: list[ZonePrimaryNameserver],
    ) -> BoundAction:
        """
        Changes the primary nameservers of the Zone.

        See https://docs.hetzner.cloud/reference/cloud#zone-actions-change-a-zones-primary-nameservers

        :param primary_nameservers: Primary nameservers of the Zone.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.change_primary_nameservers(
            self,
            primary_nameservers=primary_nameservers,
        )

    def get_rrset(
        self,
        name: str,
        type: ZoneRRSetType,
    ) -> BoundZoneRRSet:
        """
        Returns a single ZoneRRSet from the Zone.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrsets-get-an-rrset

        :param name: Name of the RRSet.
        :param type: Type of the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.get_rrset(self, name=name, type=type)

    def get_rrset_list(
        self,
        *,
        name: str | None = None,
        type: list[ZoneRRSetType] | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ZoneRRSetsPageResult:
        """
        Returns all ZoneRRSet in the Zone for a specific page.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrsets-list-rrsets

        :param name: Filter resources by their name. The response will only contain the resources matching exactly the specified name.
        :param type: Filter resources by their type. The response will only contain the resources matching exactly the specified type.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.
        :param page: Page number to return.
        :param per_page: Maximum number of entries returned per page.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.get_rrset_list(
            self,
            name=name,
            type=type,
            label_selector=label_selector,
            sort=sort,
            page=page,
            per_page=per_page,
        )

    def get_rrset_all(
        self,
        *,
        name: str | None = None,
        type: list[ZoneRRSetType] | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundZoneRRSet]:
        """
        Returns all ZoneRRSet in the Zone.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrsets-list-rrsets

        :param name: Filter resources by their name. The response will only contain the resources matching exactly the specified name.
        :param type: Filter resources by their type. The response will only contain the resources matching exactly the specified type.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.get_rrset_all(
            self,
            name=name,
            type=type,
            label_selector=label_selector,
            sort=sort,
        )

    def create_rrset(
        self,
        *,
        name: str,
        type: ZoneRRSetType,
        ttl: int | None = None,
        labels: dict[str, str] | None = None,
        records: list[ZoneRecord] | None = None,
    ) -> CreateZoneRRSetResponse:
        """
        Creates a ZoneRRSet in the Zone.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrsets-create-an-rrset

        :param name: Name of the RRSet.
        :param type: Type of the RRSet.
        :param ttl: Time To Live (TTL) of the RRSet.
        :param labels: User-defined labels (key/value pairs) for the Resource.
        :param records: Records of the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.create_rrset(
            self,
            name=name,
            type=type,
            ttl=ttl,
            labels=labels,
            records=records,
        )

    def update_rrset(
        self,
        rrset: ZoneRRSet | BoundZoneRRSet,
        *,
        labels: dict[str, str] | None = None,
    ) -> BoundZoneRRSet:
        """
        Updates a ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrsets-update-an-rrset

        :param rrset: RRSet to update.
        :param labels: User-defined labels (key/value pairs) for the Resource.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.update_rrset(rrset=rrset, labels=labels)

    def delete_rrset(
        self,
        rrset: ZoneRRSet | BoundZoneRRSet,
    ) -> DeleteZoneRRSetResponse:
        """
        Deletes a ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrsets-delete-an-rrset

        :param rrset: RRSet to delete.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.delete_rrset(rrset=rrset)

    def change_rrset_protection(
        self,
        rrset: ZoneRRSet | BoundZoneRRSet,
        *,
        change: bool | None = None,
    ) -> BoundAction:
        """
        Changes the protection of a ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-change-an-rrsets-protection

        :param rrset: RRSet to update.
        :param change: Prevent the Zone from being changed (deletion and updates).

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.change_rrset_protection(rrset=rrset, change=change)

    def change_rrset_ttl(
        self,
        rrset: ZoneRRSet | BoundZoneRRSet,
        ttl: int | None,
    ) -> BoundAction:
        """
        Changes the TTL of a ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-change-an-rrsets-ttl

        :param rrset: RRSet to update.
        :param change: Time To Live (TTL) of the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.change_rrset_ttl(rrset=rrset, ttl=ttl)

    def add_rrset_records(
        self,
        rrset: ZoneRRSet | BoundZoneRRSet,
        records: list[ZoneRecord],
        ttl: int | None = None,
    ) -> BoundAction:
        """
        Adds records to a ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-add-records-to-an-rrset

        :param rrset: RRSet to update.
        :param records: Records to add to the RRSet.
        :param ttl: Time To Live (TTL) of the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.add_rrset_records(rrset=rrset, records=records, ttl=ttl)

    def remove_rrset_records(
        self,
        rrset: ZoneRRSet | BoundZoneRRSet,
        records: list[ZoneRecord],
    ) -> BoundAction:
        """
        Removes records from a ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-remove-records-from-an-rrset

        :param rrset: RRSet to update.
        :param records: Records to remove from the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.remove_rrset_records(rrset=rrset, records=records)

    def set_rrset_records(
        self,
        rrset: ZoneRRSet | BoundZoneRRSet,
        records: list[ZoneRecord],
    ) -> BoundAction:
        """
        Sets the records of a ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-set-records-of-an-rrset

        :param rrset: RRSet to update.
        :param records: Records to set in the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.set_rrset_records(rrset=rrset, records=records)


class BoundZoneRRSet(BoundModelBase, ZoneRRSet):
    _client: ZonesClient

    model = ZoneRRSet

    def __init__(self, client: ZonesClient, data: dict, complete: bool = True):
        raw = data.get("zone")
        if raw is not None:
            data["zone"] = BoundZone(client, data={"id": raw}, complete=False)

        raw = data.get("records")
        if raw is not None:
            data["records"] = [ZoneRecord.from_dict(o) for o in raw]

        super().__init__(client, data, complete)

    def update_rrset(
        self,
        *,
        labels: dict[str, str] | None = None,
    ) -> BoundZoneRRSet:
        """
        Updates the ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrsets-update-an-rrset

        :param labels: User-defined labels (key/value pairs) for the Resource.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.update_rrset(self, labels=labels)

    def delete_rrset(
        self,
    ) -> DeleteZoneRRSetResponse:
        """
        Deletes the ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrsets-delete-an-rrset

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.delete_rrset(self)

    def change_rrset_protection(
        self,
        *,
        change: bool | None = None,
    ) -> BoundAction:
        """
        Changes the protection of the ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-change-an-rrsets-protection

        :param change: Prevent the Zone from being changed (deletion and updates).

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.change_rrset_protection(self, change=change)

    def change_rrset_ttl(
        self,
        ttl: int | None,
    ) -> BoundAction:
        """
        Changes the TTL of the ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-change-an-rrsets-ttl

        :param change: Time To Live (TTL) of the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.change_rrset_ttl(self, ttl=ttl)

    def add_rrset_records(
        self,
        records: list[ZoneRecord],
        ttl: int | None = None,
    ) -> BoundAction:
        """
        Adds records to the ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-add-records-to-an-rrset

        :param records: Records to add to the RRSet.
        :param ttl: Time To Live (TTL) of the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.add_rrset_records(self, records=records, ttl=ttl)

    def remove_rrset_records(
        self,
        records: list[ZoneRecord],
    ) -> BoundAction:
        """
        Removes records from the ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-remove-records-from-an-rrset

        :param records: Records to remove from the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.remove_rrset_records(self, records=records)

    def set_rrset_records(
        self,
        records: list[ZoneRecord],
    ) -> BoundAction:
        """
        Sets the records of the ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-set-records-of-an-rrset

        :param records: Records to set in the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._client.set_rrset_records(self, records=records)


class ZonesPageResult(NamedTuple):
    zones: list[BoundZone]
    meta: Meta


class ZoneRRSetsPageResult(NamedTuple):
    rrsets: list[BoundZoneRRSet]
    meta: Meta


class ZonesClient(ResourceClientBase):
    """
    ZoneClient is a client for the Zone (DNS) API.

    See https://docs.hetzner.cloud/reference/cloud#zones and https://docs.hetzner.cloud/reference/cloud#zone-rrsets.

    Experimental:
        DNS API is in beta, breaking changes may occur within minor releases.
        See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
    """

    _base_url = "/zones"

    actions: ResourceActionsClient
    """Zones scoped actions client

    :type: :class:`ResourceActionsClient <hcloud.actions.client.ResourceActionsClient>`
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.actions = ResourceActionsClient(client, self._base_url)

    def get(self, id_or_name: int | str) -> BoundZone:
        """
        Returns a single Zone.

        See https://docs.hetzner.cloud/reference/cloud#zones-get-a-zone

        :param id_or_name: ID or Name of the Zone.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        response = self._client.request(
            method="GET",
            url=f"{self._base_url}/{id_or_name}",
        )
        return BoundZone(self, response["zone"])

    def get_list(
        self,
        *,
        name: str | None = None,
        mode: ZoneMode | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ZonesPageResult:
        """
        Returns a list of Zone for a specific page.

        See https://docs.hetzner.cloud/reference/cloud#zones-list-zones

        :param name: Filter resources by their name. The response will only contain the resources matching exactly the specified name.
        :param mode: Filter resources by their mode. The response will only contain the resources matching exactly the specified mode.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.
        :param page: Page number to return.
        :param per_page: Maximum number of entries returned per page.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if mode is not None:
            params["mode"] = mode
        if label_selector is not None:
            params["label_selector"] = label_selector
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(
            method="GET",
            url=f"{self._base_url}",
            params=params,
        )
        return ZonesPageResult(
            zones=[BoundZone(self, item) for item in response["zones"]],
            meta=Meta.parse_meta(response),
        )

    def get_all(
        self,
        *,
        name: str | None = None,
        mode: ZoneMode | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundZone]:
        """
        Returns a list of all Zone.

        See https://docs.hetzner.cloud/reference/cloud#zones-list-zones

        :param name: Filter resources by their name. The response will only contain the resources matching exactly the specified name.
        :param mode: Filter resources by their mode. The response will only contain the resources matching exactly the specified mode.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._iter_pages(
            self.get_list,
            name=name,
            mode=mode,
            label_selector=label_selector,
            sort=sort,
        )

    def create(
        self,
        *,
        name: str,
        mode: ZoneMode,
        ttl: int | None = None,
        labels: dict[str, str] | None = None,
        primary_nameservers: list[ZonePrimaryNameserver] | None = None,
        rrsets: list[ZoneRRSet] | None = None,
        zonefile: str | None = None,
    ) -> CreateZoneResponse:
        """
        Creates a Zone.

        A default SOA and three NS resource records with the assigned Hetzner nameservers are created automatically.

        See https://docs.hetzner.cloud/reference/cloud#zones-create-a-zone

        :param name: Name of the Zone.
        :param mode: Mode of the Zone.
        :param ttl: Default Time To Live (TTL) of the Zone.
        :param labels: User-defined labels (key/value pairs) for the Resource.
        :param primary_nameservers: Primary nameservers of the Zone.
        :param rrsets: RRSets to be added to the Zone.
        :param zonefile: Zone file to import.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        data: dict[str, Any] = {
            "name": name,
            "mode": mode,
        }
        if ttl is not None:
            data["ttl"] = ttl
        if labels is not None:
            data["labels"] = labels
        if primary_nameservers is not None:
            data["primary_nameservers"] = [o.to_payload() for o in primary_nameservers]
        if rrsets is not None:
            data["rrsets"] = [o.to_payload() for o in rrsets]
        if zonefile is not None:
            data["zonefile"] = zonefile

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}",
            json=data,
        )

        return CreateZoneResponse(
            zone=BoundZone(self, response["zone"]),
            action=BoundAction(self._parent.actions, response["action"]),
        )

    def update(
        self,
        zone: Zone | BoundZone,
        *,
        labels: dict[str, str] | None = None,
    ) -> BoundZone:
        """
        Updates a Zone.

        See https://docs.hetzner.cloud/reference/cloud#zones-update-a-zone

        :param zone: Zone to update.
        :param labels: User-defined labels (key/value pairs) for the Resource.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        data: dict[str, Any] = {}
        if labels is not None:
            data["labels"] = labels

        response = self._client.request(
            method="PUT",
            url=f"{self._base_url}/{zone.id_or_name}",
            json=data,
        )
        return BoundZone(self, response["zone"])

    def delete(
        self,
        zone: Zone | BoundZone,
    ) -> DeleteZoneResponse:
        """
        Deletes a Zone.

        See https://docs.hetzner.cloud/reference/cloud#zones-delete-a-zone

        :param zone: Zone to delete.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        response = self._client.request(
            method="DELETE",
            url=f"{self._base_url}/{zone.id_or_name}",
        )

        return DeleteZoneResponse(
            action=BoundAction(self._parent.actions, response["action"]),
        )

    def export_zonefile(
        self,
        zone: Zone | BoundZone,
    ) -> ExportZonefileResponse:
        """
        Returns a generated Zone file in BIND (RFC 1034/1035) format.

        See https://docs.hetzner.cloud/reference/cloud#zones-export-a-zone-file

        :param zone: Zone to export the zone file from.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        response = self._client.request(
            method="GET",
            url=f"{self._base_url}/{zone.id_or_name}/zonefile",
        )
        return ExportZonefileResponse(response["zonefile"])

    def get_actions_list(
        self,
        zone: Zone | BoundZone,
        *,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """
        Returns all Actions for a Zone for a specific page.

        See https://docs.hetzner.cloud/reference/cloud#zones-list-zones

        :param zone: Zone to fetch the Actions from.
        :param status: Filter the actions by status. The response will only contain actions matching the specified statuses.
        :param sort: Sort resources by field and direction.
        :param page: Page number to return.
        :param per_page: Maximum number of entries returned per page.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        params: dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(
            method="GET",
            url=f"{self._base_url}/{zone.id_or_name}/actions",
            params=params,
        )
        return ActionsPageResult(
            actions=[BoundAction(self._parent.actions, o) for o in response["actions"]],
            meta=Meta.parse_meta(response),
        )

    def get_actions(
        self,
        zone: Zone | BoundZone,
        *,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """
        Returns all Actions for a Zone.

        See https://docs.hetzner.cloud/reference/cloud#zones-list-zones

        :param zone: Zone to fetch the Actions from.
        :param status: Filter the actions by status. The response will only contain actions matching the specified statuses.
        :param sort: Sort resources by field and direction.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._iter_pages(
            self.get_actions_list,
            zone,
            status=status,
            sort=sort,
        )

    def import_zonefile(
        self,
        zone: Zone | BoundZone,
        zonefile: str,
    ) -> BoundAction:
        """
        Imports a zone file, replacing all resource record sets (ZoneRRSet).

        See https://docs.hetzner.cloud/reference/cloud#zone-actions-import-a-zone-file

        :param zone: Zone to import the zone file into.
        :param zonefile: Zone file to import.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        data: dict[str, Any] = {
            "zonefile": zonefile,
        }

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{zone.id_or_name}/actions/import_zonefile",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def change_protection(
        self,
        zone: Zone | BoundZone,
        *,
        delete: bool | None = None,
    ) -> BoundAction:
        """
        Changes the protection of a Zone.

        See https://docs.hetzner.cloud/reference/cloud#zone-actions-change-a-zones-protection

        :param zone: Zone to update.
        :param delete: Prevents the Zone from being deleted.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        data: dict[str, Any] = {}
        if delete is not None:
            data["delete"] = delete

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{zone.id_or_name}/actions/change_protection",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def change_ttl(
        self,
        zone: Zone | BoundZone,
        ttl: int,
    ) -> BoundAction:
        """
        Changes the TTL of a Zone.

        See https://docs.hetzner.cloud/reference/cloud#zone-actions-change-a-zones-default-ttl

        :param zone: Zone to update.
        :param ttl: Default Time To Live (TTL) of the Zone.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        data: dict[str, Any] = {
            "ttl": ttl,
        }

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{zone.id_or_name}/actions/change_ttl",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def change_primary_nameservers(
        self,
        zone: Zone | BoundZone,
        primary_nameservers: list[ZonePrimaryNameserver],
    ) -> BoundAction:
        """
        Changes the primary nameservers of a Zone.

        See https://docs.hetzner.cloud/reference/cloud#zone-actions-change-a-zones-primary-nameservers

        :param zone: Zone to update.
        :param primary_nameservers: Primary nameservers of the Zone.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        data: dict[str, Any] = {
            "primary_nameservers": [o.to_payload() for o in primary_nameservers],
        }

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{zone.id_or_name}/actions/change_primary_nameservers",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def get_rrset(
        self,
        zone: Zone | BoundZone,
        name: str,
        type: ZoneRRSetType,
    ) -> BoundZoneRRSet:
        """
        Returns a single ZoneRRSet from the Zone.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrsets-get-an-rrset

        :param zone: Zone to fetch the RRSet from.
        :param name: Name of the RRSet.
        :param type: Type of the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        response = self._client.request(
            method="GET",
            url=f"{self._base_url}/{zone.id_or_name}/rrsets/{name}/{type}",
        )
        return BoundZoneRRSet(self, response["rrset"])

    def get_rrset_list(
        self,
        zone: Zone | BoundZone,
        *,
        name: str | None = None,
        type: list[ZoneRRSetType] | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ZoneRRSetsPageResult:
        """
        Returns all ZoneRRSet in the Zone for a specific page.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrsets-list-rrsets

        :param zone: Zone to fetch the RRSets from.
        :param name: Filter resources by their name. The response will only contain the resources matching exactly the specified name.
        :param type: Filter resources by their type. The response will only contain the resources matching exactly the specified type.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.
        :param page: Page number to return.
        :param per_page: Maximum number of entries returned per page.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if type is not None:
            params["type"] = type
        if label_selector is not None:
            params["label_selector"] = label_selector
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(
            method="GET",
            url=f"{self._base_url}/{zone.id_or_name}/rrsets",
            params=params,
        )
        return ZoneRRSetsPageResult(
            rrsets=[BoundZoneRRSet(self, item) for item in response["rrsets"]],
            meta=Meta.parse_meta(response),
        )

    def get_rrset_all(
        self,
        zone: Zone | BoundZone,
        *,
        name: str | None = None,
        type: list[ZoneRRSetType] | None = None,
        label_selector: str | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundZoneRRSet]:
        """
        Returns all ZoneRRSet in the Zone.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrsets-list-rrsets

        :param zone: Zone to fetch the RRSets from.
        :param name: Filter resources by their name. The response will only contain the resources matching exactly the specified name.
        :param type: Filter resources by their type. The response will only contain the resources matching exactly the specified type.
        :param label_selector: Filter resources by labels. The response will only contain resources matching the label selector.
        :param sort: Sort resources by field and direction.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        return self._iter_pages(
            self.get_rrset_list,
            zone,
            name=name,
            type=type,
            label_selector=label_selector,
            sort=sort,
        )

    def create_rrset(
        self,
        zone: Zone | BoundZone,
        *,
        name: str,
        type: ZoneRRSetType,
        ttl: int | None = None,
        labels: dict[str, str] | None = None,
        records: list[ZoneRecord] | None = None,
    ) -> CreateZoneRRSetResponse:
        """
        Creates a ZoneRRSet in the Zone.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrsets-create-an-rrset

        :param zone: Zone to create the RRSets in.
        :param name: Name of the RRSet.
        :param type: Type of the RRSet.
        :param ttl: Time To Live (TTL) of the RRSet.
        :param labels: User-defined labels (key/value pairs) for the Resource.
        :param records: Records of the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        data: dict[str, Any] = {
            "name": name,
            "type": type,
        }
        if ttl is not None:
            data["ttl"] = ttl
        if labels is not None:
            data["labels"] = labels
        if records is not None:
            data["records"] = [o.to_payload() for o in records]

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{zone.id_or_name}/rrsets",
            json=data,
        )
        return CreateZoneRRSetResponse(
            rrset=BoundZoneRRSet(self, response["rrset"]),
            action=BoundAction(self._parent.actions, response["action"]),
        )

    def update_rrset(
        self,
        rrset: ZoneRRSet | BoundZoneRRSet,
        *,
        labels: dict[str, str] | None = None,
    ) -> BoundZoneRRSet:
        """
        Updates a ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrsets-update-an-rrset

        :param rrset: RRSet to update.
        :param labels: User-defined labels (key/value pairs) for the Resource.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        if rrset.zone is None:
            raise ValueError("rrset zone property is none")

        data: dict[str, Any] = {}
        if labels is not None:
            data["labels"] = labels

        response = self._client.request(
            method="PUT",
            url=f"{self._base_url}/{rrset.zone.id_or_name}/rrsets/{rrset.name}/{rrset.type}",
            json=data,
        )
        return BoundZoneRRSet(self, response["rrset"])

    def delete_rrset(
        self,
        rrset: ZoneRRSet | BoundZoneRRSet,
    ) -> DeleteZoneRRSetResponse:
        """
        Deletes a ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrsets-delete-an-rrset

        :param rrset: RRSet to delete.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        if rrset.zone is None:
            raise ValueError("rrset zone property is none")

        response = self._client.request(
            method="DELETE",
            url=f"{self._base_url}/{rrset.zone.id_or_name}/rrsets/{rrset.name}/{rrset.type}",
        )
        return DeleteZoneRRSetResponse(
            action=BoundAction(self._parent.actions, response["action"]),
        )

    def change_rrset_protection(
        self,
        rrset: ZoneRRSet | BoundZoneRRSet,
        *,
        change: bool | None = None,
    ) -> BoundAction:
        """
        Changes the protection of a ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-change-an-rrsets-protection

        :param rrset: RRSet to update.
        :param change: Prevent the Zone from being changed (deletion and updates).

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        if rrset.zone is None:
            raise ValueError("rrset zone property is none")

        data: dict[str, Any] = {}
        if change is not None:
            data["change"] = change

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{rrset.zone.id_or_name}/rrsets/{rrset.name}/{rrset.type}/actions/change_protection",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def change_rrset_ttl(
        self,
        rrset: ZoneRRSet | BoundZoneRRSet,
        ttl: int | None,
    ) -> BoundAction:
        """
        Changes the TTL of a ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-change-an-rrsets-ttl

        :param rrset: RRSet to update.
        :param change: Time To Live (TTL) of the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        if rrset.zone is None:
            raise ValueError("rrset zone property is none")

        data: dict[str, Any] = {
            "ttl": ttl,
        }

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{rrset.zone.id_or_name}/rrsets/{rrset.name}/{rrset.type}/actions/change_ttl",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def add_rrset_records(
        self,
        rrset: ZoneRRSet | BoundZoneRRSet,
        records: list[ZoneRecord],
        ttl: int | None = None,
    ) -> BoundAction:
        """
        Adds records to a ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-add-records-to-an-rrset

        :param rrset: RRSet to update.
        :param records: Records to add to the RRSet.
        :param ttl: Time To Live (TTL) of the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        if rrset.zone is None:
            raise ValueError("rrset zone property is none")

        data: dict[str, Any] = {
            "records": [o.to_payload() for o in records],
        }
        if ttl is not None:
            data["ttl"] = ttl

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{rrset.zone.id_or_name}/rrsets/{rrset.name}/{rrset.type}/actions/add_records",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def remove_rrset_records(
        self,
        rrset: ZoneRRSet | BoundZoneRRSet,
        records: list[ZoneRecord],
    ) -> BoundAction:
        """
        Removes records from a ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-remove-records-from-an-rrset

        :param rrset: RRSet to update.
        :param records: Records to remove from the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        if rrset.zone is None:
            raise ValueError("rrset zone property is none")

        data: dict[str, Any] = {
            "records": [o.to_payload() for o in records],
        }

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{rrset.zone.id_or_name}/rrsets/{rrset.name}/{rrset.type}/actions/remove_records",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])

    def set_rrset_records(
        self,
        rrset: ZoneRRSet | BoundZoneRRSet,
        records: list[ZoneRecord],
    ) -> BoundAction:
        """
        Sets the records of a ZoneRRSet.

        See https://docs.hetzner.cloud/reference/cloud#zone-rrset-actions-set-records-of-an-rrset

        :param rrset: RRSet to update.
        :param records: Records to set in the RRSet.

        Experimental:
            DNS API is in beta, breaking changes may occur within minor releases.
            See https://docs.hetzner.cloud/changelog#2025-10-07-dns-beta for more details.
        """
        if rrset.zone is None:
            raise ValueError("rrset zone property is none")

        data: dict[str, Any] = {
            "records": [o.to_payload() for o in records],
        }

        response = self._client.request(
            method="POST",
            url=f"{self._base_url}/{rrset.zone.id_or_name}/rrsets/{rrset.name}/{rrset.type}/actions/set_records",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])
