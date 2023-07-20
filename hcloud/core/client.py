from __future__ import annotations


class ClientEntityBase:
    max_per_page = 50
    results_list_attribute_name = None

    def __init__(self, client):
        """
        :param client: Client
        :return self
        """
        self._client = client

    def _get_all(
        self,
        list_function,  # type: function
        *args,
        **kwargs,
    ):
        # type (...) -> List[BoundModelBase]
        results = []

        page = 1
        while page:
            result, meta = list_function(
                page=page, per_page=self.max_per_page, *args, **kwargs
            )
            if result:
                results.extend(result)

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
        return self._get_all(self.get_list, *args, **kwargs)

    def get_actions(self, *args, **kwargs):
        # type: (...) -> List[BoundModelBase]
        if not hasattr(self, "get_actions_list"):
            raise ValueError("this endpoint does not support get_actions method")

        return self._get_all(self.get_actions_list, *args, **kwargs)


class GetEntityByNameMixin:
    """
    Use as a mixin for ClientEntityBase classes
    """

    def get_by_name(self, name):
        # type: (str) -> BoundModelBase
        entities, _ = self.get_list(name=name)
        return entities[0] if entities else None


class BoundModelBase:
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
