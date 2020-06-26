# -*- coding: utf-8 -*-
from hcloud.actions.client import BoundAction
from hcloud.core.client import BoundModelBase, ClientEntityBase, GetEntityByNameMixin
from hcloud.core.domain import add_meta_to_result

from hcloud.images.domain import Image


class BoundImage(BoundModelBase):
    model = Image

    def __init__(self, client, data):
        from hcloud.servers.client import BoundServer
        created_from = data.get("created_from")
        if created_from is not None:
            data['created_from'] = BoundServer(client._client.servers, created_from, complete=False)
        bound_to = data.get("bound_to")
        if bound_to is not None:
            data['bound_to'] = BoundServer(client._client.servers, {"id": bound_to}, complete=False)

        super(BoundImage, self).__init__(client, data)

    def get_actions_list(self, sort=None, page=None, per_page=None, status=None):
        # type: (Optional[List[str]], Optional[int], Optional[int], Optional[List[str]]) -> PageResult[BoundAction, Meta]
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
        return self._client.get_actions_list(self, sort=sort, page=page, per_page=per_page, status=status)

    def get_actions(self, sort=None, status=None):
        # type: (Optional[List[str]], Optional[List[str]]) -> List[BoundAction]
        """Returns all action objects for the image.

        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `id:asc` `id:desc` `command` `command:asc` `command:desc` `status` `status:asc` `status:desc` `progress` `progress:asc` `progress:desc` `started` `started:asc` `started:desc` `finished` `finished:asc` `finished:desc`
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return self._client.get_actions(self, status=status, sort=sort)

    def update(self, description=None, type=None, labels=None):
        # type: (Optional[str], Optional[Dict[str, str]]) -> BoundImage
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
        return self._client.update(self, description, type, labels)

    def delete(self):
        # type: () -> bool
        """Deletes an Image. Only images of type snapshot and backup can be deleted.

        :return: bool
        """
        return self._client.delete(self)

    def change_protection(self, delete=None):
        # type: (Optional[bool]) -> BoundAction
        """Changes the protection configuration of the image. Can only be used on snapshots.

        :param delete: bool
               If true, prevents the snapshot from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        return self._client.change_protection(self, delete)


class ImagesClient(ClientEntityBase, GetEntityByNameMixin):
    results_list_attribute_name = 'images'

    def get_actions_list(self,
                         image,         # type: Image
                         sort=None,     # type: Optional[List[str]]
                         page=None,     # type: Optional[int]
                         per_page=None,  # type: Optional[int]
                         status=None,  # type: Optional[List[str]]
                         ):
        # type: (...) -> PageResults[List[BoundAction], Meta]
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
        params = {}
        if sort is not None:
            params["sort"] = sort
        if status is not None:
            params["status"] = status
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        response = self._client.request(url="/images/{image_id}/actions".format(image_id=image.id), method="GET", params=params)
        actions = [BoundAction(self._client.actions, action_data) for action_data in response['actions']]
        return add_meta_to_result(actions, response, 'actions')

    def get_actions(self,
                    image,         # type: Image
                    sort=None,  # type: Optional[List[str]]
                    status=None,   # type: Optional[List[str]]
                    ):
        # type: (...) -> List[BoundAction]
        """Returns all action objects for an image.

        :param image: :class:`BoundImage <hcloud.images.client.BoundImage>` or :class:`Image <hcloud.images.domain.Image>`
        :param status: List[str] (optional)
               Response will have only actions with specified statuses. Choices: `running` `success` `error`
        :param sort: List[str] (optional)
               Specify how the results are sorted. Choices: `id` `command` `status` `progress`  `started` `finished` . You can add one of ":asc", ":desc" to modify sort order. ( ":asc" is default)
        :return: List[:class:`BoundAction <hcloud.actions.client.BoundAction>`]
        """
        return super(ImagesClient, self).get_actions(image, sort=sort, status=status)

    def get_by_id(self, id):
        # type: (int) -> BoundImage
        """Get a specific Image

        :param id: int
        :return: :class:`BoundImage <hcloud.images.client.BoundImage
        """
        response = self._client.request(url="/images/{image_id}".format(image_id=id), method="GET")
        return BoundImage(self, response['image'])

    def get_list(self,
                 name=None,            # type: Optional[str]
                 label_selector=None,  # type: Optional[str]
                 bound_to=None,        # type: Optional[List[str]]
                 type=None,            # type: Optional[List[str]]
                 sort=None,            # type: Optional[List[str]]
                 page=None,            # type: Optional[int]
                 per_page=None,        # type: Optional[int]
                 status=None           # type: Optional[List[str]]
                 ):
        # type: (...) -> PageResults[List[BoundImage]]
        """Get all images

        :param name: str (optional)
               Can be used to filter images by their name.
        :param label_selector: str (optional)
               Can be used to filter servers by labels. The response will only contain servers matching the label selector.
        :param bound_to: List[str] (optional)
               Server Id linked to the image. Only available for images of type backup
        :param type: List[str] (optional)
               Choices: system snapshot backup
        :param status: List[str] (optional)
               Can be used to filter images by their status. The response will only contain images matching the status.
        :param sort: List[str] (optional)
               Choices: id id:asc id:desc name name:asc name:desc created created:asc created:desc
        :param page: int (optional)
               Specifies the page to fetch
        :param per_page: int (optional)
               Specifies how many results are returned by page
        :return: (List[:class:`BoundImage <hcloud.images.client.BoundImage>`], :class:`Meta <hcloud.core.domain.Meta>`)
        """
        params = {}
        if name is not None:
            params['name'] = name
        if label_selector is not None:
            params['label_selector'] = label_selector
        if bound_to is not None:
            params['bound_to'] = bound_to
        if type is not None:
            params['type'] = type
        if sort is not None:
            params['sort'] = sort
        if page is not None:
            params['page'] = page
        if per_page is not None:
            params['per_page'] = per_page
        if status is not None:
            params['status'] = per_page

        response = self._client.request(url="/images", method="GET", params=params)
        images = [BoundImage(self, image_data) for image_data in response['images']]

        return self._add_meta_to_result(images, response)

    def get_all(self,
                name=None,            # type: Optional[str]
                label_selector=None,  # type: Optional[str]
                bound_to=None,        # type: Optional[List[str]]
                type=None,            # type: Optional[List[str]]
                sort=None,            # type: Optional[List[str]]
                status=None,          # type: Optional[List[str]]
                ):
        # type: (...) -> List[BoundImage]
        """Get all images

        :param name: str (optional)
               Can be used to filter images by their name.
        :param label_selector: str (optional)
               Can be used to filter servers by labels. The response will only contain servers matching the label selector.
        :param bound_to: List[str] (optional)
               Server Id linked to the image. Only available for images of type backup
        :param type: List[str] (optional)
               Choices: system snapshot backup
        :param status: List[str] (optional)
               Can be used to filter images by their status. The response will only contain images matching the status.
        :param sort: List[str] (optional)
               Choices: id name created (You can add one of ":asc", ":desc" to modify sort order. ( ":asc" is default))
        :return: List[:class:`BoundImage <hcloud.images.client.BoundImage>`]
        """
        return super(ImagesClient, self).get_all(name=name, label_selector=label_selector, bound_to=bound_to, type=type, sort=sort, status=status)

    def get_by_name(self, name):
        # type: (str) -> BoundImage
        """Get image by name

        :param name: str
               Used to get image by name.
        :return: :class:`BoundImage <hcloud.images.client.BoundImage>`
        """
        return super(ImagesClient, self).get_by_name(name)

    def update(self, image, description=None, type=None, labels=None):
        # type:(Image,  Optional[str], Optional[str],  Optional[Dict[str, str]]) -> BoundImage
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
        data = {}
        if description is not None:
            data.update({"description": description})
        if type is not None:
            data.update({"type": type})
        if labels is not None:
            data.update({"labels": labels})
        response = self._client.request(url="/images/{image_id}".format(image_id=image.id), method="PUT", json=data)
        return BoundImage(self, response['image'])

    def delete(self, image):
        # type: (Image) -> bool
        """Deletes an Image. Only images of type snapshot and backup can be deleted.

        :param :class:`BoundImage <hcloud.images.client.BoundImage>` or :class:`Image <hcloud.images.domain.Image>`
        :return: bool
        """
        self._client.request(url="/images/{image_id}".format(image_id=image.id), method="DELETE")
        # Return allays true, because the API does not return an action for it. When an error occurs a APIException will be raised
        return True

    def change_protection(self, image, delete=None):
        # type: (Image, Optional[bool], Optional[bool]) -> BoundAction
        """Changes the protection configuration of the image. Can only be used on snapshots.

        :param image: :class:`BoundImage <hcloud.images.client.BoundImage>` or :class:`Image <hcloud.images.domain.Image>`
        :param delete: bool
               If true, prevents the snapshot from being deleted
        :return: :class:`BoundAction <hcloud.actions.client.BoundAction>`
        """
        data = {}
        if delete is not None:
            data.update({"delete": delete})

        response = self._client.request(url="/images/{image_id}/actions/change_protection".format(image_id=image.id), method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])
