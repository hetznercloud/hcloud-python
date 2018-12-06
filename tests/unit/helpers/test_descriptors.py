import pytest
import datetime
from dateutil.tz import tzoffset

from hcloud.helpers.descriptors import ISODateTime


class TestISODateTime(object):

    @pytest.fixture()
    def entity_with_descriptor(self):

        class TestDesctiptorISODateTime(object):
            created = ISODateTime()

            def __init__(self, created=None):
                self.created = created

        return TestDesctiptorISODateTime

    def test_created_none(self, entity_with_descriptor):
        entity = entity_with_descriptor()
        assert entity.created is None

    def test_created_assigned_valid(self, entity_with_descriptor):
        entity = entity_with_descriptor()
        entity.created = "2016-01-30T23:50+00:00"
        assert entity.created == datetime.datetime(2016, 1, 30, 23, 50, tzinfo=tzoffset(None, 0))

    def test_created_valid(self, entity_with_descriptor):
        entity = entity_with_descriptor(created="2016-01-30T23:50+00:00")
        assert entity.created == datetime.datetime(2016, 1, 30, 23, 50, tzinfo=tzoffset(None, 0))

    def test_created_invalid(self, entity_with_descriptor):
        with pytest.raises(ValueError):
            entity_with_descriptor(created="invalid")
