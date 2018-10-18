# -*- coding: utf-8 -*-
import pytest

from cms_pages.cms_api_helpers import (
    find_published_translated_urls,
    find_published_urls,
    get_and_assert,
    invest_find_published_translated_urls,
    ALL_API_PAGES,
    INVEST_API_PAGES,
    NON_INVEST_API_PAGES,
)


@pytest.mark.parametrize("url", find_published_urls(ALL_API_PAGES))
def test_all_published_english_pages_should_return_200(url):
    get_and_assert(url, 200)


@pytest.mark.parametrize(
    "url", find_published_translated_urls(NON_INVEST_API_PAGES)
)
def test_non_invest_published_translated_pages_should_return_200_new(url):
    get_and_assert(url, 200)


@pytest.mark.parametrize(
    "url", invest_find_published_translated_urls(INVEST_API_PAGES)
)
def test_published_and_translated_invest_pages_should_return_200_new(url):
    get_and_assert(url, 200)
