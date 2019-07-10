import datetime
from dateutil.tz import tzoffset

from hcloud.actions.domain import Action


class TestAction(object):

    def test_started_finished_is_datetime(self):
        action = Action(id=1, started="2016-01-30T23:50+00:00", finished="2016-03-30T23:50+00:00")
        assert action.started == datetime.datetime(2016, 1, 30, 23, 50, tzinfo=tzoffset(None, 0))
        assert action.finished == datetime.datetime(2016, 3, 30, 23, 50, tzinfo=tzoffset(None, 0))
