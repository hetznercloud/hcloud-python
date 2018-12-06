# -*- coding: utf-8 -*-
class BaseDomain(object):
    __slots__ = ()

    @property
    def id_or_name(self):
        if self.id is not None:
            return self.id
        elif self.name is not None:
            return self.name
        else:
            raise ValueError("id or name must be set")
