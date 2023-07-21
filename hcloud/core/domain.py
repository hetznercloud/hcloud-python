from __future__ import annotations


class BaseDomain:
    __slots__ = ()

    @classmethod
    def from_dict(cls, data):
        supported_data = {k: v for k, v in data.items() if k in cls.__slots__}
        return cls(**supported_data)

    def __repr__(self) -> str:
        kwargs = [f"{key}={getattr(self, key)!r}" for key in self.__slots__]
        return f"{self.__class__.__qualname__}({', '.join(kwargs)})"


class DomainIdentityMixin:
    __slots__ = ()

    @property
    def id_or_name(self):
        if self.id is not None:
            return self.id
        elif self.name is not None:
            return self.name
        else:
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
        page,
        per_page,
        previous_page=None,
        next_page=None,
        last_page=None,
        total_entries=None,
    ):
        self.page = page
        self.per_page = per_page
        self.previous_page = previous_page
        self.next_page = next_page
        self.last_page = last_page
        self.total_entries = total_entries


class Meta(BaseDomain):
    __slots__ = ("pagination",)

    def __init__(self, pagination=None):
        self.pagination = pagination

    @classmethod
    def parse_meta(cls, response: dict) -> Meta | None:
        meta = None
        if response and "meta" in response:
            meta = cls()
            try:
                meta.pagination = Pagination(**response["meta"]["pagination"])
            except KeyError:
                pass

        return meta
