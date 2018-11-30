# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase

from hcloud.actions.domain import Action
from hcloud.servers.domain import Server, CreateServerResponse, ResetPasswordResponse, EnableRescueResponse, RequestConsoleResponse
from hcloud.volumes.client import BoundVolume
from hcloud.images.domain import Image, CreateImageResponse
from hcloud.iso.domain import Iso


class BoundServer(BoundModelBase):
    model = Server

    def __init__(self, client, data):
        volumes = data.get('volumes', [])
        if volumes:
            volumes = [BoundVolume(client._client.volumes, {"id": volume}, complete=False) for volume in volumes]
            data['volumes'] = volumes

        image = data.get("image", None)
        if image is not None:
            # data['image'] = BoundImage(client._client.images, image, complete=True) # When Image Client is implemented
            data['image'] = Image(**image)
            print(data['image'].id)

        iso = data.get("iso", None)
        if iso is not None:
            # data['iso'] = BoundIso(client._client.iso, iso, complete=True) # When ISO Client is implemented
            data['iso'] = Iso(**iso)

        super(BoundServer, self).__init__(client, data)

    def get_actions(self, status=None, sort=None):
        # type: # type: (Optional[List[str], Optional[List[str]]) -> List[Action]
        return self._client.get_actions(self, status, sort)

    def update(self, name=None, labels=None):
        # type: (Optional[str], Optional[Dict[str, str]]) -> BoundServer
        return self._client.update(self, name, labels)

    def delete(self):
        # type: () -> Action
        return self._client.delete(self)

    def power_off(self):
        # type: () -> Action
        return self._client.power_off(self)

    def power_on(self):
        # type: () -> Action
        return self._client.power_on(self)

    def reboot(self):
        # type: () -> Action
        return self._client.reboot(self)

    def reset(self):
        # type: () -> Action
        return self._client.reset(self)

    def shutdown(self):
        # type: () -> Action
        return self._client.shutdown(self)

    def reset_password(self):
        # type: () -> ResetPasswordResponse
        return self._client.reset_password(self)

    def enable_rescue(self, type=None, ssh_keys=None):
        # type: (str, Optional[List[str]]) -> EnableRescueResponse
        return self._client.enable_rescue(self, type=type, ssh_keys=ssh_keys)

    def disable_rescue(self):
        # type: () -> Action
        return self._client.disable_rescue(self)

    def create_image(self, description=None, type=None, labels=None):
        # type: (str, str, Optional[Dict[str, str]]) -> Action
        return self._client.create_image(self, description, type, labels)

    def rebuild(self, image):
        # type: (Image) -> Action
        return self._client.rebuild(self, image)

    def change_type(self):
        # type: () -> Action
        # TODO: Add Parameter upgrade_disk, server_type (required)
        return self._client.change_type(self)

    def enable_backup(self):
        # type: () -> Action
        return self._client.enable_backup(self)

    def disable_backup(self):
        # type: () -> Action
        return self._client.disable_backup(self)

    def attach_iso(self, iso):
        # type: (Iso) -> Action
        return self._client.attach_iso(self, iso)

    def detach_iso(self):
        # type: () -> Action
        return self._client.detach_iso(self)

    def change_dns_ptr(self, ip, dns_ptr):
        # type: (str, Optional[str]) -> Action
        return self._client.change_dns_ptr(self, ip, dns_ptr)

    def change_protection(self, delete=None, rebuild=None):
        # type: (Optional[bool],Optional[bool]) -> Action
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
               name,                     # type: str
               server_type,              # type: str
               image,                    # type: Image
               ssh_keys=None,            # type: Optional[List[str]]
               volumes=None,             # type: Optional[List[Volume]]
               user_data=None,           # type: Optional[str]
               labels=None,              # type: Optional[Dict[str, str]]
               location=None,            # type: Optional[str]
               datacenter=None,          # type: Optional[str]
               start_after_create=True   # type: Optional[bool]
               ):
        # type: (...) -> CreateServerResponse
        # TODO: convert location str type to locations.domain.Location type, when implementation is ready
        # TODO: convert datacenter str type to datacenters.domain.Datacenter type, when implementation is ready
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
            "start_after_create": start_after_create
        }
        if image.id is not None:
            data['image'] = image.id
        else:
            data['image'] = image.name

        if ssh_keys is not None:
            data['ssh_keys'] = ssh_keys
        if volumes is not None:
            data['volumes'] = [str(volume.id) for volume in volumes]
        if user_data is not None:
            data['user_data'] = user_data
        if labels is not None:
            data['labels'] = labels
        if location is not None:
            data['location'] = location
        if datacenter is not None:
            data["datacenter"] = datacenter

        response = self._client.request(url="/servers", method="POST", json=data)

        result = CreateServerResponse(
            server=BoundServer(self, response['server']),
            action=Action(**response['action']),
            next_actions=[Action(**action) for action in response['next_actions']],
            root_password=response['root_password']
        )
        return result

    def get_actions(self, server, status=None, sort=None):
        # type: (Server, Optional[List[str]], Optional[List[str]]) -> List[Action]
        params = {}
        if status is not None:
            params.update({"status": status})
        if sort is not None:
            params.update({"sort": sort})
        response = self._client.request(url="/servers/{server_id}/actions".format(server_id=server.id), method="GET", params=params)
        return [Action(**action_data) for action_data in response['actions']]

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
        # type: (Server) -> Action
        response = self._client.request(url="/servers/{server_id}".format(server_id=server.id), method="DELETE")
        return Action(**response['action'])

    def power_off(self, server):
        # type: (Server) -> Action
        response = self._client.request(url="/servers/{server_id}/actions/poweroff".format(server_id=server.id), method="POST")
        return Action(**response['action'])

    def power_on(self, server):
        # type: (servers.domain.Server) -> actions.domain.Action
        response = self._client.request(url="/servers/{server_id}/actions/poweron".format(server_id=server.id), method="POST")
        return Action(**response['action'])

    def reboot(self, server):
        # type: (servers.domain.Server) -> actions.domain.Action
        response = self._client.request(url="/servers/{server_id}/actions/reboot".format(server_id=server.id), method="POST")
        return Action(**response['action'])

    def reset(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        response = self._client.request(url="/servers/{server_id}/actions/reset".format(server_id=server.id), method="POST")
        return Action(**response['action'])

    def shutdown(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        response = self._client.request(url="/servers/{server_id}/actions/shutdown".format(server_id=server.id), method="POST")
        return Action(**response['action'])

    def reset_password(self, server):
        # type: (servers.domain.Server) -> ResetPasswordResponse
        response = self._client.request(url="/servers/{server_id}/actions/reset_password".format(server_id=server.id), method="POST")
        return ResetPasswordResponse(action=Action(**response['action']), root_password=response['root_password'])

    def enable_rescue(self, server, type=None, ssh_keys=None):
        # type: (servers.domain.Server, str, Optional[List[str]]) -> EnableRescueResponse

        data = {
            "type": type
        }
        if ssh_keys is not None:
            data.update({"ssh_keys": ssh_keys})

        response = self._client.request(url="/servers/{server_id}/actions/enable_rescue".format(server_id=server.id), method="POST", json=data)
        return EnableRescueResponse(action=Action(**response['action']), root_password=response['root_password'])

    def disable_rescue(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        response = self._client.request(url="/servers/{server_id}/actions/disable_rescue".format(server_id=server.id), method="POST")
        return Action(**response['action'])

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
        return CreateImageResponse(action=Action(**response['action']), image=Image(**response['image']))

    def rebuild(self, server, image):
        # type: (servers.domain.Server, Image) -> actions.domainAction
        if image.id is None:
            data = {
                "image": image.name
            }
        else:
            data = {
                "image": image.id
            }

        response = self._client.request(url="/servers/{server_id}/actions/rebuild".format(server_id=server.id), method="POST", json=data)
        return Action(**response['action'])

    def enable_backup(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        response = self._client.request(url="/servers/{server_id}/actions/enable_backup".format(server_id=server.id), method="POST")
        return Action(**response['action'])

    def disable_backup(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        response = self._client.request(url="/servers/{server_id}/actions/disable_backup".format(server_id=server.id), method="POST")
        return Action(**response['action'])

    def attach_iso(self, server, iso):
        # type: (servers.domain.Server, Iso) -> actions.domainAction
        if iso.id is None:
            data = {
                "iso": iso.name
            }
        else:
            data = {
                "iso": iso.id
            }
        response = self._client.request(url="/servers/{server_id}/actions/attach_iso".format(server_id=server.id), method="POST", json=data)
        return Action(**response['action'])

    def detach_iso(self, server):
        # type: (servers.domain.Server) -> actions.domainAction
        response = self._client.request(url="/servers/{server_id}/actions/detach_iso".format(server_id=server.id), method="POST")
        return Action(**response['action'])

    def change_dns_ptr(self, server, ip, dns_ptr):
        # type: (servers.domain.Server, str, Optional[str]) -> actions.domainAction
        data = {
            "ip": ip,
            "dns_ptr": dns_ptr
        }
        response = self._client.request(url="/servers/{server_id}/actions/change_dns_ptr".format(server_id=server.id), method="POST", json=data)
        return Action(**response['action'])

    def change_protection(self, server, delete=None, rebuild=None):
        # type: (servers.domain.Server, Optional[bool], Optional[bool]) -> actions.domainAction
        data = {}
        if delete is not None:
            data.update({"delete": delete})
        if rebuild is not None:
            data.update({"rebuild": rebuild})

        response = self._client.request(url="/servers/{server_id}/actions/change_protection".format(server_id=server.id), method="POST", json=data)
        return Action(**response['action'])

    def request_console(self, server):
        # type: (servers.domain.Server) -> RequestConsoleResponse
        response = self._client.request(url="/servers/{server_id}/actions/request_console".format(server_id=server.id), method="POST")
        return RequestConsoleResponse(action=Action(**response['action']), wss_url=response['wss_url'], password=response['password'])
