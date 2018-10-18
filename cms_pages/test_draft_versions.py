# -*- coding: utf-8 -*-
import pytest

from cms_pages.cms_api_helpers import (
    find_draft_urls,
    get_and_assert,
    invest_find_draft_urls,
    NON_INVEST_API_PAGES,
    INVEST_API_PAGES,
)


@pytest.mark.parametrize("url", find_draft_urls(NON_INVEST_API_PAGES))
def test_non_invest_draft_translated_pages_should_return_200(url):
    get_and_assert(url, 200)


@pytest.mark.parametrize("url", invest_find_draft_urls(INVEST_API_PAGES))
def test_draft_translated_invest_pages_should_return_200(url):
    get_and_assert(url, 200)
