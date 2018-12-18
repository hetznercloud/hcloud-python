# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase

from hcloud.actions.client import BoundAction
from hcloud.isos.client import BoundIso
from hcloud.servers.domain import Server, CreateServerResponse, ResetPasswordResponse, EnableRescueResponse, RequestConsoleResponse
from hcloud.volumes.client import BoundVolume
from hcloud.images.domain import CreateImageResponse
from hcloud.images.client import BoundImage
from hcloud.server_types.client import BoundServerType
from hcloud.datacenters.client import BoundDatacenter


class BoundServer(BoundModelBase):
    model = Server

    def __init__(self, client, data, complete=False):

        datacenter = data.get('datacenter')
        if datacenter is not None:
            data['datacenter'] = BoundDatacenter(client._client.datacenters, datacenter)

        volumes = data.get('volumes', [])
        if volumes:
            volumes = [BoundVolume(client._client.volumes, {"id": volume}, complete=False) for volume in volumes]
            data['volumes'] = volumes

        image = data.get("image", None)
        if image is not None:
            data['image'] = BoundImage(client._client.images, image)

        iso = data.get("iso", None)
        if iso is not None:
            data['iso'] = BoundIso(client._client.isos, iso)

        server_type = data.get("server_type")
        if server_type is not None:
            data['server_type'] = BoundServerType(client._client.server_types, server_type)

        super(BoundServer, self).__init__(client, data, complete)

    def get_actions(self, status=None, sort=None):
        # type: (Optional[List[str]], Optional[List[str]]) -> List[BoundAction]
        return self._client.get_actions(self, status, sort)

    def update(self, name=None, labels=None):
        # type: (Optional[str], Optional[Dict[str, str]]) -> BoundServer
        return self._client.update(self, name, labels)

    def delete(self):
        # type: () -> BoundAction
        return self._client.delete(self)

    def power_off(self):
        # type: () -> BoundAction
        return self._client.power_off(self)

    def power_on(self):
        # type: () -> BoundAction
        return self._client.power_on(self)

    def reboot(self):
        # type: () -> BoundAction
        return self._client.reboot(self)

    def reset(self):
        # type: () -> BoundAction
        return self._client.reset(self)

    def shutdown(self):
        # type: () -> BoundAction
        return self._client.shutdown(self)

    def reset_password(self):
        # type: () -> ResetPasswordResponse
        return self._client.reset_password(self)

    def enable_rescue(self, type=None, ssh_keys=None):
        # type: (str, Optional[List[str]]) -> EnableRescueResponse
        return self._client.enable_rescue(self, type=type, ssh_keys=ssh_keys)

    def disable_rescue(self):
        # type: () -> BoundAction
        return self._client.disable_rescue(self)

    def create_image(self, description=None, type=None, labels=None):
        # type: (str, str, Optional[Dict[str, str]]) -> BoundAction
        return self._client.create_image(self, description, type, labels)

    def rebuild(self, image):
        # type: (Image) -> BoundAction
        return self._client.rebuild(self, image)

    def change_type(self, server_type, upgrade_disk):
        # type: (BoundServerType, bool) -> BoundAction
        return self._client.change_type(self, server_type, upgrade_disk)

    def enable_backup(self):
        # type: () -> BoundAction
        return self._client.enable_backup(self)

    def disable_backup(self):
        # type: () -> BoundAction
        return self._client.disable_backup(self)

    def attach_iso(self, iso):
        # type: (Iso) -> BoundAction
        return self._client.attach_iso(self, iso)

    def detach_iso(self):
        # type: () -> BoundAction
        return self._client.detach_iso(self)

    def change_dns_ptr(self, ip, dns_ptr):
        # type: (str, Optional[str]) -> BoundAction
        return self._client.change_dns_ptr(self, ip, dns_ptr)

    def change_protection(self, delete=None, rebuild=None):
        # type: (Optional[bool], Optional[bool]) -> BoundAction
        return self._client.change_protection(self, delete, rebuild)

    def request_console(self):
        # type: () -> RequestConsoleResponse
        return self._client.request_console(self)


class ServersClient(ClientEntityBase):

    def get_by_id(self, id):
        # type: (int) -> BoundServer
        response = self._client.request(url="/servers/{server_id}".format(server_id=id), method="GET")
        return BoundServer(self, response['server'])

    def get_all(self, name=None, label_selector=None):
        # type: (Optional[str], Optional[str]) -> List[BoundServer]
        params = {}
        if name:
            params['name'] = name
        if label_selector:
            params['label_selector'] = label_selector

        response = self._client.request(url="/servers", method="GET", params=params)
        return [BoundServer(self, server_data) for server_data in response['servers']]

    def create(self,
               name,                      # type: str
               server_type,               # type: str
               image,                     # type: Image
               ssh_keys=None,             # type: Optional[List[SSHKey]]
               volumes=None,              # type: Optional[List[Volume]]
               user_data=None,            # type: Optional[str]
               labels=None,               # type: Optional[Dict[str, str]]
               location=None,             # type: Optional[Location]
               datacenter=None,           # type: Optional[Datacenter]
               start_after_create=True,   # type: Optional[bool]
               automount=None             # type: Optional[bool]
               ):
        # type: (...) -> CreateServerResponse
        """
        Should be visible in docs
        :param name:
        :param server_type:
        :param image:
        :param ssh_keys:
        :param volumes:
        :param user_data:
        :param labels:
        :param location:
        :param datacenter:
        :param start_after_create:
        :return:
        """
        data = {
            'name': name,
            'server_type': server_type,
            "start_after_create": start_after_create,
            "image": image.id_or_name
        }

        if location is not None:
            data['location'] = location.id_or_name

        if datacenter is not None:
            data['datacenter'] = datacenter.id_or_name

        if ssh_keys is not None:
            data['ssh_keys'] = [str(ssh_key.id_or_name) for ssh_key in ssh_keys]
        if volumes is not None:
            data['volumes'] = [str(volume.id) for volume in volumes]
        if user_data is not None:
            data['user_data'] = user_data
        if labels is not None:
            data['labels'] = labels
        if automount is not None:
            data["automount"] = automount

        response = self._client.request(url="/servers", method="POST", json=data)

        result = CreateServerResponse(
            server=BoundServer(self, response['server']),
            action=BoundAction(self._client.actions, response['action']),
            next_actions=[BoundAction(self._client.actions, action) for action in response['next_actions']],
            root_password=response['root_password']
        )
        return result

    def get_actions(self, server, status=None, sort=None):
        # type: (Server, Optional[List[str]], Optional[List[str]]) -> List[BoundAction]
        params = {}
        if status is not None:
            params.update({"status": status})
        if sort is not None:
            params.update({"sort": sort})
        response = self._client.request(url="/servers/{server_id}/actions".format(server_id=server.id), method="GET", params=params)
        return [BoundAction(self._client.actions, action_data) for action_data in response['actions']]

    def update(self, server, name=None, labels=None):
        # type:(Server,  Optional[str],  Optional[Dict[str, str]]) -> BoundServer
        data = {}
        if name is not None:
            data.update({"name": name})
        if labels is not None:
            data.update({"labels": labels})
        response = self._client.request(url="/servers/{server_id}".format(server_id=server.id), method="PUT", json=data)
        return BoundServer(self, response['server'])

    def delete(self, server):
        # type: (Server) -> BoundAction
        response = self._client.request(url="/servers/{server_id}".format(server_id=server.id), method="DELETE")
        return BoundAction(self._client.actions, response['action'])

    def power_off(self, server):
        # type: (Server) -> Action
        response = self._client.request(url="/servers/{server_id}/actions/poweroff".format(server_id=server.id), method="POST")
        return BoundAction(self._client.actions, response['action'])

    def power_on(self, server):
        # type: (servers.domain.Server) -> actions.domain.Action
        response = self._client.request(url="/servers/{server_id}/actions/poweron".format(server_id=server.id), method="POST")
        return BoundAction(self._client.actions, response['action'])

    def reboot(self, server):
        # type: (servers.domain.Server) -> actions.domain.Action
        response = self._client.request(url="/servers/{server_id}/actions/reboot".format(server_id=server.id), method="POST")
        return BoundAction(self._client.actions, response['action'])

    def reset(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        response = self._client.request(url="/servers/{server_id}/actions/reset".format(server_id=server.id), method="POST")
        return BoundAction(self._client.actions, response['action'])

    def shutdown(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        response = self._client.request(url="/servers/{server_id}/actions/shutdown".format(server_id=server.id), method="POST")
        return BoundAction(self._client.actions, response['action'])

    def reset_password(self, server):
        # type: (servers.domain.Server) -> ResetPasswordResponse
        response = self._client.request(url="/servers/{server_id}/actions/reset_password".format(server_id=server.id), method="POST")
        return ResetPasswordResponse(action=BoundAction(self._client.actions, response['action']), root_password=response['root_password'])

    def change_type(self, server, server_type, upgrade_disk):
        # type: (servers.domain.Server, BoundServerType, bool) -> actions.domainAction

        data = {
            "server_type": server_type.id_or_name,
            "upgrade_disk": upgrade_disk
        }
        response = self._client.request(url="/servers/{server_id}/actions/change_type".format(server_id=server.id), method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])

    def enable_rescue(self, server, type=None, ssh_keys=None):
        # type: (servers.domain.Server, str, Optional[List[str]]) -> EnableRescueResponse

        data = {
            "type": type
        }
        if ssh_keys is not None:
            data.update({"ssh_keys": ssh_keys})

        response = self._client.request(url="/servers/{server_id}/actions/enable_rescue".format(server_id=server.id), method="POST", json=data)
        return EnableRescueResponse(action=BoundAction(self._client.actions, response['action']), root_password=response['root_password'])

    def disable_rescue(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        response = self._client.request(url="/servers/{server_id}/actions/disable_rescue".format(server_id=server.id), method="POST")
        return BoundAction(self._client.actions, response['action'])

    def create_image(self, server, description=None, type=None, labels=None):
        # type: (servers.domain.Server, str, str, Optional[Dict[str, str]]) -> CreateImageResponse

        data = {}
        if description is not None:
            data.update({"description": description})

        if type is not None:
            data.update({"type": type})

        if labels is not None:
            data.update({"type": labels})

        response = self._client.request(url="/servers/{server_id}/actions/create_image".format(server_id=server.id), method="POST", json=data)
        return CreateImageResponse(action=BoundAction(self._client.actions, response['action']), image=BoundImage(self._client.images, response['image']))

    def rebuild(self, server, image):
        # type: (servers.domain.Server, Image) -> actions.domainAction

        data = {
            "image": image.id_or_name
        }
        response = self._client.request(url="/servers/{server_id}/actions/rebuild".format(server_id=server.id), method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])

    def enable_backup(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        response = self._client.request(url="/servers/{server_id}/actions/enable_backup".format(server_id=server.id), method="POST")
        return BoundAction(self._client.actions, response['action'])

    def disable_backup(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        response = self._client.request(url="/servers/{server_id}/actions/disable_backup".format(server_id=server.id), method="POST")
        return BoundAction(self._client.actions, response['action'])

    def attach_iso(self, server, iso):
        # type: (servers.domain.Server, Iso) -> actions.domainAction
        data = {
            "iso": iso.id_or_name
        }
        response = self._client.request(url="/servers/{server_id}/actions/attach_iso".format(server_id=server.id), method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])

    def detach_iso(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        response = self._client.request(url="/servers/{server_id}/actions/detach_iso".format(server_id=server.id), method="POST")
        return BoundAction(self._client.actions, response['action'])

    def change_dns_ptr(self, server, ip, dns_ptr):
        # type: (servers.domain.Server, str, Optional[str]) -> actions.domainAction
        data = {
            "ip": ip,
            "dns_ptr": dns_ptr
        }
        response = self._client.request(url="/servers/{server_id}/actions/change_dns_ptr".format(server_id=server.id), method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])

    def change_protection(self, server, delete=None, rebuild=None):
        # type: (servers.domain.Server, Optional[bool], Optional[bool]) -> actions.domainAction
        data = {}
        if delete is not None:
            data.update({"delete": delete})
        if rebuild is not None:
            data.update({"rebuild": rebuild})

        response = self._client.request(url="/servers/{server_id}/actions/change_protection".format(server_id=server.id), method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])

    def request_console(self, server):
        # type: (servers.domain.Server) -> RequestConsoleResponse
        response = self._client.request(url="/servers/{server_id}/actions/request_console".format(server_id=server.id), method="POST")
        return RequestConsoleResponse(action=BoundAction(self._client.actions, response['action']), wss_url=response['wss_url'], password=response['password'])
