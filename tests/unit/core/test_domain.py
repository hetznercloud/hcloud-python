import pytest
from dateutil.parser import isoparse

from hcloud.core.domain import (
    BaseDomain,
    DomainIdentityMixin,
    Meta,
    Pagination,
    add_meta_to_result,
)


class TestMeta(object):
    @pytest.mark.parametrize("json_content", [None, "", {}])
    def test_parse_meta_empty_json(self, json_content):
        result = Meta.parse_meta(json_content)
        assert result is None

    def test_parse_meta_json_no_paginaton(self):
        json_content = {"meta": {}}
        result = Meta.parse_meta(json_content)
        assert isinstance(result, Meta)
        assert result.pagination is None

    def test_parse_meta_json_ok(self):
        json_content = {
            "meta": {
                "pagination": {
                    "page": 2,
                    "per_page": 10,
                    "previous_page": 1,
                    "next_page": 3,
                    "last_page": 10,
                    "total_entries": 100,
                }
            }
        }
        result = Meta.parse_meta(json_content)
        assert isinstance(result, Meta)
        assert isinstance(result.pagination, Pagination)
        assert result.pagination.page == 2
        assert result.pagination.per_page == 10
        assert result.pagination.next_page == 3
        assert result.pagination.last_page == 10
        assert result.pagination.total_entries == 100

    def test_add_meta_to_result(self):
        json_content = {
            "meta": {
                "pagination": {
                    "page": 2,
                    "per_page": 10,
                    "previous_page": 1,
                    "next_page": 3,
                    "last_page": 10,
                    "total_entries": 100,
                }
            }
        }
        result = add_meta_to_result([1, 2, 3], json_content, "id_list")
        assert result.id_list == [1, 2, 3]
        assert result.meta.pagination.page == 2
        assert result.meta.pagination.per_page == 10
        assert result.meta.pagination.next_page == 3
        assert result.meta.pagination.last_page == 10
        assert result.meta.pagination.total_entries == 100


class SomeDomain(BaseDomain, DomainIdentityMixin):
    __slots__ = ("id", "name")

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name


class TestDomainIdentityMixin(object):
    @pytest.mark.parametrize(
        "domain,expected_result",
        [
            (SomeDomain(id=1, name="name"), 1),
            (SomeDomain(id=1), 1),
            (SomeDomain(name="name"), "name"),
        ],
    )
    def test_id_or_name_ok(self, domain, expected_result):
        assert domain.id_or_name == expected_result

    def test_id_or_name_exception(self):
        domain = SomeDomain()

        with pytest.raises(ValueError) as exception_info:
            domain.id_or_name
        error = exception_info.value
        assert str(error) == "id or name must be set"


class ActionDomain(BaseDomain, DomainIdentityMixin):
    __slots__ = ("id", "name", "started")

    def __init__(self, id, name="name1", started=None):
        self.id = id
        self.name = name
        self.started = isoparse(started) if started else None


class TestBaseDomain(object):
    @pytest.mark.parametrize(
        "data_dict,expected_result",
        [
            ({"id": 1}, {"id": 1, "name": "name1", "started": None}),
            ({"id": 2, "name": "name2"}, {"id": 2, "name": "name2", "started": None}),
            (
                {"id": 3, "foo": "boo", "description": "new"},
                {"id": 3, "name": "name1", "started": None},
            ),
            (
                {
                    "id": 4,
                    "foo": "boo",
                    "description": "new",
                    "name": "name-name3",
                    "started": "2016-01-30T23:50+00:00",
                },
                {
                    "id": 4,
                    "name": "name-name3",
                    "started": isoparse("2016-01-30T23:50+00:00"),
                },
            ),
        ],
    )
    def test_from_dict_ok(self, data_dict, expected_result):
        model = ActionDomain.from_dict(data_dict)
        for k, v in expected_result.items():
            assert getattr(model, k) == v
