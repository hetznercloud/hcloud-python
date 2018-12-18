# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase

from hcloud.ssh_keys.domain import SSHKey


class BoundSSHKey(BoundModelBase):
    model = SSHKey

    def update(self, name=None, labels=None):
        # type: (Optional[str], Optional[Dict[str, str]]) -> BoundSSHKey
        return self._client.update(self, name, labels)

    def delete(self):
        # type: () -> bool
        return self._client.delete(self)


class SSHKeysClient(ClientEntityBase):

    def get_by_id(self, id):
        # type: (int) -> BoundSSHKey
        response = self._client.request(url="/ssh_keys/{ssh_key_id}".format(ssh_key_id=id), method="GET")
        return BoundSSHKey(self, response['ssh_key'])

    def get_all(self, name=None, fingerprint=None, label_selector=None):
        # type: (Optional[str], Optional[str], Optional[str]) -> List[BoundSSHKey]
        params = {}
        if name is not None:
            params['name'] = name
        if fingerprint is not None:
            params['fingerprint'] = fingerprint
        if label_selector is not None:
            params['label_selector'] = label_selector

        response = self._client.request(url="/ssh_keys", method="GET", params=params)
        return [BoundSSHKey(self, location_data) for location_data in response['ssh_keys']]

    def create(self, name, public_key, labels=None):
        # type: (str, str, Optional[Dict[str, str]]) -> BoundSSHKey
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
        data = {}
        if name is not None:
            data['name'] = name
        if labels is not None:
            data['labels'] = labels
        response = self._client.request(url="/ssh_keys/{ssh_key_id}".format(ssh_key_id=ssh_key.id), method="PUT", json=data)
        return BoundSSHKey(self, response['ssh_key'])

    def delete(self, ssh_key):
        # type: (SSHKey) -> bool
        self._client.request(url="/ssh_keys/{ssh_key_id}".format(ssh_key_id=ssh_key.id), method="DELETE")
        # Return allays true, because the API does not return an action for it. When an error occurs a HcloudAPIException will be raised
        return True
