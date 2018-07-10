# -*- coding: utf-8 -*-
from pprint import pformat

import pytest
import requests

from cms_pages import get_page_ids_by_type
from cms_pages.settings import CMS_API_PAGES_ENDPOINT


@pytest.mark.parametrize(
    "page_type",
    [
        "export_readiness.GetFinancePage",
        "export_readiness.PrivacyAndCookiesPage",
        "export_readiness.TermsAndConditionsPage",
        "find_a_supplier.IndustryArticlePage",
        "find_a_supplier.IndustryContactPage",
        "find_a_supplier.IndustryLandingPage",
        "find_a_supplier.IndustryPage",
        "find_a_supplier.LandingPage",
        "invest.InfoPage",
        "invest.InvestHomePage",
        "invest.RegionLandingPage",
        "invest.SectorLandingPage",
        "invest.SectorPage",
        "invest.SetupGuideLandingPage",
        "invest.SetupGuidePage",
    ],
)
def test_all_published_pages_should_return_200(cms_client, page_type):
    results = []
    page_ids = get_page_ids_by_type(cms_client, page_type)
    for page_id in page_ids:
        url = "{}{}/".format(CMS_API_PAGES_ENDPOINT, page_id)
        try:
            api_response = cms_client.get(url)
        except Exception as ex:
            results.append((page_id, url, str(ex)))
            continue
        if api_response.status_code == 200:
            live_url = api_response.json()["meta"]["url"]
            try:
                live_response = requests.get(live_url)
            except Exception as ex:
                results.append((page_id, live_url, str(ex)))
                continue
            results.append((page_id, live_url, live_response.status_code))
        else:
            print("{} returned {}".format(url, api_response.status_code))
    non_200 = [result for result in results if result[2] != 200]
    template = "Page ID: {} URL: {} Status Code: {}"
    formatted_non_200 = [template.format(*result) for result in non_200]
    error_msg = "{} out of {} published pages of type {} are broken {}".format(
        len(non_200), len(results), page_type, pformat(formatted_non_200)
    )
    assert not non_200, error_msg
