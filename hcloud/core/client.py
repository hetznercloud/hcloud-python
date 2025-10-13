from __future__ import annotations

import warnings
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from .._client import Client, ClientBase
    from .domain import BaseDomain


class ResourceClientBase:
    _base_url: ClassVar[str]
    _parent: Client
    _client: ClientBase

    max_per_page: int = 50

    def __init__(self, client: Client):
        self._parent = client
        # Use the parent "default" base client.
        self._client = client._client

    def _iter_pages(  # type: ignore[no-untyped-def]
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
                *args, page=page, per_page=self.max_per_page, **kwargs
            )
            if result:
                results.extend(result)

            if meta and meta.pagination and meta.pagination.next_page:
                page = meta.pagination.next_page
            else:
                page = 0

        return results

    def _get_first_by(self, **kwargs):  # type: ignore[no-untyped-def]
        assert hasattr(self, "get_list")
        # pylint: disable=no-member
        entities, _ = self.get_list(**kwargs)
        return entities[0] if entities else None


class ClientEntityBase(ResourceClientBase):
    """
    Kept for backward compatibility.

    .. deprecated:: 2.6.0
        Use :class:``hcloud.core.client.ResourceClientBase`` instead.
    """

    def __init__(self, client: Client):
        warnings.warn(
            "The 'hcloud.core.client.ClientEntityBase' class is deprecated, please use the "
            "'hcloud.core.client.ResourceClientBase' class instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(client)


class BoundModelBase:
    """Bound Model Base"""

    model: type[BaseDomain]

    def __init__(
        self,
        client: ResourceClientBase,
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

    def __repr__(self) -> str:
        # Override and reset hcloud.core.domain.BaseDomain.__repr__ method for bound
        # models, as they will generate a lot of API call trying to print all the fields
        # of the model.
        return object.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        """Compare a bound model object with another of the same type."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.data_model == other.data_model
