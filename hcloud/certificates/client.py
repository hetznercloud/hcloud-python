from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple

from ..actions import ActionsPageResult, BoundAction, ResourceActionsClient
from ..core import BoundModelBase, ClientEntityBase, Meta
from .domain import (
    Certificate,
    CreateManagedCertificateResponse,
    ManagedCertificateError,
    ManagedCertificateStatus,
)

if TYPE_CHECKING:
    from .._client import Client


class BoundCertificate(BoundModelBase, Certificate):
    _client: CertificatesClient

    model = Certificate

    def __init__(self, client: CertificatesClient, data: dict, complete: bool = True):
        status = data.get("status")
        if status is not None:
            error_data = status.get("error")
            error = None
            if error_data:
                error = ManagedCertificateError(
                    code=error_data["code"], message=error_data["message"]
                )
            data["status"] = ManagedCertificateStatus(
                issuance=status["issuance"], renewal=status["renewal"], error=error
            )
        super().__init__(client, data, complete)

    def get_actions_list(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """Returns all action objects for a Certificate.

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

    def get_actions(
        self,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """Returns all action objects for a Certificate.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.get_actions(self, status, sort)

    def update(
        self,
        name: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundCertificate:
        """Updates an certificate. You can update an certificate name and the certificate labels.

        :param name: str (optional)
               New name to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>`
        """
        return self._client.update(self, name, labels)

    def delete(self) -> bool:
        """Deletes a certificate.
        :return: boolean
        """
        return self._client.delete(self)

    def retry_issuance(self) -> BoundAction:
        """Retry a failed Certificate issuance or renewal.
        :return: BoundAction
        """
        return self._client.retry_issuance(self)


class CertificatesPageResult(NamedTuple):
    certificates: list[BoundCertificate]
    meta: Meta | None


class CertificatesClient(ClientEntityBase):
    _client: Client

    actions: ResourceActionsClient
    """Certificates scoped actions client

    :type: :class:`ResourceActionsClient <hcloud.actions.client.ResourceActionsClient>`
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.actions = ResourceActionsClient(client, "/certificates")

    def get_by_id(self, id: int) -> BoundCertificate:
        """Get a specific certificate by its ID.

        :param id: int
        :return: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>`
        """
        response = self._client.request(url=f"/certificates/{id}", method="GET")
        return BoundCertificate(self, response["certificate"])

    def get_list(
        self,
        name: str | None = None,
        label_selector: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> CertificatesPageResult:
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
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name

        if label_selector is not None:
            params["label_selector"] = label_selector

        if page is not None:
            params["page"] = page

        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(
            url="/certificates", method="GET", params=params
        )

        certificates = [
            BoundCertificate(self, certificate_data)
            for certificate_data in response["certificates"]
        ]

        return CertificatesPageResult(certificates, Meta.parse_meta(response))

    def get_all(
        self,
        name: str | None = None,
        label_selector: str | None = None,
    ) -> list[BoundCertificate]:
        """Get all certificates

        :param name: str (optional)
               Can be used to filter certificates by their name.
        :param label_selector: str (optional)
               Can be used to filter certificates by labels. The response will only contain certificates matching the label selector.
        :return: List[:class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>`]
        """
        return self._iter_pages(self.get_list, name=name, label_selector=label_selector)

    def get_by_name(self, name: str) -> BoundCertificate | None:
        """Get certificate by name

        :param name: str
               Used to get certificate by name.
        :return: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>`
        """
        return self._get_first_by(name=name)

    def create(
        self,
        name: str,
        certificate: str,
        private_key: str,
        labels: dict[str, str] | None = None,
    ) -> BoundCertificate:
        """Creates a new Certificate with the given name, certificate and private_key. This methods allows only creating
           custom uploaded certificates. If you want to create a managed certificate use :func:`~hcloud.certificates.client.CertificatesClient.create_managed`

        :param name: str
        :param certificate: str
               Certificate and chain in PEM format, in order so that each record directly certifies the one preceding
        :param private_key: str
               Certificate key in PEM format
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>`
        """
        data: dict[str, Any] = {
            "name": name,
            "certificate": certificate,
            "private_key": private_key,
            "type": Certificate.TYPE_UPLOADED,
        }
        if labels is not None:
            data["labels"] = labels
        response = self._client.request(url="/certificates", method="POST", json=data)
        return BoundCertificate(self, response["certificate"])

    def create_managed(
        self,
        name: str,
        domain_names: list[str],
        labels: dict[str, str] | None = None,
    ) -> CreateManagedCertificateResponse:
        """Creates a new managed Certificate with the given name and domain names. This methods allows only creating
           managed certificates for domains that are using the Hetzner DNS service. If you want to create a custom uploaded certificate use :func:`~hcloud.certificates.client.CertificatesClient.create`

        :param name: str
        :param domain_names: List[str]
               Domains and subdomains that should be contained in the Certificate
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>`
        """
        data: dict[str, Any] = {
            "name": name,
            "type": Certificate.TYPE_MANAGED,
            "domain_names": domain_names,
        }
        if labels is not None:
            data["labels"] = labels
        response = self._client.request(url="/certificates", method="POST", json=data)
        return CreateManagedCertificateResponse(
            certificate=BoundCertificate(self, response["certificate"]),
            action=BoundAction(self._client.actions, response["action"]),
        )

    def update(
        self,
        certificate: Certificate | BoundCertificate,
        name: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundCertificate:
        """Updates a Certificate. You can update a certificate name and labels.

        :param certificate: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>` or  :class:`Certificate <hcloud.certificates.domain.Certificate>`
        :param name: str (optional)
               New name to set
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>`
        """
        data: dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if labels is not None:
            data["labels"] = labels
        response = self._client.request(
            url=f"/certificates/{certificate.id}",
            method="PUT",
            json=data,
        )
        return BoundCertificate(self, response["certificate"])

    def delete(self, certificate: Certificate | BoundCertificate) -> bool:
        """Deletes a certificate.

        :param certificate: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>` or  :class:`Certificate <hcloud.certificates.domain.Certificate>`
        :return: True
        """
        self._client.request(
            url=f"/certificates/{certificate.id}",
            method="DELETE",
        )
        # Return always true, because the API does not return an action for it. When an error occurs a HcloudAPIException will be raised
        return True

    def get_actions_list(
        self,
        certificate: Certificate | BoundCertificate,
        status: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> ActionsPageResult:
        """Returns all action objects for a Certificate.

        :param certificate: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>` or :class:`Certificate <hcloud.certificates.domain.Certificate>`
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
        params: dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = self._client.request(
            url=f"/certificates/{certificate.id}/actions",
            method="GET",
            params=params,
        )
        actions = [
            BoundAction(self._client.actions, action_data)
            for action_data in response["actions"]
        ]
        return ActionsPageResult(actions, Meta.parse_meta(response))

    def get_actions(
        self,
        certificate: Certificate | BoundCertificate,
        status: list[str] | None = None,
        sort: list[str] | None = None,
    ) -> list[BoundAction]:
        """Returns all action objects for a Certificate.

        :param certificate: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>` or :class:`Certificate <hcloud.certificates.domain.Certificate>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._iter_pages(
            self.get_actions_list,
            certificate,
            status=status,
            sort=sort,
        )

    def retry_issuance(
        self,
        certificate: Certificate | BoundCertificate,
    ) -> BoundAction:
        """Returns all action objects for a Certificate.

        :param certificate: :class:`BoundCertificate <hcloud.certificates.client.BoundCertificate>` or :class:`Certificate <hcloud.certificates.domain.Certificate>`
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        response = self._client.request(
            url=f"/certificates/{certificate.id}/actions/retry",
            method="POST",
        )
        return BoundAction(self._client.actions, response["action"])
