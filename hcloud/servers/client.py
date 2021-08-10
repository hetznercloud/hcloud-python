# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase, GetEntityByNameMixin

from hcloud.actions.client import BoundAction
from hcloud.core.domain import add_meta_to_result
from hcloud.firewalls.client import BoundFirewall
from hcloud.floating_ips.client import BoundFloatingIP
from hcloud.isos.client import BoundIso
from hcloud.servers.domain import (
    Server,
    CreateServerResponse,
    ResetPasswordResponse,
    EnableRescueResponse,
    RequestConsoleResponse,
    PublicNetwork,
    IPv4Address,
    IPv6Network,
    PrivateNet,
    PublicNetworkFirewall,
)
from hcloud.volumes.client import BoundVolume
from hcloud.images.domain import CreateImageResponse
from hcloud.images.client import BoundImage
from hcloud.server_types.client import BoundServerType
from hcloud.datacenters.client import BoundDatacenter
from hcloud.networks.client import BoundNetwork  # noqa
from hcloud.networks.domain import Network  # noqa


class BoundServer(BoundModelBase):
    model = Server

    def __init__(self, client, data, complete=True):

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
            ipv4_address = IPv4Address.from_dict(public_net["ipv4"])
            ipv6_network = IPv6Network.from_dict(public_net["ipv6"])
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
                floating_ips=floating_ips,
                firewalls=firewalls,
            )

        private_nets = data.get("private_net")
        if private_nets:
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

        super(BoundServer, self).__init__(client, data, complete)

    def get_actions_list(self, status=None, sort=None, page=None, per_page=None):
        # type: (Optional[List[str]], Optional[List[str]], Optional[int], Optional[int]) -> PageResults[List[BoundAction, Meta]]
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

    def get_actions(self, status=None, sort=None):
        # type: (Optional[List[str]], Optional[List[str]]) -> List[BoundAction]
        """Returns all action objects for a server.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.get_actions(self, status, sort)

    def update(self, name=None, labels=None):
        # type: (Optional[str], Optional[Dict[str, str]]) -> BoundServer
        """Updates a server. You can update a server’s name and a server’s labels.

        :param name: str (optional)
               New name to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundServer <hcloud.servers.client.BoundServer>`
        """
        return self._client.update(self, name, labels)

    def delete(self):
        # type: () -> BoundAction
        """Deletes a server. This immediately removes the server from your account, and it is no longer accessible.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.delete(self)

    def power_off(self):
        # type: () -> BoundAction
        """Cuts power to the server. This forcefully stops it without giving the server operating system time to gracefully stop

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.power_off(self)

    def power_on(self):
        # type: () -> BoundAction
        """Starts a server by turning its power on.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.power_on(self)

    def reboot(self):
        # type: () -> BoundAction
        """Reboots a server gracefully by sending an ACPI request.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.reboot(self)

    def reset(self):
        # type: () -> BoundAction
        """Cuts power to a server and starts it again.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.reset(self)

    def shutdown(self):
        # type: () -> BoundAction
        """Shuts down a server gracefully by sending an ACPI shutdown request.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.shutdown(self)

    def reset_password(self):
        # type: () -> ResetPasswordResponse
        """Resets the root password. Only works for Linux systems that are running the qemu guest agent.

        :return: :class:`ResetPasswordResponse <hcloud.servers.domain.ResetPasswordResponse>`
        """
        return self._client.reset_password(self)

    def enable_rescue(self, type=None, ssh_keys=None):
        # type: (str, Optional[List[str]]) -> EnableRescueResponse
        """Enable the Hetzner Rescue System for this server.

        :param type: str
                Type of rescue system to boot (default: linux64)
                Choices: linux64, linux32, freebsd64
        :param ssh_keys: List[str]
                Array of SSH key IDs which should be injected into the rescue system. Only available for types: linux64 and linux32.
        :return: :class:`EnableRescueResponse <hcloud.servers.domain.EnableRescueResponse>`
        """
        return self._client.enable_rescue(self, type=type, ssh_keys=ssh_keys)

    def disable_rescue(self):
        # type: () -> BoundAction
        """Disables the Hetzner Rescue System for a server.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.disable_rescue(self)

    def create_image(self, description=None, type=None, labels=None):
        # type: (str, str, Optional[Dict[str, str]]) -> CreateImageResponse
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

    def rebuild(self, image):
        # type: (Image) -> BoundAction
        """Rebuilds a server overwriting its disk with the content of an image, thereby destroying all data on the target server.

        :param image: :class:`BoundImage <hcloud.images.client.BoundImage>` or :class:`Image <hcloud.servers.domain.Image>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.rebuild(self, image)

    def change_type(self, server_type, upgrade_disk):
        # type: (BoundServerType, bool) -> BoundAction
        """Changes the type (Cores, RAM and disk sizes) of a server.

        :param server_type: :class:`BoundServerType <hcloud.server_types.client.BoundServerType>` or :class:`ServerType <hcloud.server_types.domain.ServerType>`
               Server type the server should migrate to
        :param upgrade_disk: boolean
               If false, do not upgrade the disk. This allows downgrading the server type later.
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_type(self, server_type, upgrade_disk)

    def enable_backup(self):
        # type: () -> BoundAction
        """Enables and configures the automatic daily backup option for the server. Enabling automatic backups will increase the price of the server by 20%.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.enable_backup(self)

    def disable_backup(self):
        # type: () -> BoundAction
        """Disables the automatic backup option and deletes all existing Backups for a Server.

        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.disable_backup(self)

    def attach_iso(self, iso):
        # type: (Iso) -> BoundAction
        """Attaches an ISO to a server.

        :param iso: :class:`BoundIso <hcloud.isos.client.BoundIso>` or :class:`Server <hcloud.isos.domain.Iso>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.attach_iso(self, iso)

    def detach_iso(self):
        # type: () -> BoundAction
        """Detaches an ISO from a server.

        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.detach_iso(self)

    def change_dns_ptr(self, ip, dns_ptr):
        # type: (str, Optional[str]) -> BoundAction
        """Changes the hostname that will appear when getting the hostname belonging to the primary IPs (ipv4 and ipv6) of this server.

        :param ip: str
                   The IP address for which to set the reverse DNS entry
        :param dns_ptr:
                  Hostname to set as a reverse DNS PTR entry, will reset to original default value if `None`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_dns_ptr(self, ip, dns_ptr)

    def change_protection(self, delete=None, rebuild=None):
        # type: (Optional[bool], Optional[bool]) -> BoundAction
        """Changes the protection configuration of the server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param delete: boolean
                     If true, prevents the server from being deleted (currently delete and rebuild attribute needs to have the same value)
        :param rebuild: boolean
                     If true, prevents the server from being rebuilt (currently delete and rebuild attribute needs to have the same value)
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_protection(self, delete, rebuild)

    def request_console(self):
        # type: () -> RequestConsoleResponse
        """Requests credentials for remote access via vnc over websocket to keyboard, monitor, and mouse for a server.

        :return: :class:`RequestConsoleResponse <hcloud.servers.domain.RequestConsoleResponse>`
        """
        return self._client.request_console(self)

    def attach_to_network(self, network, ip=None, alias_ips=None):
        # type: (Union[Network,BoundNetwork],Optional[str], Optional[List[str]]) -> BoundAction
        """Attaches a server to a network

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param ip: str
                IP to request to be assigned to this server
        :param alias_ips: List[str]
                New alias IPs to set for this server.
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.attach_to_network(self, network, ip, alias_ips)

    def detach_from_network(self, network):
        # type: ( Union[Network,BoundNetwork]) -> BoundAction
        """Detaches a server from a network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.detach_from_network(self, network)

    def change_alias_ips(self, network, alias_ips):
        # type: (Union[Network,BoundNetwork], List[str]) -> BoundAction
        """Changes the alias IPs of an already attached network.

        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param alias_ips: List[str]
                New alias IPs to set for this server.
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_alias_ips(self, network, alias_ips)


class ServersClient(ClientEntityBase, GetEntityByNameMixin):
    results_list_attribute_name = "servers"

    def get_by_id(self, id):
        # type: (int) -> BoundServer
        """Get a specific server

        :param id: int
        :return: :class:`BoundServer <hcloud.servers.client.BoundServer>`
        """
        response = self._client.request(
            url="/servers/{server_id}".format(server_id=id), method="GET"
        )
        return BoundServer(self, response["server"])

    def get_list(
        self,
        name=None,  # type: Optional[str]
        label_selector=None,  # type: Optional[str]
        page=None,  # type: Optional[int]
        per_page=None,  # type: Optional[int]
        status=None,  # type: Optional[List[str]]
    ):
        # type: (...) -> PageResults[List[BoundServer], Meta]
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
        params = {}
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
        return self._add_meta_to_result(ass_servers, response)

    def get_all(self, name=None, label_selector=None, status=None):
        # type: (Optional[str], Optional[str], Optional[List[str]]) -> List[BoundServer]
        """Get all servers from this account

        :param name: str (optional)
               Can be used to filter servers by their name.
        :param label_selector: str (optional)
               Can be used to filter servers by labels. The response will only contain servers matching the label selector.
        :param status: List[str] (optional)
               Can be used to filter servers by their status. The response will only contain servers matching the status.
        :return: List[:class:`BoundServer <hcloud.servers.client.BoundServer>`]
        """
        return super(ServersClient, self).get_all(
            name=name, label_selector=label_selector, status=status
        )

    def get_by_name(self, name):
        # type: (str) -> BoundServer
        """Get server by name

        :param name: str
               Used to get server by name.
        :return: :class:`BoundServer <hcloud.servers.client.BoundServer>`
        """
        return super(ServersClient, self).get_by_name(name)

    def create(
        self,
        name,  # type: str
        server_type,  # type: ServerType
        image,  # type: Image
        ssh_keys=None,  # type: Optional[List[SSHKey]]
        volumes=None,  # type: Optional[List[Volume]]
        firewalls=None,  # type: Optional[List[Firewall]]
        networks=None,  # type: Optional[List[Network]]
        user_data=None,  # type: Optional[str]
        labels=None,  # type: Optional[Dict[str, str]]
        location=None,  # type: Optional[Location]
        datacenter=None,  # type: Optional[Datacenter]
        start_after_create=True,  # type: Optional[bool]
        automount=None,  # type: Optional[bool]
    ):
        # type: (...) -> CreateServerResponse
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
        :return: :class:`CreateServerResponse <hcloud.servers.domain.CreateServerResponse>`
        """
        data = {
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
        self, server, status=None, sort=None, page=None, per_page=None
    ):
        # type: (Server, Optional[List[str]], Optional[List[str]], Optional[int], Optional[int]) -> PageResults[List[BoundAction], Meta]
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
        params = {}
        if status is not None:
            params["status"] = status
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(
            url="/servers/{server_id}/actions".format(server_id=server.id),
            method="GET",
            params=params,
        )
        actions = [
            BoundAction(self._client.actions, action_data)
            for action_data in response["actions"]
        ]
        return add_meta_to_result(actions, response, "actions")

    def get_actions(self, server, status=None, sort=None):
        # type: (Server, Optional[List[str]], Optional[List[str]]) -> List[BoundAction]
        """Returns all action objects for a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return super(ServersClient, self).get_actions(server, status=status, sort=sort)

    def update(self, server, name=None, labels=None):
        # type:(Server,  Optional[str],  Optional[Dict[str, str]]) -> BoundServer
        """Updates a server. You can update a server’s name and a server’s labels.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param name: str (optional)
               New name to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundServer <hcloud.servers.client.BoundServer>`
        """
        data = {}
        if name is not None:
            data.update({"name": name})
        if labels is not None:
            data.update({"labels": labels})
        response = self._client.request(
            url="/servers/{server_id}".format(server_id=server.id),
            method="PUT",
            json=data,
        )
        return BoundServer(self, response["server"])

    def delete(self, server):
        # type: (Server) -> BoundAction
        """Deletes a server. This immediately removes the server from your account, and it is no longer accessible.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/servers/{server_id}".format(server_id=server.id), method="DELETE"
        )
        return BoundAction(self._client.actions, response["action"])

    def power_off(self, server):
        # type: (Server) -> Action
        """Cuts power to the server. This forcefully stops it without giving the server operating system time to gracefully stop

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/servers/{server_id}/actions/poweroff".format(server_id=server.id),
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def power_on(self, server):
        # type: (servers.domain.Server) -> actions.domain.Action
        """Starts a server by turning its power on.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/servers/{server_id}/actions/poweron".format(server_id=server.id),
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def reboot(self, server):
        # type: (servers.domain.Server) -> actions.domain.Action
        """Reboots a server gracefully by sending an ACPI request.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/servers/{server_id}/actions/reboot".format(server_id=server.id),
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def reset(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        """Cuts power to a server and starts it again.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/servers/{server_id}/actions/reset".format(server_id=server.id),
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def shutdown(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        """Shuts down a server gracefully by sending an ACPI shutdown request.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/servers/{server_id}/actions/shutdown".format(server_id=server.id),
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def reset_password(self, server):
        # type: (servers.domain.Server) -> ResetPasswordResponse
        """Resets the root password. Only works for Linux systems that are running the qemu guest agent.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return: :class:`ResetPasswordResponse <hcloud.servers.domain.ResetPasswordResponse>`
        """
        response = self._client.request(
            url="/servers/{server_id}/actions/reset_password".format(
                server_id=server.id
            ),
            method="POST",
        )
        return ResetPasswordResponse(
            action=BoundAction(self._client.actions, response["action"]),
            root_password=response["root_password"],
        )

    def change_type(self, server, server_type, upgrade_disk):
        # type: (servers.domain.Server, BoundServerType, bool) -> actions.domainAction
        """Changes the type (Cores, RAM and disk sizes) of a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param server_type: :class:`BoundServerType <hcloud.server_types.client.BoundServerType>` or :class:`ServerType <hcloud.server_types.domain.ServerType>`
               Server type the server should migrate to
        :param upgrade_disk: boolean
               If false, do not upgrade the disk. This allows downgrading the server type later.
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {"server_type": server_type.id_or_name, "upgrade_disk": upgrade_disk}
        response = self._client.request(
            url="/servers/{server_id}/actions/change_type".format(server_id=server.id),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def enable_rescue(self, server, type=None, ssh_keys=None):
        # type: (servers.domain.Server, str, Optional[List[str]]) -> EnableRescueResponse
        """Enable the Hetzner Rescue System for this server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param type: str
                Type of rescue system to boot (default: linux64)
                Choices: linux64, linux32, freebsd64
        :param ssh_keys: List[str]
                Array of SSH key IDs which should be injected into the rescue system. Only available for types: linux64 and linux32.
        :return: :class:`EnableRescueResponse <hcloud.servers.domain.EnableRescueResponse>`
        """
        data = {"type": type}
        if ssh_keys is not None:
            data.update({"ssh_keys": ssh_keys})

        response = self._client.request(
            url="/servers/{server_id}/actions/enable_rescue".format(
                server_id=server.id
            ),
            method="POST",
            json=data,
        )
        return EnableRescueResponse(
            action=BoundAction(self._client.actions, response["action"]),
            root_password=response["root_password"],
        )

    def disable_rescue(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        """Disables the Hetzner Rescue System for a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/servers/{server_id}/actions/disable_rescue".format(
                server_id=server.id
            ),
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def create_image(self, server, description=None, type=None, labels=None):
        # type: (servers.domain.Server, str, str, Optional[Dict[str, str]]) -> CreateImageResponse
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
        data = {}
        if description is not None:
            data.update({"description": description})

        if type is not None:
            data.update({"type": type})

        if labels is not None:
            data.update({"labels": labels})

        response = self._client.request(
            url="/servers/{server_id}/actions/create_image".format(server_id=server.id),
            method="POST",
            json=data,
        )
        return CreateImageResponse(
            action=BoundAction(self._client.actions, response["action"]),
            image=BoundImage(self._client.images, response["image"]),
        )

    def rebuild(self, server, image):
        # type: (servers.domain.Server, Image) -> actions.domainAction
        """Rebuilds a server overwriting its disk with the content of an image, thereby destroying all data on the target server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param image: :class:`BoundImage <hcloud.images.client.BoundImage>` or :class:`Image <hcloud.servers.domain.Image>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {"image": image.id_or_name}
        response = self._client.request(
            url="/servers/{server_id}/actions/rebuild".format(server_id=server.id),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def enable_backup(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        """Enables and configures the automatic daily backup option for the server. Enabling automatic backups will increase the price of the server by 20%.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/servers/{server_id}/actions/enable_backup".format(
                server_id=server.id
            ),
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def disable_backup(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        """Disables the automatic backup option and deletes all existing Backups for a Server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/servers/{server_id}/actions/disable_backup".format(
                server_id=server.id
            ),
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def attach_iso(self, server, iso):
        # type: (servers.domain.Server, Iso) -> actions.domainAction
        """Attaches an ISO to a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param iso: :class:`BoundIso <hcloud.isos.client.BoundIso>` or :class:`Server <hcloud.isos.domain.Iso>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {"iso": iso.id_or_name}
        response = self._client.request(
            url="/servers/{server_id}/actions/attach_iso".format(server_id=server.id),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def detach_iso(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        """Detaches an ISO from a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/servers/{server_id}/actions/detach_iso".format(server_id=server.id),
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def change_dns_ptr(self, server, ip, dns_ptr):
        # type: (servers.domain.Server, str, str) -> actions.domainAction
        """Changes the hostname that will appear when getting the hostname belonging to the primary IPs (ipv4 and ipv6) of this server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param ip: str
                   The IP address for which to set the reverse DNS entry
        :param dns_ptr:
                  Hostname to set as a reverse DNS PTR entry, will reset to original default value if `None`
        :return:  :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {"ip": ip, "dns_ptr": dns_ptr}
        response = self._client.request(
            url="/servers/{server_id}/actions/change_dns_ptr".format(
                server_id=server.id
            ),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def change_protection(self, server, delete=None, rebuild=None):
        # type: (servers.domain.Server, Optional[bool], Optional[bool]) -> actions.domainAction
        """Changes the protection configuration of the server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param delete: boolean
                     If true, prevents the server from being deleted (currently delete and rebuild attribute needs to have the same value)
        :param rebuild: boolean
                     If true, prevents the server from being rebuilt (currently delete and rebuild attribute needs to have the same value)
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {}
        if delete is not None:
            data.update({"delete": delete})
        if rebuild is not None:
            data.update({"rebuild": rebuild})

        response = self._client.request(
            url="/servers/{server_id}/actions/change_protection".format(
                server_id=server.id
            ),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def request_console(self, server):
        # type: (servers.domain.Server) -> RequestConsoleResponse
        """Requests credentials for remote access via vnc over websocket to keyboard, monitor, and mouse for a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :return: :class:`RequestConsoleResponse <hcloud.servers.domain.RequestConsoleResponse>`
        """
        response = self._client.request(
            url="/servers/{server_id}/actions/request_console".format(
                server_id=server.id
            ),
            method="POST",
        )
        return RequestConsoleResponse(
            action=BoundAction(self._client.actions, response["action"]),
            wss_url=response["wss_url"],
            password=response["password"],
        )

    def attach_to_network(self, server, network, ip=None, alias_ips=None):
        # type: (Union[Server,BoundServer], Union[Network,BoundNetwork],Optional[str], Optional[List[str]]) -> BoundAction
        """Attaches a server to a network

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param ip: str
                IP to request to be assigned to this server
        :param alias_ips: List[str]
                New alias IPs to set for this server.
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {
            "network": network.id,
        }
        if ip is not None:
            data.update({"ip": ip})
        if alias_ips is not None:
            data.update({"alias_ips": alias_ips})
        response = self._client.request(
            url="/servers/{server_id}/actions/attach_to_network".format(
                server_id=server.id
            ),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def detach_from_network(self, server, network):
        # type: (Union[Server,BoundServer], Union[Network,BoundNetwork]) -> BoundAction
        """Detaches a server from a network.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {
            "network": network.id,
        }
        response = self._client.request(
            url="/servers/{server_id}/actions/detach_from_network".format(
                server_id=server.id
            ),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def change_alias_ips(self, server, network, alias_ips):
        # type: (Union[Server,BoundServer], Union[Network,BoundNetwork], List[str]) -> BoundAction
        """Changes the alias IPs of an already attached network.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or :class:`Server <hcloud.servers.domain.Server>`
        :param network: :class:`BoundNetwork <hcloud.networks.client.BoundNetwork>` or :class:`Network <hcloud.networks.domain.Network>`
        :param alias_ips: List[str]
                New alias IPs to set for this server.
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {"network": network.id, "alias_ips": alias_ips}
        response = self._client.request(
            url="/servers/{server_id}/actions/change_alias_ips".format(
                server_id=server.id
            ),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])
