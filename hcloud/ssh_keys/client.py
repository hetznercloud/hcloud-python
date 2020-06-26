# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase, GetEntityByNameMixin

from hcloud.ssh_keys.domain import SSHKey


class BoundSSHKey(BoundModelBase):
    model = SSHKey

    def update(self, name=None, labels=None):
        # type: (Optional[str], Optional[Dict[str, str]]) -> BoundSSHKey
        """Updates an SSH key. You can update an SSH key name and an SSH key labels.

        :param description: str (optional)
               New Description to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>
        """
        return self._client.update(self, name, labels)

    def delete(self):
        # type: () -> bool
        """Deletes an SSH key. It cannot be used anymore.
           :return: boolean
        """
        return self._client.delete(self)


class SSHKeysClient(ClientEntityBase, GetEntityByNameMixin):
    results_list_attribute_name = 'ssh_keys'

    def get_by_id(self, id):
        # type: (int) -> BoundSSHKey
        """Get a specific SSH Key by its ID

        :param id: int
        :return: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>`
        """
        response = self._client.request(url="/ssh_keys/{ssh_key_id}".format(ssh_key_id=id), method="GET")
        return BoundSSHKey(self, response['ssh_key'])

    def get_list(self,
                 name=None,  # type: Optional[str]
                 fingerprint=None,  # type: Optional[str]
                 label_selector=None,  # type: Optional[str]
                 page=None,  # type: Optional[int]
                 per_page=None  # type: Optional[int]
                 ):
        # type: (...) -> PageResults[List[BoundSSHKey], Meta]
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
        params = {}
        if name is not None:
            params['name'] = name
        if fingerprint is not None:
            params['fingerprint'] = fingerprint
        if label_selector is not None:
            params['label_selector'] = label_selector
        if page is not None:
            params['page'] = page
        if per_page is not None:
            params['per_page'] = per_page

        response = self._client.request(url="/ssh_keys", method="GET", params=params)

        ass_ssh_keys = [BoundSSHKey(self, server_data) for server_data in response['ssh_keys']]
        return self._add_meta_to_result(ass_ssh_keys, response)

    def get_all(self, name=None, fingerprint=None, label_selector=None):
        # type: (Optional[str], Optional[str], Optional[str]) -> List[BoundSSHKey]
        """Get all SSH keys from the account

        :param name: str (optional)
               Can be used to filter SSH keys by their name. The response will only contain the SSH key matching the specified name.
        :param fingerprint: str (optional)
               Can be used to filter SSH keys by their fingerprint. The response will only contain the SSH key matching the specified fingerprint.
        :param label_selector: str (optional)
               Can be used to filter SSH keys by labels. The response will only contain SSH keys matching the label selector.
        :return:  List[:class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>`]
        """
        return super(SSHKeysClient, self).get_all(name=name, fingerprint=fingerprint, label_selector=label_selector)

    def get_by_name(self, name):
        # type: (str) -> SSHKeysClient
        """Get ssh key by name

        :param name: str
               Used to get ssh key by name.
        :return: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>`
        """
        return super(SSHKeysClient, self).get_by_name(name)

    def get_by_fingerprint(self, fingerprint):
        # type: (str) -> BoundSSHKey
        """Get ssh key by fingerprint

        :param fingerprint: str
                Used to get ssh key by fingerprint.
        :return: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>`
        """
        response = self.get_list(fingerprint=fingerprint)
        sshkeys = response.ssh_keys
        return sshkeys[0] if sshkeys else None

    def create(self, name, public_key, labels=None):
        # type: (str, str, Optional[Dict[str, str]]) -> BoundSSHKey
        """Creates a new SSH key with the given name and public_key.

        :param name: str
        :param public_key: str
               Public Key of the SSH Key you want create
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>`
        """
        data = {
            'name': name,
            'public_key': public_key
        }
        if labels is not None:
            data['labels'] = labels
        response = self._client.request(url="/ssh_keys", method="POST", json=data)
        return BoundSSHKey(self, response['ssh_key'])

    def update(self, ssh_key, name=None, labels=None):
        # type: (SSHKey,  Optional[str],  Optional[Dict[str, str]]) -> BoundSSHKey
        """Updates an SSH key. You can update an SSH key name and an SSH key labels.

        :param ssh_key: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>` or  :class:`SSHKey <hcloud.ssh_keys.domain.SSHKey>`
        :param name: str (optional)
               New Description to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>`
        """
        data = {}
        if name is not None:
            data['name'] = name
        if labels is not None:
            data['labels'] = labels
        response = self._client.request(url="/ssh_keys/{ssh_key_id}".format(ssh_key_id=ssh_key.id), method="PUT",
                                        json=data)
        return BoundSSHKey(self, response['ssh_key'])

    def delete(self, ssh_key):
        # type: (SSHKey) -> bool
        self._client.request(url="/ssh_keys/{ssh_key_id}".format(ssh_key_id=ssh_key.id), method="DELETE")
        """Deletes an SSH key. It cannot be used anymore.

        :param ssh_key: :class:`BoundSSHKey <hcloud.ssh_keys.client.BoundSSHKey>` or  :class:`SSHKey <hcloud.ssh_keys.domain.SSHKey>`
        :return: True
        """
        # Return always true, because the API does not return an action for it. When an error occurs a HcloudAPIException will be raised
        return True
