# -*- coding: utf-8 -*-
import arrow


class ISODateTime(object):
    def __init__(self, initval=None):
        self.val = initval

    def __get__(self, obj, obj_type):
        return self.val

    def __set__(self, obj, string_date):
        if string_date is None:
            self.val = None
        else:
            try:
                self.val = arrow.get(string_date).datetime
            except arrow.parser.ParserError:
                raise ValueError('invalid date format')
