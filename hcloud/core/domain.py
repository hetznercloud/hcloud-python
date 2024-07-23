from __future__ import annotations


class BaseDomain:
    __api_properties__: tuple

    @classmethod
    def from_dict(cls, data: dict):  # type: ignore[no-untyped-def]
        """
        Build the domain object from the data dict.
        """
        supported_data = {k: v for k, v in data.items() if k in cls.__api_properties__}
        return cls(**supported_data)

    def __repr__(self) -> str:
        kwargs = [f"{key}={getattr(self, key)!r}" for key in self.__api_properties__]  # type: ignore[var-annotated]
        return f"{self.__class__.__qualname__}({', '.join(kwargs)})"


class DomainIdentityMixin:

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

    def has_id_or_name(self, id_or_name: int | str) -> bool:
        """
        Return whether this domain has the same id or same name as the other.

        The domain calling this method MUST be a bound domain or be populated, otherwise
        the comparison will not work as expected (e.g. the domains are the same but
        cannot be equal, if one provides an id and the other the name).
        """
        values: list[int | str] = []
        if self.id is not None:
            values.append(self.id)
        if self.name is not None:
            values.append(self.name)
        if not values:
            raise ValueError("id or name must be set")

        return id_or_name in values


class Pagination(BaseDomain):
    __api_properties__ = (
        "page",
        "per_page",
        "previous_page",
        "next_page",
        "last_page",
        "total_entries",
    )
    __slots__ = __api_properties__

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
    __api_properties__ = ("pagination",)
    __slots__ = __api_properties__

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
