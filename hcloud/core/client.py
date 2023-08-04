from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from .._client import Client
    from ..actions import BoundAction


class ClientEntityBase:
    _client: Client

    max_per_page: int = 50

    def __init__(self, client: Client):
        """
        :param client: Client
        :return self
        """
        self._client = client

    def _get_all(  # type: ignore[no-untyped-def]
        self,
        list_function: Callable,
        *args,
        **kwargs,
    ) -> list:
        results = []

        page = 1
        while page:
            # The *PageResult tuples MUST have the following structure
            # `(result: List[Bound*], meta: Meta)`
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
                page = 0

        return results

    def get_all(self, *args, **kwargs) -> list:  # type: ignore[no-untyped-def]
        assert hasattr(self, "get_list")
        return self._get_all(self.get_list, *args, **kwargs)

    def get_actions(self, *args, **kwargs) -> list[BoundAction]:  # type: ignore[no-untyped-def]
        if not hasattr(self, "get_actions_list"):
            raise ValueError("this endpoint does not support get_actions method")

        return self._get_all(self.get_actions_list, *args, **kwargs)


class GetEntityByNameMixin:
    """
    Use as a mixin for ClientEntityBase classes
    """

    def get_by_name(self, name: str):  # type: ignore[no-untyped-def]
        assert hasattr(self, "get_list")
        entities, _ = self.get_list(name=name)
        return entities[0] if entities else None


class BoundModelBase:
    """Bound Model Base"""

    model: Any

    def __init__(
        self,
        client: ClientEntityBase,
        data: dict,
        complete: bool = True,
    ):
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

    def __getattr__(self, name: str):  # type: ignore[no-untyped-def]
        """Allow magical access to the properties of the model
        :param name: str
        :return:
        """
        value = getattr(self.data_model, name)
        if not value and not self.complete:
            self.reload()
            value = getattr(self.data_model, name)
        return value

    def reload(self) -> None:
        """Reloads the model and tries to get all data from the APIx"""
        assert hasattr(self._client, "get_by_id")
        bound_model = self._client.get_by_id(self.data_model.id)
        self.data_model = bound_model.data_model
        self.complete = True
