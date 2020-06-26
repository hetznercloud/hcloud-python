# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase, GetEntityByNameMixin

from hcloud.certificates.domain import Certificate


class BoundCertificate(BoundModelBase):
    model = Certificate

    def update(self, name=None, labels=None):
        # type: (Optional[str], Optional[Dict[str, str]]) -> BoundCertificate
        """Updates an certificate. You can update an certificate name and the certificate labels.

        :param name: str (optional)
               New name to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>
        """
        return self._client.update(self, name, labels)

    def delete(self):
        # type: () -> bool
        """Deletes a certificate.
           :return: boolean
        """
        return self._client.delete(self)


class CertificatesClient(ClientEntityBase, GetEntityByNameMixin):
    results_list_attribute_name = 'certificates'

    def get_by_id(self, id):
        # type: (int) -> BoundCertificate
        """Get a specific certificate by its ID.

        :param id: int
        :return: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>`
        """
        response = self._client.request(url="/certificates/{certificate_id}".format(certificate_id=id), method="GET")
        return BoundCertificate(self, response['certificate'])

    def get_list(self,
                 name=None,  # type: Optional[str]
                 label_selector=None,  # type: Optional[str]
                 page=None,  # type: Optional[int]
                 per_page=None  # type: Optional[int]
                 ):
        # type: (...) -> PageResults[List[BoundCertificate], Meta]
        """Get a list of certificates

        :param name: str (optional)
               Can be used to filter certificates by their name.
        :param label_selector: str (optional)
               Can be used to filter certificates by labels. The response will only contain certificates matching the label selector.
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params = {}
        if name is not None:
            params["name"] = name

        if label_selector is not None:
            params["label_selector"] = label_selector

        if page is not None:
            params['page'] = page

        if per_page is not None:
            params['per_page'] = per_page

        response = self._client.request(url="/certificates", method="GET", params=params)

        certificates = [BoundCertificate(self, certificate_data) for certificate_data in response['certificates']]

        return self._add_meta_to_result(certificates, response)

    def get_all(self, name=None, label_selector=None):
        # type: (Optional[str]) -> List[BoundCertificate]
        """Get all certificates

        :param name: str (optional)
               Can be used to filter certificates by their name.
        :param label_selector: str (optional)
               Can be used to filter certificates by labels. The response will only contain certificates matching the label selector.
        :return: List[:class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>`]
        """
        return super(CertificatesClient, self).get_all(name=name, label_selector=label_selector)

    def get_by_name(self, name):
        # type: (str) -> BoundCertificate
        """Get certificate by name

        :param name: str
               Used to get certificate by name.
        :return: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>`
        """
        return super(CertificatesClient, self).get_by_name(name)

    def create(self, name, certificate, private_key, labels=None):
        # type: (str, str, Optional[Dict[str, str]]) -> BoundCertificate
        """Creates a new Certificate with the given name, certificate and private_key.

        :param name: str
        :param certificate: str
               Certificate and chain in PEM format, in order so that each record directly certifies the one preceding
        :param private_key: str
               Certificate key in PEM format
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>`
        """
        data = {
            'name': name,
            'certificate': certificate,
            'private_key': private_key
        }
        if labels is not None:
            data['labels'] = labels
        response = self._client.request(url="/certificates", method="POST", json=data)
        return BoundCertificate(self, response['certificate'])

    def update(self, certificate, name=None, labels=None):
        # type: (Certificate,  Optional[str],  Optional[Dict[str, str]]) -> BoundCertificate
        """Updates a Certificate. You can update a certificate name and labels.

        :param certificate: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>` or  :class:`Certificate <hcloud.certificates.domain.Certificate>`
        :param name: str (optional)
               New name to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>`
        """
        data = {}
        if name is not None:
            data['name'] = name
        if labels is not None:
            data['labels'] = labels
        response = self._client.request(url="/certificates/{certificate_id}".format(certificate_id=certificate.id),
                                        method="PUT",
                                        json=data)
        return BoundCertificate(self, response['certificate'])

    def delete(self, certificate):
        # type: (Certificate) -> bool
        self._client.request(url="/certificates/{certificate_id}".format(certificate_id=certificate.id),
                             method="DELETE")
        """Deletes a certificate.

        :param certificate: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>` or  :class:`Certificate <hcloud.certificates.domain.Certificate>`
        :return: True
        """
        # Return always true, because the API does not return an action for it. When an error occurs a HcloudAPIException will be raised
        return True
