from __future__ import annotations


class BaseDomain:
    __slots__ = ()

    @classmethod
    def from_dict(cls, data: dict):  # type: ignore[no-untyped-def]
        """
        Build the domain object from the data dict.
        """
        supported_data = {k: v for k, v in data.items() if k in cls.__slots__}
        return cls(**supported_data)

    def __repr__(self) -> str:
        kwargs = [f"{key}={getattr(self, key)!r}" for key in self.__slots__]  # type: ignore[var-annotated]
        return f"{self.__class__.__qualname__}({', '.join(kwargs)})"


class DomainIdentityMixin:
    __slots__ = ()

    id: int | None
    name: str | None

    @property
    def id_or_name(self) -> int | str:
        """
        Return the first defined value, and fails if none is defined.
        """
        if self.id is not None:
            return self.id
        if self.name is not None:
            return self.name
        raise ValueError("id or name must be set")


class Pagination(BaseDomain):
    __slots__ = (
        "page",
        "per_page",
        "previous_page",
        "next_page",
        "last_page",
        "total_entries",
    )

    def __init__(
        self,
        page: int,
        per_page: int,
        previous_page: int | None = None,
        next_page: int | None = None,
        last_page: int | None = None,
        total_entries: int | None = None,
    ):
        self.page = page
        self.per_page = per_page
        self.previous_page = previous_page
        self.next_page = next_page
        self.last_page = last_page
        self.total_entries = total_entries


class Meta(BaseDomain):
    __slots__ = ("pagination",)

    def __init__(self, pagination: Pagination | None = None):
        self.pagination = pagination

    @classmethod
    def parse_meta(cls, response: dict) -> Meta | None:
        """
        If present, extract the meta details from the response and return a meta object.
        """
        meta = None
        if response and "meta" in response:
            meta = cls()
            try:
                meta.pagination = Pagination(**response["meta"]["pagination"])
            except KeyError:
                pass

        return meta
