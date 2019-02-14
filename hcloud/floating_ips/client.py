# -*- coding: utf-8 -*-
from hcloud.actions.client import BoundAction
from hcloud.core.client import BoundModelBase, ClientEntityBase
from hcloud.core.domain import add_meta_to_result

from hcloud.floating_ips.domain import FloatingIP, CreateFloatingIPResponse
from hcloud.locations.client import BoundLocation


class BoundFloatingIP(BoundModelBase):
    model = FloatingIP

    def __init__(self, client, data, complete=True):
        from hcloud.servers.client import BoundServer
        server = data.get("server")
        if server is not None:
            data['server'] = BoundServer(client._client.servers, {"id": server}, complete=False)

        home_location = data.get("home_location")
        if home_location is not None:
            data['home_location'] = BoundLocation(client._client.locations, home_location)

        super(BoundFloatingIP, self).__init__(client, data, complete)

    def get_actions_list(self, sort=None, page=None, per_page=None):
        # type: (Optional[List[str]], Optional[int], Optional[int]) -> PageResult[BoundAction, Meta]
        return self._client.get_actions_list(self, sort, page, per_page)

    def get_actions(self, sort=None):
        # type: (Optional[List[str]]) -> List[BoundAction]
        return self._client.get_actions(self, sort)

    def update(self, description=None, labels=None):
        # type: (Optional[str], Optional[Dict[str, str]]) -> BoundFloatingIP
        return self._client.update(self, description, labels)

    def delete(self):
        # type: () -> bool
        return self._client.delete(self)

    def change_protection(self, delete=None):
        # type: (Optional[bool]) -> BoundAction
        return self._client.change_protection(self, delete)

    def assign(self, server):
        # type: (Server) -> BoundAction
        return self._client.assign(self, server)

    def unassign(self):
        # type: () -> BoundAction
        return self._client.unassign(self)

    def change_dns_ptr(self, ip, dns_ptr):
        # type: (str, str) -> BoundAction
        return self._client.change_dns_ptr(self, ip, dns_ptr)


class FloatingIPsClient(ClientEntityBase):
    results_list_attribute_name = 'floating_ips'

    def get_actions_list(self,
                         floating_ip,         # type: FloatingIP
                         sort=None,     # type: Optional[List[str]]
                         page=None,     # type: Optional[int]
                         per_page=None  # type: Optional[int]
                         ):
        # type: (...) -> PageResults[List[BoundAction], Meta]
        params = {}
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        response = self._client.request(url="/floating_ips/{floating_ip_id}/actions".format(floating_ip_id=floating_ip.id), method="GET", params=params)
        actions = [BoundAction(self._client.actions, action_data) for action_data in response['actions']]
        return add_meta_to_result(actions, response, 'actions')

    def get_actions(self,
                    floating_ip,   # type: FloatingIP
                    sort=None,     # type: Optional[List[str]]
                    ):
        # type: (...) -> List[BoundAction]
        return super(FloatingIPsClient, self).get_actions(floating_ip, sort=sort)

    def get_by_id(self, id):
        # type: (int) -> BoundFloatingIP
        response = self._client.request(url="/floating_ips/{floating_ip_id}".format(floating_ip_id=id), method="GET")
        return BoundFloatingIP(self, response['floating_ip'])

    def get_list(self,
                 label_selector=None,  # type: Optional[str]
                 page=None,            # type: Optional[int]
                 per_page=None         # type: Optional[int]
                 ):
        # type: (...) -> PageResults[List[BoundFloatingIP]]
        params = {}

        if label_selector:
            params['label_selector'] = label_selector
        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page

        response = self._client.request(url="/floating_ips", method="GET", params=params)
        floating_ips = [BoundFloatingIP(self, floating_ip_data) for floating_ip_data in response['floating_ips']]

        return self.add_meta_to_result(floating_ips, response)

    def get_all(self, label_selector=None):
        # type: (Optional[str]) -> List[BoundFloatingIP]
        return super(FloatingIPsClient, self).get_all(label_selector=label_selector)

    def create(self,
               type,                # type: str
               description=None,    # type: Optional[str]
               labels=None,         # type: Optional[str]
               home_location=None,  # type: Optional[Location]
               server=None,         # type: Optional[Server]
               ):
        # type: (...) -> CreateFloatingIPResponse

        data = {
            'type': type
        }
        if description is not None:
            data['description'] = description
        if labels is not None:
            data['labels'] = labels
        if home_location is not None:
            data['home_location'] = home_location.id_or_name
        if server is not None:
            data['server'] = server.id

        response = self._client.request(url="/floating_ips", json=data, method="POST")

        result = CreateFloatingIPResponse(
            floating_ip=BoundFloatingIP(self, response['floating_ip']),
            action=BoundAction(self._client.actions, response['action'])
        )
        return result

    def update(self, floating_ip, description=None, labels=None):
        # type: (FloatingIP,  Optional[str], Optional[Dict[str, str]]) -> BoundFloatingIP
        data = {}
        if description is not None:
            data['description'] = description
        if labels is not None:
            data['labels'] = labels

        response = self._client.request(url="/floating_ips/{floating_ip_id}".format(floating_ip_id=floating_ip.id), method="PUT", json=data)
        return BoundFloatingIP(self, response['floating_ip'])

    def delete(self, floating_ip):
        # type: (FloatingIP) -> bool
        self._client.request(url="/floating_ips/{floating_ip_id}".format(floating_ip_id=floating_ip.id), method="DELETE")
        # Return allays true, because the API does not return an action for it. When an error occurs a HcloudAPIException will be raised
        return True

    def change_protection(self, floating_ip, delete=None):
        # type: (FloatingIP, Optional[bool], Optional[bool]) -> BoundAction
        data = {}
        if delete is not None:
            data.update({"delete": delete})

        response = self._client.request(url="/floating_ips/{floating_ip_id}/actions/change_protection".format(floating_ip_id=floating_ip.id), method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])

    def assign(self, floating_ip, server):
        # type: (FloatingIP, Server) -> BoundAction
        response = self._client.request(url="/floating_ips/{floating_ip_id}/actions/assign".format(floating_ip_id=floating_ip.id), method="POST", json={"server": server.id})
        return BoundAction(self._client.actions, response['action'])

    def unassign(self, floating_ip):
        # type: (FloatingIP) -> BoundAction
        response = self._client.request(url="/floating_ips/{floating_ip_id}/actions/unassign".format(floating_ip_id=floating_ip.id), method="POST")
        return BoundAction(self._client.actions, response['action'])

    def change_dns_ptr(self, floating_ip, ip, dns_ptr):
        # type: (FloatingIP, str, str) -> BoundAction
        response = self._client.request(url="/floating_ips/{floating_ip_id}/actions/change_dns_ptr".format(floating_ip_id=floating_ip.id), method="POST", json={"ip": ip, "dns_ptr": dns_ptr})
        return BoundAction(self._client.actions, response['action'])
