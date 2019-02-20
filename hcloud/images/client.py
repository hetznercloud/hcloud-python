# -*- coding: utf-8 -*-
from hcloud.actions.client import BoundAction
from hcloud.core.client import BoundModelBase, ClientEntityBase
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

    def get_actions_list(self, sort=None, page=None, per_page=None):
        # type: (Optional[List[str]], Optional[int], Optional[int]) -> PageResult[BoundAction, Meta]
        return self._client.get_actions_list(self, sort, page, per_page)

    def get_actions(self, sort=None):
        # type: (Optional[List[str]]) -> List[BoundAction]
        return self._client.get_actions(self, sort)

    def update(self, description=None, type=None, labels=None):
        # type: (Optional[str], Optional[Dict[str, str]]) -> BoundImage
        return self._client.update(self, description, type, labels)

    def delete(self):
        # type: () -> bool
        return self._client.delete(self)

    def change_protection(self, delete=None):
        # type: (Optional[bool]) -> BoundAction
        return self._client.change_protection(self, delete)


class ImagesClient(ClientEntityBase):
    results_list_attribute_name = 'images'

    def get_actions_list(self,
                         image,         # type: Image
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
        response = self._client.request(url="/images/{image_id}/actions".format(image_id=image.id), method="GET", params=params)
        actions = [BoundAction(self._client.actions, action_data) for action_data in response['actions']]
        return add_meta_to_result(actions, response, 'actions')

    def get_actions(self,
                    image,         # type: Image
                    sort=None,     # type: Optional[List[str]]
                    ):
        # type: (...) -> List[BoundAction]
        return super(ImagesClient, self).get_actions(image, sort=sort)

    def get_by_id(self, id):
        # type: (int) -> BoundImage
        response = self._client.request(url="/images/{image_id}".format(image_id=id), method="GET")
        return BoundImage(self, response['image'])

    def get_list(self,
                 name=None,            # type: Optional[str]
                 label_selector=None,  # type: Optional[str]
                 bound_to=None,        # type: Optional[List[str]]
                 type=None,            # type: Optional[List[str]]
                 sort=None,            # type: Optional[List[str]]
                 page=None,            # type: Optional[int]
                 per_page=None         # type: Optional[int]
                 ):
        # type: (...) -> PageResults[List[BoundImage]]
        params = {}
        if name:
            params['name'] = name
        if label_selector:
            params['label_selector'] = label_selector
        if bound_to:
            params['bound_to'] = bound_to
        if type:
            params['type'] = type
        if sort:
            params['sort'] = sort
        if page:
            params['page'] = page
        if per_page:
            params['per_page'] = per_page

        response = self._client.request(url="/images", method="GET", params=params)
        images = [BoundImage(self, image_data) for image_data in response['images']]

        return self.add_meta_to_result(images, response)

    def get_all(self,
                name=None,            # type: Optional[str]
                label_selector=None,  # type: Optional[str]
                bound_to=None,        # type: Optional[List[str]]
                type=None,            # type: Optional[List[str]]
                sort=None,            # type: Optional[List[str]]
                ):
        # type: (...) -> List[BoundImage]
        return super(ImagesClient, self).get_all(name=name, label_selector=label_selector, bound_to=bound_to, type=type, sort=sort)

    def update(self, image, description=None, type=None, labels=None):
        # type:(Image,  Optional[str], Optional[str],  Optional[Dict[str, str]]) -> BoundImage
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
        self._client.request(url="/images/{image_id}".format(image_id=image.id), method="DELETE")
        # Return allays true, because the API does not return an action for it. When an error occurs a APIException will be raised
        return True

    def change_protection(self, image, delete=None):
        # type: (Image, Optional[bool], Optional[bool]) -> BoundAction
        data = {}
        if delete is not None:
            data.update({"delete": delete})

        response = self._client.request(url="/images/{image_id}/actions/change_protection".format(image_id=image.id), method="POST", json=data)
        return BoundAction(self._client.actions, response['action'])
