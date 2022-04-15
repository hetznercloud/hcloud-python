from hcloud.actions.client import BoundAction
from hcloud.core.client import BoundModelBase, ClientEntityBase, GetEntityByNameMixin
from hcloud.core.domain import add_meta_to_result

from hcloud.floating_ips.domain import FloatingIP, CreateFloatingIPResponse
from hcloud.locations.client import BoundLocation


class BoundFloatingIP(BoundModelBase):
    model = FloatingIP

    def __init__(self, client, data, complete=True):
        from hcloud.servers.client import BoundServer

        server = data.get("server")
        if server is not None:
            data["server"] = BoundServer(
                client._client.servers, {"id": server}, complete=False
            )

        home_location = data.get("home_location")
        if home_location is not None:
            data["home_location"] = BoundLocation(
                client._client.locations, home_location
            )

        super(BoundFloatingIP, self).__init__(client, data, complete)

    def get_actions_list(self, status=None, sort=None, page=None, per_page=None):
        # type: (Optional[List[str]], Optional[List[str]], Optional[int], Optional[int]) -> PageResult[BoundAction, Meta]
        """Returns all action objects for a Floating IP.

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
        # type: (Optional[List[str]]) -> List[BoundAction]
        """Returns all action objects for a Floating IP.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`

        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.get_actions(self, status, sort)

    def update(self, description=None, labels=None, name=None):
        # type: (Optional[str], Optional[Dict[str, str]], Optional[str]) -> BoundFloatingIP
        """Updates the description or labels of a Floating IP.

        :param description: str (optional)
               New Description to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str (optional)
               New Name to set
        :return: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`
        """
        return self._client.update(self, description, labels, name)

    def delete(self):
        # type: () -> bool
        """Deletes a Floating IP. If it is currently assigned to a server it will automatically get unassigned.

        :return: boolean
        """
        return self._client.delete(self)

    def change_protection(self, delete=None):
        # type: (Optional[bool]) -> BoundAction
        """Changes the protection configuration of the Floating IP.

        :param delete: boolean
               If true, prevents the Floating IP from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_protection(self, delete)

    def assign(self, server):
        # type: (Server) -> BoundAction
        """Assigns a Floating IP to a server.

        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or  :class:`Server <hcloud.servers.domain.Server>`
               Server the Floating IP shall be assigned to
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.assign(self, server)

    def unassign(self):
        # type: () -> BoundAction
        """Unassigns a Floating IP, resulting in it being unreachable. You may assign it to a server again at a later time.

        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.unassign(self)

    def change_dns_ptr(self, ip, dns_ptr):
        # type: (str, str) -> BoundAction
        """Changes the hostname that will appear when getting the hostname belonging to this Floating IP.

        :param ip: str
               The IP address for which to set the reverse DNS entry
        :param dns_ptr: str
               Hostname to set as a reverse DNS PTR entry, will reset to original default value if `None`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_dns_ptr(self, ip, dns_ptr)


class FloatingIPsClient(ClientEntityBase, GetEntityByNameMixin):
    results_list_attribute_name = "floating_ips"

    def get_actions_list(
        self,
        floating_ip,  # type: FloatingIP
        status=None,  # type: Optional[List[str]]
        sort=None,  # type: Optional[List[str]]
        page=None,  # type: Optional[int]
        per_page=None,  # type: Optional[int]
    ):
        # type: (...) -> PageResults[List[BoundAction], Meta]
        """Returns all action objects for a Floating IP.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
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
            url="/floating_ips/{floating_ip_id}/actions".format(
                floating_ip_id=floating_ip.id
            ),
            method="GET",
            params=params,
        )
        actions = [
            BoundAction(self._client.actions, action_data)
            for action_data in response["actions"]
        ]
        return add_meta_to_result(actions, response, "actions")

    def get_actions(
        self,
        floating_ip,  # type: FloatingIP
        status=None,  # type: Optional[List[str]]
        sort=None,  # type: Optional[List[str]]
    ):
        # type: (...) -> List[BoundAction]
        """Returns all action objects for a Floating IP.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`

        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return super(FloatingIPsClient, self).get_actions(
            floating_ip, status=status, sort=sort
        )

    def get_by_id(self, id):
        # type: (int) -> BoundFloatingIP
        """Returns a specific Floating IP object.

        :param id: int
        :return: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`
        """
        response = self._client.request(
            url="/floating_ips/{floating_ip_id}".format(floating_ip_id=id), method="GET"
        )
        return BoundFloatingIP(self, response["floating_ip"])

    def get_list(
        self,
        label_selector=None,  # type: Optional[str]
        page=None,  # type: Optional[int]
        per_page=None,  # type: Optional[int]
        name=None,  # type: Optional[str]
    ):
        # type: (...) -> PageResults[List[BoundFloatingIP]]
        """Get a list of floating ips from this account

        :param label_selector: str (optional)
               Can be used to filter Floating IPs by labels. The response will only contain Floating IPs matching the label selector.able values.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :param name: str (optional)
               Can be used to filter networks by their name.
        :return: (List[:class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params = {}

        if label_selector is not None:
            params["label_selector"] = label_selector
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if name is not None:
            params["name"] = name

        response = self._client.request(
            url="/floating_ips", method="GET", params=params
        )
        floating_ips = [
            BoundFloatingIP(self, floating_ip_data)
            for floating_ip_data in response["floating_ips"]
        ]

        return self._add_meta_to_result(floating_ips, response)

    def get_all(self, label_selector=None, name=None):
        # type: (Optional[str], Optional[str]) -> List[BoundFloatingIP]
        """Get all floating ips from this account

        :param label_selector: str (optional)
               Can be used to filter Floating IPs by labels. The response will only contain Floating IPs matching the label selector.able values.
        :param name: str (optional)
               Can be used to filter networks by their name.
        :return: List[:class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`]
        """
        return super(FloatingIPsClient, self).get_all(
            label_selector=label_selector, name=name
        )

    def get_by_name(self, name):
        # type: (str) -> BoundFloatingIP
        """Get Floating IP by name

        :param name: str
               Used to get Floating IP by name.
        :return: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`
        """
        return super(FloatingIPsClient, self).get_by_name(name)

    def create(
        self,
        type,  # type: str
        description=None,  # type: Optional[str]
        labels=None,  # type: Optional[str]
        home_location=None,  # type: Optional[Location]
        server=None,  # type: Optional[Server]
        name=None,  # type: Optional[str]
    ):
        # type: (...) -> CreateFloatingIPResponse
        """Creates a new Floating IP assigned to a server.

        :param type: str
               Floating IP type Choices: ipv4, ipv6
        :param description: str (optional)
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param home_location: :class:`BoundLocation <hcloud.locations.client.BoundLocation>` or :class:`Location <hcloud.locations.domain.Location>` (
               Home location (routing is optimized for that location). Only optional if server argument is passed.
        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or  :class:`Server <hcloud.servers.domain.Server>`
               Server to assign the Floating IP to
        :param name: str (optional)
        :return: :class:`CreateFloatingIPResponse <hcloud.floating_ips.domain.CreateFloatingIPResponse>`
        """

        data = {"type": type}
        if description is not None:
            data["description"] = description
        if labels is not None:
            data["labels"] = labels
        if home_location is not None:
            data["home_location"] = home_location.id_or_name
        if server is not None:
            data["server"] = server.id
        if name is not None:
            data["name"] = name

        response = self._client.request(url="/floating_ips", json=data, method="POST")

        action = None
        if response.get("action") is not None:
            action = BoundAction(self._client.actions, response["action"])

        result = CreateFloatingIPResponse(
            floating_ip=BoundFloatingIP(self, response["floating_ip"]), action=action
        )
        return result

    def update(self, floating_ip, description=None, labels=None, name=None):
        # type: (FloatingIP,  Optional[str], Optional[Dict[str, str]], Optional[str]) -> BoundFloatingIP
        """Updates the description or labels of a Floating IP.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
        :param description: str (optional)
               New Description to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str (optional)
               New name to set
        :return: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>`
        """
        data = {}
        if description is not None:
            data["description"] = description
        if labels is not None:
            data["labels"] = labels
        if name is not None:
            data["name"] = name

        response = self._client.request(
            url="/floating_ips/{floating_ip_id}".format(floating_ip_id=floating_ip.id),
            method="PUT",
            json=data,
        )
        return BoundFloatingIP(self, response["floating_ip"])

    def delete(self, floating_ip):
        # type: (FloatingIP) -> bool
        """Deletes a Floating IP. If it is currently assigned to a server it will automatically get unassigned.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
        :return: boolean
        """
        self._client.request(
            url="/floating_ips/{floating_ip_id}".format(floating_ip_id=floating_ip.id),
            method="DELETE",
        )
        # Return always true, because the API does not return an action for it. When an error occurs a HcloudAPIException will be raised
        return True

    def change_protection(self, floating_ip, delete=None):
        # type: (FloatingIP, Optional[bool]) -> BoundAction
        """Changes the protection configuration of the Floating IP.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
        :param delete: boolean
               If true, prevents the Floating IP from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {}
        if delete is not None:
            data.update({"delete": delete})

        response = self._client.request(
            url="/floating_ips/{floating_ip_id}/actions/change_protection".format(
                floating_ip_id=floating_ip.id
            ),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def assign(self, floating_ip, server):
        # type: (FloatingIP, Server) -> BoundAction
        """Assigns a Floating IP to a server.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
        :param server: :class:`BoundServer <hcloud.servers.client.BoundServer>` or  :class:`Server <hcloud.servers.domain.Server>`
               Server the Floating IP shall be assigned to
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/floating_ips/{floating_ip_id}/actions/assign".format(
                floating_ip_id=floating_ip.id
            ),
            method="POST",
            json={"server": server.id},
        )
        return BoundAction(self._client.actions, response["action"])

    def unassign(self, floating_ip):
        # type: (FloatingIP) -> BoundAction
        """Unassigns a Floating IP, resulting in it being unreachable. You may assign it to a server again at a later time.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/floating_ips/{floating_ip_id}/actions/unassign".format(
                floating_ip_id=floating_ip.id
            ),
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def change_dns_ptr(self, floating_ip, ip, dns_ptr):
        # type: (FloatingIP, str, str) -> BoundAction
        """Changes the hostname that will appear when getting the hostname belonging to this Floating IP.

        :param floating_ip: :class:`BoundFloatingIP <hcloud.floating_ips.client.BoundFloatingIP>` or  :class:`FloatingIP <hcloud.floating_ips.domain.FloatingIP>`
        :param ip: str
               The IP address for which to set the reverse DNS entry
        :param dns_ptr: str
               Hostname to set as a reverse DNS PTR entry, will reset to original default value if `None`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/floating_ips/{floating_ip_id}/actions/change_dns_ptr".format(
                floating_ip_id=floating_ip.id
            ),
            method="POST",
            json={"ip": ip, "dns_ptr": dns_ptr},
        )
        return BoundAction(self._client.actions, response["action"])
