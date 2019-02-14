# -*- coding: utf-8 -*-
from dateutil.parser import isoparse


class ISODateTime(object):
    def __init__(self, initval=None):
        self.val = initval

    def __get__(self, obj, obj_type):
        return self.val

    def __set__(self, obj, string_date):
        if string_date is None:
            self.val = None
        else:
            # 2016-01-30T23:50+00:00
            self.val = isoparse(string_date)
