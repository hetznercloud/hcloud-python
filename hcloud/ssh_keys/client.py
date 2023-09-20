from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

from ..core import BoundModelBase, ClientEntityBase, Meta
from .domain import SSHKey

if TYPE_CHECKING:
    from .._client import Client


class BoundSSHKey(BoundModelBase, SSHKey):
    _client: SSHKeysClient

    model = SSHKey

    def update(
        self,
        name: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundSSHKey:
        """Updates an SSH key. You can update an SSH key name and an SSH key labels.

        :param description: str (optional)
               New Description to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>`
        """
        return self._client.update(self, name, labels)

    def delete(self) -> bool:
        """Deletes an SSH key. It cannot be used anymore.
        :return: boolean
        """
        return self._client.delete(self)


class SSHKeysPageResult(NamedTuple):
    ssh_keys: list[BoundSSHKey]
    meta: Meta | None


class SSHKeysClient(ClientEntityBase):
    _client: Client

    def get_by_id(self, id: int) -> BoundSSHKey:
        """Get a specific SSH Key by its ID

        :param id: int
        :return: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>`
        """
        response = self._client.request(url=f"/ssh_keys/{id}", method="GET")
        return BoundSSHKey(self, response["ssh_key"])

    def get_list(
        self,
        name: str | None = None,
        fingerprint: str | None = None,
        label_selector: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> SSHKeysPageResult:
        """Get a list of SSH keys from the account

        :param name: str (optional)
               Can be used to filter SSH keys by their name. The response will only contain the SSH key matching the specified name.
        :param fingerprint: str (optional)
               Can be used to filter SSH keys by their fingerprint. The response will only contain the SSH key matching the specified fingerprint.
        :param label_selector: str (optional)
               Can be used to filter SSH keys by labels. The response will only contain SSH keys matching the label selector.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return:  (List[:class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if fingerprint is not None:
            params["fingerprint"] = fingerprint
        if label_selector is not None:
            params["label_selector"] = label_selector
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(url="/ssh_keys", method="GET", params=params)

        ssh_keys = [
            BoundSSHKey(self, server_data) for server_data in response["ssh_keys"]
        ]
        return SSHKeysPageResult(ssh_keys, Meta.parse_meta(response))

    def get_all(
        self,
        name: str | None = None,
        fingerprint: str | None = None,
        label_selector: str | None = None,
    ) -> list[BoundSSHKey]:
        """Get all SSH keys from the account

        :param name: str (optional)
               Can be used to filter SSH keys by their name. The response will only contain the SSH key matching the specified name.
        :param fingerprint: str (optional)
               Can be used to filter SSH keys by their fingerprint. The response will only contain the SSH key matching the specified fingerprint.
        :param label_selector: str (optional)
               Can be used to filter SSH keys by labels. The response will only contain SSH keys matching the label selector.
        :return:  List[:class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>`]
        """
        return self._iter_pages(
            self.get_list,
            name=name,
            fingerprint=fingerprint,
            label_selector=label_selector,
        )

    def get_by_name(self, name: str) -> BoundSSHKey | None:
        """Get ssh key by name

        :param name: str
               Used to get ssh key by name.
        :return: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>`
        """
        return self._get_first_by(name=name)

    def get_by_fingerprint(self, fingerprint: str) -> BoundSSHKey | None:
        """Get ssh key by fingerprint

        :param fingerprint: str
                Used to get ssh key by fingerprint.
        :return: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>`
        """
        return self._get_first_by(fingerprint=fingerprint)

    def create(
        self,
        name: str,
        public_key: str,
        labels: dict[str, str] | None = None,
    ) -> BoundSSHKey:
        """Creates a new SSH key with the given name and public_key.

        :param name: str
        :param public_key: str
               Public Key of the SSH Key you want create
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>`
        """
        data: dict[str, Any] = {"name": name, "public_key": public_key}
        if labels is not None:
            data["labels"] = labels
        response = self._client.request(url="/ssh_keys", method="POST", json=data)
        return BoundSSHKey(self, response["ssh_key"])

    def update(
        self,
        ssh_key: SSHKey | BoundSSHKey,
        name: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundSSHKey:
        """Updates an SSH key. You can update an SSH key name and an SSH key labels.

        :param ssh_key: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>` or  :class:`SSHKey <hcloud.ssh_keys.domain.SSHKey>`
        :param name: str (optional)
               New Description to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>`
        """
        data: dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if labels is not None:
            data["labels"] = labels
        response = self._client.request(
            url=f"/ssh_keys/{ssh_key.id}",
            method="PUT",
            json=data,
        )
        return BoundSSHKey(self, response["ssh_key"])

    def delete(self, ssh_key: SSHKey | BoundSSHKey) -> bool:
        """Deletes an SSH key. It cannot be used anymore.

        :param ssh_key: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>` or  :class:`SSHKey <hcloud.ssh_keys.domain.SSHKey>`
        :return: True
        """
        self._client.request(url=f"/ssh_keys/{ssh_key.id}", method="DELETE")
        # Return always true, because the API does not return an action for it. When an error occurs a HcloudAPIException will be raised
        return True
