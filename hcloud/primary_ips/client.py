from ..actions.client import BoundAction
from ..core.client import BoundModelBase, ClientEntityBase, GetEntityByNameMixin
from .domain import CreatePrimaryIPResponse, PrimaryIP


class BoundPrimaryIP(BoundModelBase):
    model = PrimaryIP

    def __init__(self, client, data, complete=True):
        from ..datacenters.client import BoundDatacenter

        datacenter = data.get("datacenter", {})
        if datacenter:
            data["datacenter"] = BoundDatacenter(client._client.datacenters, datacenter)

        super().__init__(client, data, complete)

    def update(self, auto_delete=None, labels=None, name=None):
        # type: (Optional[bool], Optional[Dict[str, str]], Optional[str]) -> BoundPrimaryIP
        """Updates the description or labels of a Primary IP.

        :param auto_delete: bool (optional)
               Auto delete IP when assignee gets deleted
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str (optional)
               New Name to set
        :return: :class:`BoundPrimaryIP <hcloud.primary_ips.client.BoundPrimaryIP>`
        """
        return self._client.update(
            self, auto_delete=auto_delete, labels=labels, name=name
        )

    def delete(self):
        # type: () -> bool
        """Deletes a Primary IP. If it is currently assigned to a server it will automatically get unassigned.

        :return: boolean
        """
        return self._client.delete(self)

    def change_protection(self, delete=None):
        # type: (Optional[bool]) -> BoundAction
        """Changes the protection configuration of the Primary IP.

        :param delete: boolean
               If true, prevents the Primary IP from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_protection(self, delete)

    def assign(self, assignee_id, assignee_type):
        # type: (int,str) -> BoundAction
        """Assigns a Primary IP to a assignee.

        :param assignee_id: int`
               Id of an assignee the Primary IP shall be assigned to
        :param assignee_type: string`
               Assignee type (e.g server) the Primary IP shall be assigned to
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.assign(self, assignee_id, assignee_type)

    def unassign(self):
        # type: () -> BoundAction
        """Unassigns a Primary IP, resulting in it being unreachable. You may assign it to a server again at a later time.

        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.unassign(self)

    def change_dns_ptr(self, ip, dns_ptr):
        # type: (str, str) -> BoundAction
        """Changes the hostname that will appear when getting the hostname belonging to this Primary IP.

        :param ip: str
               The IP address for which to set the reverse DNS entry
        :param dns_ptr: str
               Hostname to set as a reverse DNS PTR entry, will reset to original default value if `None`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_dns_ptr(self, ip, dns_ptr)


class PrimaryIPsClient(ClientEntityBase, GetEntityByNameMixin):
    results_list_attribute_name = "primary_ips"

    def get_by_id(self, id):
        # type: (int) -> BoundPrimaryIP
        """Returns a specific Primary IP object.

        :param id: int
        :return: :class:`BoundPrimaryIP <hcloud.primary_ips.client.BoundPrimaryIP>`
        """
        response = self._client.request(url=f"/primary_ips/{id}", method="GET")
        return BoundPrimaryIP(self, response["primary_ip"])

    def get_list(
        self,
        label_selector=None,  # type: Optional[str]
        page=None,  # type: Optional[int]
        per_page=None,  # type: Optional[int]
        name=None,  # type: Optional[str]
        ip=None,  # type: Optional[ip]
    ):
        # type: (...) -> PageResults[List[BoundPrimaryIP]]
        """Get a list of primary ips from this account

        :param label_selector: str (optional)
               Can be used to filter Primary IPs by labels. The response will only contain Primary IPs matching the label selectorable values.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :param name: str (optional)
               Can be used to filter networks by their name.
        :param ip: str (optional)
               Can be used to filter resources by their ip. The response will only contain the resources matching the specified ip.
        :return: (List[:class:`BoundPrimaryIP <hcloud.primary_ips.client.BoundPrimaryIP>`], :class:`Meta <hcloud.core.domain.Meta>`)
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
        if ip is not None:
            params["ip"] = ip

        response = self._client.request(url="/primary_ips", method="GET", params=params)
        primary_ips = [
            BoundPrimaryIP(self, primary_ip_data)
            for primary_ip_data in response["primary_ips"]
        ]

        return self._add_meta_to_result(primary_ips, response)

    def get_all(self, label_selector=None, name=None):
        # type: (Optional[str], Optional[str]) -> List[BoundPrimaryIP]
        """Get all primary ips from this account

        :param label_selector: str (optional)
               Can be used to filter Primary IPs by labels. The response will only contain Primary IPs matching the label selector.able values.
        :param name: str (optional)
               Can be used to filter networks by their name.
        :return: List[:class:`BoundPrimaryIP <hcloud.primary_ips.client.BoundPrimaryIP>`]
        """
        return super().get_all(label_selector=label_selector, name=name)

    def get_by_name(self, name):
        # type: (str) -> BoundPrimaryIP
        """Get Primary IP by name

        :param name: str
               Used to get Primary IP by name.
        :return: :class:`BoundPrimaryIP <hcloud.primary_ips.client.BoundPrimaryIP>`
        """
        return super().get_by_name(name)

    def create(
        self,
        type,  # type: str
        datacenter,  # type: Datacenter
        name,  # type: str
        assignee_type="server",  # type: Optional[str]
        assignee_id=None,  # type: Optional[int]
        auto_delete=False,  # type: Optional[bool]
        labels=None,  # type: Optional[dict]
    ):
        # type: (...) -> CreatePrimaryIPResponse
        """Creates a new Primary IP assigned to a server.

        :param type: str
               Primary IP type Choices: ipv4, ipv6
        :param assignee_type: str
        :param assignee_id: int (optional)
        :param datacenter: Datacenter
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str
        :param auto_delete: bool (optional)
        :return: :class:`CreatePrimaryIPResponse <hcloud.primary_ips.domain.CreatePrimaryIPResponse>`
        """

        data = {
            "type": type,
            "assignee_type": assignee_type,
            "auto_delete": auto_delete,
            "datacenter": datacenter.id_or_name,
            "name": name,
        }
        if assignee_id:
            data["assignee_id"] = assignee_id
        if labels is not None:
            data["labels"] = labels

        response = self._client.request(url="/primary_ips", json=data, method="POST")

        action = None
        if response.get("action") is not None:
            action = BoundAction(self._client.actions, response["action"])

        result = CreatePrimaryIPResponse(
            primary_ip=BoundPrimaryIP(self, response["primary_ip"]), action=action
        )
        return result

    def update(self, primary_ip, auto_delete=None, labels=None, name=None):
        # type: (PrimaryIP,  Optional[bool], Optional[Dict[str, str]], Optional[str]) -> BoundPrimaryIP
        """Updates the name, auto_delete or labels of a Primary IP.

        :param primary_ip: :class:`BoundPrimaryIP <hcloud.primary_ips.client.BoundPrimaryIP>` or  :class:`PrimaryIP <hcloud.primary_ips.domain.PrimaryIP>`
        :param auto_delete: bool (optional)
               Delete this Primary IP when the resource it is assigned to is deleted
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :param name: str (optional)
               New name to set
        :return: :class:`BoundPrimaryIP <hcloud.primary_ips.client.BoundPrimaryIP>`
        """
        data = {}
        if auto_delete is not None:
            data["auto_delete"] = auto_delete
        if labels is not None:
            data["labels"] = labels
        if name is not None:
            data["name"] = name

        response = self._client.request(
            url=f"/primary_ips/{primary_ip.id}",
            method="PUT",
            json=data,
        )
        return BoundPrimaryIP(self, response["primary_ip"])

    def delete(self, primary_ip):
        # type: (PrimaryIP) -> bool
        """Deletes a Primary IP. If it is currently assigned to an assignee it will automatically get unassigned.

        :param primary_ip: :class:`BoundPrimaryIP <hcloud.primary_ips.client.BoundPrimaryIP>` or  :class:`PrimaryIP <hcloud.primary_ips.domain.PrimaryIP>`
        :return: boolean
        """
        self._client.request(
            url=f"/primary_ips/{primary_ip.id}",
            method="DELETE",
        )
        # Return always true, because the API does not return an action for it. When an error occurs a HcloudAPIException will be raised
        return True

    def change_protection(self, primary_ip, delete=None):
        # type: (PrimaryIP, Optional[bool]) -> BoundAction
        """Changes the protection configuration of the Primary IP.

        :param primary_ip: :class:`BoundPrimaryIP <hcloud.primary_ips.client.BoundPrimaryIP>` or  :class:`PrimaryIP <hcloud.primary_ips.domain.PrimaryIP>`
        :param delete: boolean
               If true, prevents the Primary IP from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {}
        if delete is not None:
            data.update({"delete": delete})

        response = self._client.request(
            url="/primary_ips/{primary_ip_id}/actions/change_protection".format(
                primary_ip_id=primary_ip.id
            ),
            method="POST",
            json=data,
        )
        return BoundAction(self._client.actions, response["action"])

    def assign(self, primary_ip, assignee_id, assignee_type="server"):
        # type: (PrimaryIP, int, str) -> BoundAction
        """Assigns a Primary IP to a assignee_id.

        :param primary_ip: :class:`BoundPrimaryIP <hcloud.primary_ips.client.BoundPrimaryIP>` or  :class:`PrimaryIP <hcloud.primary_ips.domain.PrimaryIP>`
        :param assignee_id: int
               Assignee the Primary IP shall be assigned to
        :param assignee_type: str
               Assignee the Primary IP shall be assigned to
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/primary_ips/{primary_ip_id}/actions/assign".format(
                primary_ip_id=primary_ip.id
            ),
            method="POST",
            json={"assignee_id": assignee_id, "assignee_type": assignee_type},
        )
        return BoundAction(self._client.actions, response["action"])

    def unassign(self, primary_ip):
        # type: (PrimaryIP) -> BoundAction
        """Unassigns a Primary IP, resulting in it being unreachable. You may assign it to a server again at a later time.

        :param primary_ip: :class:`BoundPrimaryIP <hcloud.primary_ips.client.BoundPrimaryIP>` or  :class:`PrimaryIP <hcloud.primary_ips.domain.PrimaryIP>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/primary_ips/{primary_ip_id}/actions/unassign".format(
                primary_ip_id=primary_ip.id
            ),
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])

    def change_dns_ptr(self, primary_ip, ip, dns_ptr):
        # type: (PrimaryIP, str, str) -> BoundAction
        """Changes the dns ptr that will appear when getting the dns ptr belonging to this Primary IP.

        :param primary_ip: :class:`BoundPrimaryIP <hcloud.primary_ips.client.BoundPrimaryIP>` or  :class:`PrimaryIP <hcloud.primary_ips.domain.PrimaryIP>`
        :param ip: str
               The IP address for which to set the reverse DNS entry
        :param dns_ptr: str
               Hostname to set as a reverse DNS PTR entry, will reset to original default value if `None`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url="/primary_ips/{primary_ip_id}/actions/change_dns_ptr".format(
                primary_ip_id=primary_ip.id
            ),
            method="POST",
            json={"ip": ip, "dns_ptr": dns_ptr},
        )
        return BoundAction(self._client.actions, response["action"])
