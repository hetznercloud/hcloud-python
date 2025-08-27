from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any, NamedTuple

from ..actions import ActionsPageResult, BoundAction, ResourceActionsClient
from ..core import BoundModelBase, Meta, ResourceClientBase
from .domain import Image

if TYPE_CHECKING:
    from .._client import Client


class BoundImage(BoundModelBase, Image):
    _client: ImagesClient

    model = Image

    def __init__(self, client: ImagesClient, data: dict):
        # pylint: disable=import-outside-toplevel
        from ..servers import BoundServer

        created_from = data.get("created_from")
        if created_from is not None:
            data["created_from"] = BoundServer(
                client._parent.servers, created_from, complete=False
            )
        bound_to = data.get("bound_to")
        if bound_to is not None:
            data["bound_to"] = BoundServer(
                client._parent.servers, {"id": bound_to}, complete=False
            )

        super().__init__(client, data)

    def get_actions_list(
        self,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
        status: list[str] | None = None,
    ) -> ActionsPageResult:
        """Returns a list of action objects for the image.

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
        return self._client.get_actions_list(
            self,
            sort=sort,
            page=page,
            per_page=per_page,
            status=status,
        )

    def get_actions(
        self,
        sort: list[str] | None = None,
        status: list[str] | None = None,
    ) -> list[BoundAction]:
        """Returns all action objects for the image.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.get_actions(
            self,
            status=status,
            sort=sort,
        )

    def update(
        self,
        description: str | None = None,
        type: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundImage:
        """Updates the Image. You may change the description, convert a Backup image to a Snapshot Image or change the image labels.

        :param description: str (optional)
               New description of Image
        :param type: str (optional)
               Destination image type to convert to
               Choices: snapshot
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundImage <hcloud.images.client.BoundImage>`
        """
        return self._client.update(
            self, description=description, type=type, labels=labels
        )

    def delete(self) -> bool:
        """Deletes an Image. Only images of type snapshot and backup can be deleted.

        :return: bool
        """
        return self._client.delete(self)

    def change_protection(self, delete: bool | None = None) -> BoundAction:
        """Changes the protection configuration of the image. Can only be used on snapshots.

        :param delete: bool
               If true, prevents the snapshot from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_protection(self, delete=delete)


class ImagesPageResult(NamedTuple):
    images: list[BoundImage]
    meta: Meta


class ImagesClient(ResourceClientBase):
    _base_url = "/images"

    actions: ResourceActionsClient
    """Images scoped actions client

    :type: :class:`ResourceActionsClient <hcloud.actions.client.ResourceActionsClient>`
    """

    def __init__(self, client: Client):
        super().__init__(client)
        self.actions = ResourceActionsClient(client, self._base_url)

    def get_actions_list(
        self,
        image: Image | BoundImage,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
        status: list[str] | None = None,
    ) -> ActionsPageResult:
        """Returns a list of action objects for an image.

        :param image: :class:`BoundImage <hcloud.images.client.BoundImage>` or :class:`Image <hcloud.images.domain.Image>`
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
        if sort is not None:
            params["sort"] = sort
        if status is not None:
            params["status"] = status
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        response = self._client.request(
            url=f"{self._base_url}/{image.id}/actions",
            method="GET",
            params=params,
        )
        actions = [
            BoundAction(self._parent.actions, action_data)
            for action_data in response["actions"]
        ]
        return ActionsPageResult(actions, Meta.parse_meta(response))

    def get_actions(
        self,
        image: Image | BoundImage,
        sort: list[str] | None = None,
        status: list[str] | None = None,
    ) -> list[BoundAction]:
        """Returns all action objects for an image.

        :param image: :class:`BoundImage <hcloud.images.client.BoundImage>` or :class:`Image <hcloud.images.domain.Image>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `command` `status` `progress`  `started` `finished` . You can add one of ":asc", ":desc" to modify sort order. ( ":asc" is default)
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._iter_pages(
            self.get_actions_list,
            image,
            sort=sort,
            status=status,
        )

    def get_by_id(self, id: int) -> BoundImage:
        """Get a specific Image

        :param id: int
        :return: :class:`BoundImage <hcloud.images.client.BoundImage`
        """
        response = self._client.request(url=f"{self._base_url}/{id}", method="GET")
        return BoundImage(self, response["image"])

    def get_list(
        self,
        name: str | None = None,
        label_selector: str | None = None,
        bound_to: list[str] | None = None,
        type: list[str] | None = None,
        architecture: list[str] | None = None,
        sort: list[str] | None = None,
        page: int | None = None,
        per_page: int | None = None,
        status: list[str] | None = None,
        include_deprecated: bool | None = None,
    ) -> ImagesPageResult:
        """Get all images

        :param name: str (optional)
               Can be used to filter images by their name.
        :param label_selector: str (optional)
               Can be used to filter servers by labels. The response will only contain servers matching the label selector.
        :param bound_to: List[str] (optional)
               Server Id linked to the image. Only available for images of type backup
        :param type: List[str] (optional)
               Choices: system snapshot backup
        :param architecture: List[str] (optional)
               Choices: x86 arm
        :param status: List[str] (optional)
               Can be used to filter images by their status. The response will only contain images matching the status.
        :param sort: List[str] (optional)
               Choices: id id:asc id:desc name name:asc name:desc created created:asc created:desc
        :param include_deprecated: bool (optional)
               Include deprecated images in the response. Default: False
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundImage <hcloud.images.client.BoundImage>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if label_selector is not None:
            params["label_selector"] = label_selector
        if bound_to is not None:
            params["bound_to"] = bound_to
        if type is not None:
            params["type"] = type
        if architecture is not None:
            params["architecture"] = architecture
        if sort is not None:
            params["sort"] = sort
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if status is not None:
            params["status"] = per_page
        if include_deprecated is not None:
            params["include_deprecated"] = include_deprecated
        response = self._client.request(url=self._base_url, method="GET", params=params)
        images = [BoundImage(self, image_data) for image_data in response["images"]]

        return ImagesPageResult(images, Meta.parse_meta(response))

    def get_all(
        self,
        name: str | None = None,
        label_selector: str | None = None,
        bound_to: list[str] | None = None,
        type: list[str] | None = None,
        architecture: list[str] | None = None,
        sort: list[str] | None = None,
        status: list[str] | None = None,
        include_deprecated: bool | None = None,
    ) -> list[BoundImage]:
        """Get all images

        :param name: str (optional)
               Can be used to filter images by their name.
        :param label_selector: str (optional)
               Can be used to filter servers by labels. The response will only contain servers matching the label selector.
        :param bound_to: List[str] (optional)
               Server Id linked to the image. Only available for images of type backup
        :param type: List[str] (optional)
               Choices: system snapshot backup
        :param architecture: List[str] (optional)
               Choices: x86 arm
        :param status: List[str] (optional)
               Can be used to filter images by their status. The response will only contain images matching the status.
        :param sort: List[str] (optional)
               Choices: id name created (You can add one of ":asc", ":desc" to modify sort order. ( ":asc" is default))
        :param include_deprecated: bool (optional)
               Include deprecated images in the response. Default: False
        :return: List[:class:`BoundImage <hcloud.images.client.BoundImage>`]
        """
        return self._iter_pages(
            self.get_list,
            name=name,
            label_selector=label_selector,
            bound_to=bound_to,
            type=type,
            architecture=architecture,
            sort=sort,
            status=status,
            include_deprecated=include_deprecated,
        )

    def get_by_name(self, name: str) -> BoundImage | None:
        """Get image by name

        :param name: str
               Used to get image by name.
        :return: :class:`BoundImage <hcloud.images.client.BoundImage>`

        .. deprecated:: 1.19
            Use :func:`hcloud.images.client.ImagesClient.get_by_name_and_architecture` instead.
        """
        warnings.warn(
            "The 'hcloud.images.client.ImagesClient.get_by_name' method is deprecated, please use the "
            "'hcloud.images.client.ImagesClient.get_by_name_and_architecture' method instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._get_first_by(name=name)

    def get_by_name_and_architecture(
        self,
        name: str,
        architecture: str,
        *,
        include_deprecated: bool | None = None,
    ) -> BoundImage | None:
        """Get image by name

        :param name: str
               Used to identify the image.
        :param architecture: str
               Used to identify the image.
        :param include_deprecated: bool (optional)
               Include deprecated images. Default: False
        :return: :class:`BoundImage <hcloud.images.client.BoundImage>`
        """
        return self._get_first_by(
            name=name,
            architecture=[architecture],
            include_deprecated=include_deprecated,
        )

    def update(
        self,
        image: Image | BoundImage,
        description: str | None = None,
        type: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> BoundImage:
        """Updates the Image. You may change the description, convert a Backup image to a Snapshot Image or change the image labels.

        :param image: :class:`BoundImage <hcloud.images.client.BoundImage>` or :class:`Image <hcloud.images.domain.Image>`
        :param description: str (optional)
               New description of Image
        :param type: str (optional)
               Destination image type to convert to
               Choices: snapshot
        :param labels: Dict[str, str] (optional)
               User-defined labels (key-value pairs)
        :return: :class:`BoundImage <hcloud.images.client.BoundImage>`
        """
        data: dict[str, Any] = {}
        if description is not None:
            data.update({"description": description})
        if type is not None:
            data.update({"type": type})
        if labels is not None:
            data.update({"labels": labels})
        response = self._client.request(
            url=f"{self._base_url}/{image.id}", method="PUT", json=data
        )
        return BoundImage(self, response["image"])

    def delete(self, image: Image | BoundImage) -> bool:
        """Deletes an Image. Only images of type snapshot and backup can be deleted.

        :param :class:`BoundImage <hcloud.images.client.BoundImage>` or :class:`Image <hcloud.images.domain.Image>`
        :return: bool
        """
        self._client.request(url=f"{self._base_url}/{image.id}", method="DELETE")
        # Return allays true, because the API does not return an action for it. When an error occurs a APIException will be raised
        return True

    def change_protection(
        self,
        image: Image | BoundImage,
        delete: bool | None = None,
    ) -> BoundAction:
        """Changes the protection configuration of the image. Can only be used on snapshots.

        :param image: :class:`BoundImage <hcloud.images.client.BoundImage>` or :class:`Image <hcloud.images.domain.Image>`
        :param delete: bool
               If true, prevents the snapshot from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data: dict[str, Any] = {}
        if delete is not None:
            data.update({"delete": delete})

        response = self._client.request(
            url=f"{self._base_url}/{image.id}/actions/change_protection",
            method="POST",
            json=data,
        )
        return BoundAction(self._parent.actions, response["action"])
