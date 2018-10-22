#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `hetznercloud` package."""

import pytest


from hetznercloud import hetznercloud


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
