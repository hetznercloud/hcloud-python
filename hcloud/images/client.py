# -*- coding: utf-8 -*-
from hcloud.core.client import BoundModelBase

from hcloud.images.domain import Image


class BoundImage(BoundModelBase):
    model = Image
