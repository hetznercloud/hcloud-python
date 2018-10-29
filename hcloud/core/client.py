# -*- coding: utf-8 -*-
class ClientEntityBase(object):

    def __init__(self, client):
        self._client = client


class BoundModelBase(object):
    model = None

    def __init__(self, client, data={}, complete=True):
        self._client = client
        self.complete = complete
        self.data_model = self.model(**data)

    def __getattr__(self, name):
        value = getattr(self.data_model, name)
        if not value and not self.complete:
            self.reload()
            value = getattr(self.data_model, name)
        return value

    def reload(self):
        bound_model = self._client.get_by_id(self.data_model.id)
        self.data_model = bound_model.data_model
        self.complete = True
