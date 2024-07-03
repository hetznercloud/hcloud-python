from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, NamedTuple

from dateutil.parser import isoparse

from ..actions import ActionsPageResult, BoundAction, ResourceActionsClient
from ..core import BoundModelBase, ClientEntityBase, Meta
from ..datacenters import BoundDatacenter
from ..firewalls import BoundFirewall
from ..floating_ips import BoundFloatingIP
from ..images import BoundImage, CreateImageResponse
from ..isos import BoundIso
from ..metrics import Metrics
from ..placement_groups import BoundPlacementGroup
from ..primary_ips import BoundPrimaryIP
from ..server_types import BoundServerType
from ..volumes import BoundVolume
from .domain import (
    CreateServerResponse,
    EnableRescueResponse,
    GetMetricsResponse,
    IPv4Address,
    IPv6Network,
    MetricsType,
    PrivateNet,
    PublicNetwork,
    PublicNetworkFirewall,
    RebuildResponse,
    RequestConsoleResponse,
    ResetPasswordResponse,
    Server,
)

if TYPE_CHECKING:
    from .._client import Client
    from ..datacenters import Datacenter
    from ..firewalls import Firewall
    from ..images import Image
    from ..isos import Iso
    from ..locations import BoundLocation, Location
    from ..networks import BoundNetwork, Network
    from ..placement_groups import PlacementGroup
    from ..server_types import ServerType
    from ..ssh_keys import BoundSSHKey, SSHKey
    from ..volumes import Volume
    from .domain import ServerCreatePublicNetwork


class BoundServer(BoundModelBase, Server):
    _client: ServersClient

    model = Server

    # pylint: disable=too-many-locals
    def __init__(self, client: ServersClient, data: dict, complete: bool = True):
        datacenter = data.get("datacenter")
        if datacenter is not None:
            data["datacenter"] = BoundDatacenter(client._client.datacenters, datacenter)

        volumes = data.get("volumes", [])
        if volumes:
            volumes = [
                BoundVolume(client._client.volumes, {"id": volume}, complete=False)
                for volume in volumes
            ]
            data["volumes"] = volumes

        image = data.get("image", None)
        if image is not None:
            data["image"] = BoundImage(client._client.images, image)

        iso = data.get("iso", None)
        if iso is not None:
            data["iso"] = BoundIso(client._client.isos, iso)

        server_type = data.get("server_type")
        if server_type is not None:
            data["server_type"] = BoundServerType(
                client._client.server_types, server_type
            )

        public_net = data.get("public_net")
        if public_net:
            ipv4_address = (
                IPv4Address.from_dict(public_net["ipv4"])
                if public_net["ipv4"] is not None
                else None
            )
            ipv4_primary_ip = (
                BoundPrimaryIP(
                    client._client.primary_ips,
                    {"id": public_net["ipv4"]["id"]},
                    complete=False,
                )
                if public_net["ipv4"] is not None
                else None
            )
            ipv6_network = (
                IPv6Network.from_dict(public_net["ipv6"])
                if public_net["ipv6"] is not None
                else None
            )
            ipv6_primary_ip = (
                BoundPrimaryIP(
                    client._client.primary_ips,
                    {"id": public_net["ipv6"]["id"]},
                    complete=False,
                )
                if public_net["ipv6"] is not None
                else None
            )
            floating_ips = [
                BoundFloatingIP(
                    client._client.floating_ips, {"id": floating_ip}, complete=False
                )
                for floating_ip in public_net["floating_ips"]
            ]
            firewalls = [
                PublicNetworkFirewall(
                    BoundFirewall(
                        client._client.firewalls, {"id": firewall["id"]}, complete=False
                    ),
                    status=firewall["status"],
                )
                for firewall in public_net.get("firewalls", [])
            ]
            data["public_net"] = PublicNetwork(
                ipv4=ipv4_address,
                ipv6=ipv6_network,
                primary_ipv4=ipv4_primary_ip,
                primary_ipv6=ipv6_primary_ip,
                floating_ips=floating_ips,
                firewalls=firewalls,
            )

        private_nets = data.get("private_net")
        if private_nets:
            # pylint: disable=import-outside-toplevel
            from ..networks import BoundNetwork

            private_nets = [
                PrivateNet(
                    network=BoundNetwork(
                        client._client.networks,
                        {"id": private_net["network"]},
                        complete=False,
                    ),
                    ip=private_net["ip"],
                    alias_ips=private_net["alias_ips"],
                    mac_address=private_net["mac_address"],
                )
                for private_net in private_nets
            ]
            data["private_net"] = private_nets

        placement_group = data.get("placement_group")
        if placement_group:
            placement_group = BoundPlacementGroup(
                client._client.placement_groups, placement_group
            )
            data["placement_group"] = placement_group

        super().__init__(client, data, complete)

    def get_actions_list(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """Returns all action objects for a server.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundAction <hcloud.actions.client.BoundAction>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        return self._client.get_actions_list(self, status, sort, page, per_page)

    def get_actions(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """Returns all action objects for a server.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.get_actions(self, status, sort)

    def update(
        self,
        name: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundServer:
        """Updates a server. You can update a server’s name and a server’s labels.

        :param name: str (optional)
               New name to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundServer <hcloud.servers.client.BoundServer>`
        """
        return self._client.update(self, name, labels)

    def get_metrics(
        self,
        type: MetricsType | list[MetricsType],
        start: datetime | str,
        end: datetime | str,
        step: float | None = None,
    ) -> GetMetricsResponse:
        """Get Metrics for a Server.

        :param server: The Server to get the metrics for.
        :param type: Type of metrics to get.
        :param start: Start of period to get Metrics for (in ISO-8601 format).
        :param end: End of period to get Metrics for (in ISO-8601 format).
        :param step: Resolution of results in seconds.
        """
        return self._client.get_metrics(
            self,
            type=type,
            start=start,
            end=end,
            step=step,
        )

    def delete(self) -> BoundAction:
        """Deletes a server. This immediately removes the server from your account, and it is no longer accessible.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.delete(self)

    def power_off(self) -> BoundAction:
        """Cuts power to the server. This forcefully stops it without giving the server operating system time to gracefully stop

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.power_off(self)

    def power_on(self) -> BoundAction:
        """Starts a server by turning its power on.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.power_on(self)

    def reboot(self) -> BoundAction:
        """Reboots a server gracefully by sending an ACPI request.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.reboot(self)

    def reset(self) -> BoundAction:
        """Cuts power to a server and starts it again.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.reset(self)

    def shutdown(self) -> BoundAction:
        """Shuts down a server gracefully by sending an ACPI shutdown request.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.shutdown(self)

    def reset_password(self) -> ResetPasswordResponse:
        """Resets the root password. Only works for Linux systems that are running the qemu guest agent.

        :return: :class:`ResetPasswordResponse <hcloud.servers.domain.ResetPasswordResponse>`
        """
        return self._client.reset_password(self)

    def enable_rescue(
        self,
        type: str | None = None,
        ssh_keys: list[str] | None = None,
    ) -> EnableRescueResponse:
        """Enable the Hetzner Rescue System for this server.

        :param type: str
                Type of rescue system to boot (default: linux64)
                Choices: linux64, linux32, freebsd64
        :param ssh_keys: List[str]
                Array of SSH key IDs which should be injected into the rescue system. Only available for types: linux64 and linux32.
        :return: :class:`EnableRescueResponse <hcloud.servers.domain.EnableRescueResponse>`
        """
        return self._client.enable_rescue(self, type=type, ssh_keys=ssh_keys)

    def disable_rescue(self) -> BoundAction:
        """Disables the Hetzner Rescue System for a server.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.disable_rescue(self)

    def create_image(
        self,
        description: str | None = None,
        type: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> CreateImageResponse:
        """Creates an image (snapshot) from a server by copying the contents of its disks.

        :param description: str (optional)
               Description of the image. If you do not set this we auto-generate one for you.
        :param type: str (optional)
               Type of image to create (default: snapshot)
               Choices: snapshot, backup
        :param labels: Dict[str, str]
               User-defined labels (key-value pairs)
        :return:  :class:`CreateImageResponse <hcloud.images.domain.CreateImageResponse>`
        """
        return self._client.create_image(self, description, type, labels)

    def rebuild(
        self,
        image: Image | BoundImage,
        # pylint: disable=unused-argument
        **kwargs: Any,
    ) -> RebuildResponse:
        """Rebuilds a server overwriting its disk with the content of an image, thereby destroying all data on the target server.

        :param image: Image to use for the rebuilt server
        """
        return self._client.rebuild(self, image)

    def change_type(
        self,
        server_type: ServerType | BoundServerType,
        upgrade_disk: bool,
    ) -> BoundAction:
        """Changes the type (Cores, RAM and disk sizes) of a server.

        :param server_type: :class:`BoundServerType <hcloud.server_types.client.BoundServerType>` or :class:`ServerType <hcloud.server_types.domain.ServerType>`
               Server type the server should migrate to
        :param upgrade_disk: boolean
               If false, do not upgrade the disk. This allows downgrading the server type later.
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_type(self, server_type, upgrade_disk)

    def enable_backup(self) -> BoundAction:
        """Enables and configures the automatic daily backup option for the server. Enabling automatic backups will increase the price of the server by 20%.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.enable_backup(self)

    def disable_backup(self) -> BoundAction:
        """Disables the automatic backup option and deletes all existing Backups for a Server.

        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.disable_backup(self)

    def attach_iso(self, iso: Iso | BoundIso) -> BoundAction:
        """Attaches an ISO to a server.

        :param iso: :class:`BoundIso <hcloud.isos.client.BoundIso>` or :class:`Server <hcloud.isos.domain.Iso>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.attach_iso(self, iso)

    def detach_iso(self) -> BoundAction:
        """Detaches an ISO from a server.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.detach_iso(self)

    def change_dns_ptr(self, ip: str, dns_ptr: str | None) -> BoundAction:
        """Changes the hostname that will appear when getting the hostname belonging to the primary IPs (ipv4 and ipv6) of this server.

        :param ip: str
                   The IP address for which to set the reverse DNS entry
        :param dns_ptr:
                  Hostname to set as a reverse DNS PTR entry, will reset to original default value if `None`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_dns_ptr(self, ip, dns_ptr)

    def change_protection(
        self,
        delete: bool | None = None,
        rebuild: bool | None = None,
    ) -> BoundAction:
        """Changes the protection configuration of the server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param delete: boolean
                     If true, prevents the server from being deleted (currently delete and rebuild attribute needs to have the same value)
        :param rebuild: boolean
                     If true, prevents the server from being rebuilt (currently delete and rebuild attribute needs to have the same value)
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_protection(self, delete, rebuild)

    def request_console(self) -> RequestConsoleResponse:
        """Requests credentials for remote access via vnc over websocket to keyboard, monitor, and mouse for a server.

        :return: :class:`RequestConsoleResponse <hcloud.servers.domain.RequestConsoleResponse>`
        """
        return self._client.request_console(self)

    def attach_to_network(
        self,
        network: Network | BoundNetwork,
        ip: str | None = None,
        alias_ips: list[str] | None = None,
    ) -> BoundAction:
        """Attaches a server to a network

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param ip: str
                IP to request to be assigned to this server
        :param alias_ips: List[str]
                New alias IPs to set for this server.
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.attach_to_network(self, network, ip, alias_ips)

    def detach_from_network(self, network: Network | BoundNetwork) -> BoundAction:
        """Detaches a server from a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.detach_from_network(self, network)

    def change_alias_ips(
        self,
        network: Network | BoundNetwork,
        alias_ips: list[str],
    ) -> BoundAction:
        """Changes the alias IPs of an already attached network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param alias_ips: List[str]
                New alias IPs to set for this server.
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_alias_ips(self, network, alias_ips)

    def add_to_placement_group(
        self,
        placement_group: PlacementGroup | BoundPlacementGroup,
    ) -> BoundAction:
        """Adds a server to a placement group.

        :param placement_group: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>` or :class:`Network <hcloud.placement_groups.domain.PlacementGroup>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.add_to_placement_group(self, placement_group)

    def remove_from_placement_group(self) -> BoundAction:
        """Removes a server from a placement group.

        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.remove_from_placement_group(self)


class ServersPageResult(NamedTuple):
    servers: list[BoundServer]
    meta: Meta | None


class ServersClient(ClientEntityBase):
    _client: Client

    actions: ResourceActionsClient
    """Servers scoped actions client

    :type: :class:`ResourceActionsClient <hcloud.actions.client.ResourceActionsClient>`
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.actions = ResourceActionsClient(client, "/servers")

    def get_by_id(self, id: int) -> BoundServer:
        """Get a specific server

        :param id: int
        :return: :class:`BoundServer <hcloud.servers.client.BoundServer>`
        """
        response = self._client.request(url=f"/servers/{id}", method="GET")
        return BoundServer(self, response["server"])

    def get_list(
        self,
        name: str | None = None,
        label_selector: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        status: list[str] | None = None,
    ) -> ServersPageResult:
        """Get a list of servers from this account

        :param name: str (optional)
               Can be used to filter servers by their name.
        :param label_selector: str (optional)
               Can be used to filter servers by labels. The response will only contain servers matching the label selector.
        :param status: List[str] (optional)
               Can be used to filter servers by their status. The response will only contain servers matching the status.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundServer <hcloud.servers.client.BoundServer>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if label_selector is not None:
            params["label_selector"] = label_selector
        if status is not None:
            params["status"] = status
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url="/servers", method="GET", params=params)

        ass_servers = [
            BoundServer(self, server_data) for server_data in response["servers"]
        ]
        return ServersPageResult(ass_servers, Meta.parse_meta(response))

    def get_all(
        self,
        name: str | None = None,
        label_selector: str | None = None,
        status: list[str] | None = None,
    ) -> list[BoundServer]:
        """Get all servers from this account

        :param name: str (optional)
               Can be used to filter servers by their name.
        :param label_selector: str (optional)
               Can be used to filter servers by labels. The response will only contain servers matching the label selector.
        :param status: List[str] (optional)
               Can be used to filter servers by their status. The response will only contain servers matching the status.
        :return: List[:class:`BoundServer <hcloud.servers.client.BoundServer>`]
        """
        return self._iter_pages(
            self.get_list,
            name=name,
            label_selector=label_selector,
            status=status,
        )

    def get_by_name(self, name: str) -> BoundServer | None:
        """Get server by name

        :param name: str
               Used to get server by name.
        :return: :class:`BoundServer <hcloud.servers.client.BoundServer>`
        """
        return self._get_first_by(name=name)

    # pylint: disable=too-many-branches,too-many-locals
    def create(
        self,
        name: str,
        server_type: ServerType | BoundServerType,
        image: Image,
        ssh_keys: list[SSHKey | BoundSSHKey] | None = None,
        volumes: list[Volume | BoundVolume] | None = None,
        firewalls: list[Firewall | BoundFirewall] | None = None,
        networks: list[Network | BoundNetwork] | None = None,
        user_data: str | None = None,
        labels: dict[str, str] | None = None,
        location: Location | BoundLocation | None = None,
        datacenter: Datacenter | BoundDatacenter | None = None,
        start_after_create: bool | None = True,
        automount: bool | None = None,
        placement_group: PlacementGroup | BoundPlacementGroup | None = None,
        public_net: ServerCreatePublicNetwork | None = None,
    ) -> CreateServerResponse:
        """Creates a new server. Returns preliminary information about the server as well as an action that covers progress of creation.

        :param name: str
               Name of the server to create (must be unique per project and a valid hostname as per RFC 1123)
        :param server_type: :class:`BoundServerType <hcloud.server_types.client.BoundServerType>` or :class:`ServerType <hcloud.server_types.domain.ServerType>`
               Server type this server should be created with
        :param image: :class:`BoundImage <hcloud.images.client.BoundImage>` or :class:`Image <hcloud.images.domain.Image>`
               Image the server is created from
        :param ssh_keys: List[:class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>` or :class:`SSHKey <hcloud.ssh_keys.domain.SSHKey>`] (optional)
               SSH keys which should be injected into the server at creation time
        :param volumes: List[:class:`BoundVolume <hcloud.volumes.client.BoundVolume>` or :class:`Volume <hcloud.volumes.domain.Volume>`] (optional)
               Volumes which should be attached to the server at the creation time. Volumes must be in the same location.
        :param networks: List[:class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`] (optional)
               Networks which should be attached to the server at the creation time.
        :param user_data: str (optional)
               Cloud-Init user data to use during server creation. This field is limited to 32KiB.
        :param labels: Dict[str,str] (optional)
               User-defined labels (key-value pairs)
        :param location: :class:`BoundLocation <hcloud.locations.client.BoundLocation>` or :class:`Location <hcloud.locations.domain.Location>`
        :param datacenter: :class:`BoundDatacenter <hcloud.datacenters.client.BoundDatacenter>` or :class:`Datacenter <hcloud.datacenters.domain.Datacenter>`
        :param start_after_create: boolean (optional)
               Start Server right after creation. Defaults to True.
        :param automount: boolean (optional)
               Auto mount volumes after attach.
        :param placement_group: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>` or :class:`Location <hcloud.placement_groups.domain.PlacementGroup>`
               Placement Group where server should be added during creation
        :param public_net: :class:`ServerCreatePublicNetwork <hcloud.servers.domain.ServerCreatePublicNetwork>`
               Options to configure the public network of a server on creation
        :return: :class:`CreateServerResponse <hcloud.servers.domain.CreateServerResponse>`
        """
        data: dict[str, Any] = {
            "name": name,
            "server_type": server_type.id_or_name,
            "start_after_create": start_after_create,
            "image": image.id_or_name,
        }

        if location is not None:
            data["location"] = location.id_or_name
        if datacenter is not None:
            data["datacenter"] = datacenter.id_or_name
        if ssh_keys is not None:
            data["ssh_keys"] = [ssh_key.id_or_name for ssh_key in ssh_keys]
        if volumes is not None:
            data["volumes"] = [volume.id for volume in volumes]
        if networks is not None:
            data["networks"] = [network.id for network in networks]
        if firewalls is not None:
            data["firewalls"] = [{"firewall": firewall.id} for firewall in firewalls]
        if user_data is not None:
            data["user_data"] = user_data
        if labels is not None:
            data["labels"] = labels
        if automount is not None:
            data["automount"] = automount
        if placement_group is not None:
            data["placement_group"] = placement_group.id

        if public_net is not None:
            data_public_net: dict[str, Any] = {
                "enable_ipv4": public_net.enable_ipv4,
                "enable_ipv6": public_net.enable_ipv6,
            }
            if public_net.ipv4 is not None:
                data_public_net["ipv4"] = public_net.ipv4.id
            if public_net.ipv6 is not None:
                data_public_net["ipv6"] = public_net.ipv6.id
            data["public_net"] = data_public_net

        response = self._client.request(url="/servers", method="POST", json=data)

        result = CreateServerResponse(
            server=BoundServer(self, response["server"]),
            action=BoundAction(self._client.actions, response["action"]),
            next_actions=[
                BoundAction(self._client.actions, action)
                for action in response["next_actions"]
            ],
            root_password=response["root_password"],
        )
        return result

    def get_actions_list(
        self,
        server: Server | BoundServer,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """Returns all action objects for a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundAction <hcloud.actions.client.BoundAction>`], :class:`Meta <hcloud.core.domain.Meta>`)
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
            url=f"/servers/{server.id}/actions",
            method="GET",
            params=params,
        )
        actions = [
            BoundAction(self._client.actions, action_data)
            for action_data in response["actions"]
        ]
        return ActionsPageResult(actions, Meta.parse_meta(response))

    def get_actions(
        self,
        server: Server | BoundServer,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """Returns all action objects for a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._iter_pages(
            self.get_actions_list,
            server,
            status=status,
            sort=sort,
        )

    def update(
        self,
        server: Server | BoundServer,
        name: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundServer:
        """Updates a server. You can update a server’s name and a server’s labels.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param name: str (optional)
               New name to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundServer <hcloud.servers.client.BoundServer>`
        """
        data: dict[str, Any] = {}
        if name is not None:
            data.update({"name": name})
        if labels is not None:
            data.update({"labels": labels})
        response = self._client.request(
            url=f"/servers/{server.id}",
            method="PUT",
            json=data,
        )
        return BoundServer(self, response["server"])

    def get_metrics(
        self,
        server: Server | BoundServer,
        type: MetricsType | list[MetricsType],
        start: datetime | str,
        end: datetime | str,
        step: float | None = None,
    ) -> GetMetricsResponse:
        """Get Metrics for a Server.

        :param server: The Server to get the metrics for.
        :param type: Type of metrics to get.
        :param start: Start of period to get Metrics for (in ISO-8601 format).
        :param end: End of period to get Metrics for (in ISO-8601 format).
        :param step: Resolution of results in seconds.
        """
        if not isinstance(type, list):
            type = [type]
        if isinstance(start, str):
            start = isoparse(start)
        if isinstance(end, str):
            end = isoparse(end)

        params: dict[str, Any] = {
            "type": ",".join(type),
            "start": start.isoformat(),
            "end": end.isoformat(),
        }
        if step is not None:
            params["step"] = step

        response = self._client.request(
            url=f"/servers/{server.id}/metrics",
            method="GET",
            params=params,
        )
        return GetMetricsResponse(
            metrics=Metrics(**response["metrics"]),
        )

    def delete(self, server: Server | BoundServer) -> BoundAction:
        """Deletes a server. This immediately removes the server from your account, and it is no longer accessible.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(url=f"/servers/{server.id}", method="DELETE")
        return BoundAction(self._client.actions, response["action"])

    def power_off(self, server: Server | BoundServer) -> BoundAction:
        """Cuts power to the server. This forcefully stops it without giving the server operating system time to gracefully stop

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"/servers/{server.id}/actions/poweroff",
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def power_on(self, server: Server | BoundServer) -> BoundAction:
        """Starts a server by turning its power on.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"/servers/{server.id}/actions/poweron",
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def reboot(self, server: Server | BoundServer) -> BoundAction:
        """Reboots a server gracefully by sending an ACPI request.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"/servers/{server.id}/actions/reboot",
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def reset(self, server: Server | BoundServer) -> BoundAction:
        """Cuts power to a server and starts it again.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"/servers/{server.id}/actions/reset",
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def shutdown(self, server: Server | BoundServer) -> BoundAction:
        """Shuts down a server gracefully by sending an ACPI shutdown request.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"/servers/{server.id}/actions/shutdown",
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def reset_password(self, server: Server | BoundServer) -> ResetPasswordResponse:
        """Resets the root password. Only works for Linux systems that are running the qemu guest agent.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return: :class:`ResetPasswordResponse <hcloud.servers.domain.ResetPasswordResponse>`
        """
        response = self._client.request(
            url=f"/servers/{server.id}/actions/reset_password",
            method="POST",
        )
        return ResetPasswordResponse(
            action=BoundAction(self._client.actions, response["action"]),
            root_password=response["root_password"],
        )

    def change_type(
        self,
        server: Server | BoundServer,
        server_type: ServerType | BoundServerType,
        upgrade_disk: bool,
    ) -> BoundAction:
        """Changes the type (Cores, RAM and disk sizes) of a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param server_type: :class:`BoundServerType <hcloud.server_types.client.BoundServerType>` or :class:`ServerType <hcloud.server_types.domain.ServerType>`
               Server type the server should migrate to
        :param upgrade_disk: boolean
               If false, do not upgrade the disk. This allows downgrading the server type later.
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {
            "server_type": server_type.id_or_name,
            "upgrade_disk": upgrade_disk,
        }
        response = self._client.request(
            url=f"/servers/{server.id}/actions/change_type",
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def enable_rescue(
        self,
        server: Server | BoundServer,
        type: str | None = None,
        ssh_keys: list[str] | None = None,
    ) -> EnableRescueResponse:
        """Enable the Hetzner Rescue System for this server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param type: str
                Type of rescue system to boot (default: linux64)
                Choices: linux64, linux32, freebsd64
        :param ssh_keys: List[str]
                Array of SSH key IDs which should be injected into the rescue system. Only available for types: linux64 and linux32.
        :return: :class:`EnableRescueResponse <hcloud.servers.domain.EnableRescueResponse>`
        """
        data: dict[str, Any] = {"type": type}
        if ssh_keys is not None:
            data.update({"ssh_keys": ssh_keys})

        response = self._client.request(
            url=f"/servers/{server.id}/actions/enable_rescue",
            method="POST",
            json=data,
        )
        return EnableRescueResponse(
            action=BoundAction(self._client.actions, response["action"]),
            root_password=response["root_password"],
        )

    def disable_rescue(self, server: Server | BoundServer) -> BoundAction:
        """Disables the Hetzner Rescue System for a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"/servers/{server.id}/actions/disable_rescue",
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def create_image(
        self,
        server: Server | BoundServer,
        description: str | None = None,
        type: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> CreateImageResponse:
        """Creates an image (snapshot) from a server by copying the contents of its disks.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param description: str (optional)
               Description of the image. If you do not set this we auto-generate one for you.
        :param type: str (optional)
               Type of image to create (default: snapshot)
               Choices: snapshot, backup
        :param labels: Dict[str, str]
               User-defined labels (key-value pairs)
        :return:  :class:`CreateImageResponse <hcloud.images.domain.CreateImageResponse>`
        """
        data: dict[str, Any] = {}
        if description is not None:
            data.update({"description": description})

        if type is not None:
            data.update({"type": type})

        if labels is not None:
            data.update({"labels": labels})

        response = self._client.request(
            url=f"/servers/{server.id}/actions/create_image",
            method="POST",
            json=data,
        )
        return CreateImageResponse(
            action=BoundAction(self._client.actions, response["action"]),
            image=BoundImage(self._client.images, response["image"]),
        )

    def rebuild(
        self,
        server: Server | BoundServer,
        image: Image | BoundImage,
        # pylint: disable=unused-argument
        **kwargs: Any,
    ) -> RebuildResponse:
        """Rebuilds a server overwriting its disk with the content of an image, thereby destroying all data on the target server.

        :param server: Server to rebuild
        :param image: Image to use for the rebuilt server
        """
        data: dict[str, Any] = {"image": image.id_or_name}
        response = self._client.request(
            url=f"/servers/{server.id}/actions/rebuild",
            method="POST",
            json=data,
        )

        return RebuildResponse(
            action=BoundAction(self._client.actions, response["action"]),
            root_password=response.get("root_password"),
        )

    def enable_backup(self, server: Server | BoundServer) -> BoundAction:
        """Enables and configures the automatic daily backup option for the server. Enabling automatic backups will increase the price of the server by 20%.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"/servers/{server.id}/actions/enable_backup",
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def disable_backup(self, server: Server | BoundServer) -> BoundAction:
        """Disables the automatic backup option and deletes all existing Backups for a Server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"/servers/{server.id}/actions/disable_backup",
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def attach_iso(
        self,
        server: Server | BoundServer,
        iso: Iso | BoundIso,
    ) -> BoundAction:
        """Attaches an ISO to a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param iso: :class:`BoundIso <hcloud.isos.client.BoundIso>` or :class:`Server <hcloud.isos.domain.Iso>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {"iso": iso.id_or_name}
        response = self._client.request(
            url=f"/servers/{server.id}/actions/attach_iso",
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def detach_iso(self, server: Server | BoundServer) -> BoundAction:
        """Detaches an ISO from a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"/servers/{server.id}/actions/detach_iso",
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def change_dns_ptr(
        self,
        server: Server | BoundServer,
        ip: str,
        dns_ptr: str | None,
    ) -> BoundAction:
        """Changes the hostname that will appear when getting the hostname belonging to the primary IPs (ipv4 and ipv6) of this server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param ip: str
                   The IP address for which to set the reverse DNS entry
        :param dns_ptr:
                  Hostname to set as a reverse DNS PTR entry, will reset to original default value if `None`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {"ip": ip, "dns_ptr": dns_ptr}
        response = self._client.request(
            url=f"/servers/{server.id}/actions/change_dns_ptr",
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def change_protection(
        self,
        server: Server | BoundServer,
        delete: bool | None = None,
        rebuild: bool | None = None,
    ) -> BoundAction:
        """Changes the protection configuration of the server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param delete: boolean
                     If true, prevents the server from being deleted (currently delete and rebuild attribute needs to have the same value)
        :param rebuild: boolean
                     If true, prevents the server from being rebuilt (currently delete and rebuild attribute needs to have the same value)
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {}
        if delete is not None:
            data.update({"delete": delete})
        if rebuild is not None:
            data.update({"rebuild": rebuild})

        response = self._client.request(
            url=f"/servers/{server.id}/actions/change_protection",
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def request_console(self, server: Server | BoundServer) -> RequestConsoleResponse:
        """Requests credentials for remote access via vnc over websocket to keyboard, monitor, and mouse for a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return: :class:`RequestConsoleResponse <hcloud.servers.domain.RequestConsoleResponse>`
        """
        response = self._client.request(
            url=f"/servers/{server.id}/actions/request_console",
            method="POST",
        )
        return RequestConsoleResponse(
            action=BoundAction(self._client.actions, response["action"]),
            wss_url=response["wss_url"],
            password=response["password"],
        )

    def attach_to_network(
        self,
        server: Server | BoundServer,
        network: Network | BoundNetwork,
        ip: str | None = None,
        alias_ips: list[str] | None = None,
    ) -> BoundAction:
        """Attaches a server to a network

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param ip: str
                IP to request to be assigned to this server
        :param alias_ips: List[str]
                New alias IPs to set for this server.
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {"network": network.id}
        if ip is not None:
            data.update({"ip": ip})
        if alias_ips is not None:
            data.update({"alias_ips": alias_ips})
        response = self._client.request(
            url=f"/servers/{server.id}/actions/attach_to_network",
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def detach_from_network(
        self,
        server: Server | BoundServer,
        network: Network | BoundNetwork,
    ) -> BoundAction:
        """Detaches a server from a network.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {"network": network.id}
        response = self._client.request(
            url=f"/servers/{server.id}/actions/detach_from_network",
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def change_alias_ips(
        self,
        server: Server | BoundServer,
        network: Network | BoundNetwork,
        alias_ips: list[str],
    ) -> BoundAction:
        """Changes the alias IPs of an already attached network.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param alias_ips: List[str]
                New alias IPs to set for this server.
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {"network": network.id, "alias_ips": alias_ips}
        response = self._client.request(
            url=f"/servers/{server.id}/actions/change_alias_ips",
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def add_to_placement_group(
        self,
        server: Server | BoundServer,
        placement_group: PlacementGroup | BoundPlacementGroup,
    ) -> BoundAction:
        """Adds a server to a placement group.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param placement_group: :class:`BoundPlacementGroup <hcloud.placement_groups.client.BoundPlacementGroup>` or :class:`Network <hcloud.placement_groups.domain.PlacementGroup>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {"placement_group": str(placement_group.id)}
        response = self._client.request(
            url=f"/servers/{server.id}/actions/add_to_placement_group",
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def remove_from_placement_group(self, server: Server | BoundServer) -> BoundAction:
        """Removes a server from a placement group.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"/servers/{server.id}/actions/remove_from_placement_group",
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])
