# -*- coding: utf-8 -*-
from hcloud.core.domain import add_meta_to_result


class ClientEntityBase(object):
    max_per_page = 50
    results_list_attribute_name = None

    def __init__(self, client):
        """
        :param client: Client
        :return self
        """
        self._client = client

    def _is_list_attribute_implemented(self):
        if self.results_list_attribute_name is None:
            raise NotImplementedError(
                "in order to get results list, 'results_list_attribute_name' attribute of {} has to be specified".format(
                    self.__class__.__name__
                )
            )

    def _add_meta_to_result(
        self,
        results,  # type: List[BoundModelBase]
        response,  # type: json
    ):
        # type: (...) -> PageResult
        self._is_list_attribute_implemented()
        return add_meta_to_result(results, response, self.results_list_attribute_name)

    def _get_all(
        self,
        list_function,  # type: function
        results_list_attribute_name,  # type: str
        *args,
        **kwargs
    ):
        # type (...) -> List[BoundModelBase]
        page = 1

        results = []

        while page:
            page_result = list_function(
                page=page, per_page=self.max_per_page, *args, **kwargs
            )
            result = getattr(page_result, results_list_attribute_name)
            if result:
                results.extend(result)
            meta = page_result.meta
            if (
                meta
                and meta.pagination
                and meta.pagination.next_page
                and meta.pagination.next_page
            ):
                page = meta.pagination.next_page
            else:
                page = None

        return results

    def get_all(self, *args, **kwargs):
        # type: (...) -> List[BoundModelBase]
        self._is_list_attribute_implemented()
        return self._get_all(
            self.get_list, self.results_list_attribute_name, *args, **kwargs
        )

    def get_actions(self, *args, **kwargs):
        # type: (...) -> List[BoundModelBase]
        if not hasattr(self, "get_actions_list"):
            raise ValueError("this endpoint does not support get_actions method")

        return self._get_all(self.get_actions_list, "actions", *args, **kwargs)


class GetEntityByNameMixin(object):
    """
    Use as a mixin for ClientEntityBase classes
    """

    def get_by_name(self, name):
        # type: (str) -> BoundModelBase
        self._is_list_attribute_implemented()
        response = self.get_list(name=name)
        entities = getattr(response, self.results_list_attribute_name)
        entity = entities[0] if entities else None
        return entity


class BoundModelBase(object):
    """Bound Model Base"""

    model = None

    def __init__(self, client, data={}, complete=True):
        """
        :param client:
                The client for the specific model to use
        :param data:
                The data of the model
        :param complete: bool
                False if not all attributes of the model fetched
        """
        self._client = client
        self.complete = complete
        self.data_model = self.model.from_dict(data)

    def __getattr__(self, name):
        """Allow magical access to the properties of the model
        :param name: str
        :return:
        """
        value = getattr(self.data_model, name)
        if not value and not self.complete:
            self.reload()
            value = getattr(self.data_model, name)
        return value

    def reload(self):
        """Reloads the model and tries to get all data from the APIx"""
        bound_model = self._client.get_by_id(self.data_model.id)
        self.data_model = bound_model.data_model
        self.complete = True
