# -*- coding: utf-8 -*-
from hcloud.core.client import BoundModelBase

from hcloud.iso.domain import Iso


class BoundIso(BoundModelBase):
    model = Iso
