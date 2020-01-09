# -*- coding: utf-8 -*-
from collections import namedtuple


class BaseDomain(object):
    __slots__ = ()

    @classmethod
    def from_dict(cls, data):
        supported_data = {k: v for k, v in data.items() if k in cls.__slots__}
        return cls(**supported_data)


class DomainIdentityMixin(object):
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

    def __init__(self, page, per_page, previous_page=None, next_page=None, last_page=None, total_entries=None):
        self.page = page
        self.per_page = per_page
        self.previous_page = previous_page
        self.next_page = next_page
        self.last_page = last_page
        self.total_entries = total_entries


class Meta(BaseDomain):

    __slots__ = (
        "pagination",
    )

    def __init__(
        self,
        pagination=None,
    ):
        self.pagination = pagination

    @classmethod
    def parse_meta(cls, json_content):
        meta = None
        if json_content and "meta" in json_content:
            meta = cls()
            pagination_json = json_content['meta'].get("pagination")
            if pagination_json:
                pagination = Pagination(**pagination_json)
                meta.pagination = pagination
        return meta


def add_meta_to_result(result, json_content, attr_name):
    # type: (List[BoundModelBase], json, string) -> PageResult
    class_name = 'PageResults{0}'.format(attr_name.capitalize())
    PageResults = namedtuple(class_name, [attr_name, 'meta'])
    return PageResults(**{
        attr_name: result,
        'meta': Meta.parse_meta(json_content)
    })
