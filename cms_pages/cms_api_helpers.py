# -*- coding: utf-8 -*-
import asyncio
import logging
from pprint import pformat
from typing import List, Tuple
from urllib.parse import urlparse, urljoin

import requests
from directory_cms_client.client import cms_api_client
from directory_cms_client.helpers import AbstractCMSResponse
from directory_constants.constants import cms

from cms_pages.settings import (
    DIRECTORY_CMS_API_CLIENT_API_KEY,
    DIRECTORY_CMS_API_CLIENT_BASE_URL,
    DIRECTORY_CMS_API_PAGES_ENDPOINT,
)

from directory_cms_client import DirectoryCMSClient


class AsyncDirectoryCMSClient(DirectoryCMSClient):
    """Make CMS Client work with AsyncIO"""

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        pass


def async_cms_client():
    return AsyncDirectoryCMSClient(
        base_url=DIRECTORY_CMS_API_CLIENT_BASE_URL,
        api_key=DIRECTORY_CMS_API_CLIENT_API_KEY,
        sender_id="directory",
        timeout=55,
        service_name=cms.INVEST,
    )


EXRED_PAGE_TYPES = [
    # "export_readiness.GetFinancePage",  # BUG CMS-486
    "export_readiness.PerformanceDashboardNotesPage",
    "export_readiness.PerformanceDashboardPage",
    "export_readiness.PrivacyAndCookiesPage",
    "export_readiness.TermsAndConditionsPage",
]
FAS_PAGE_TYPES = [
    "find_a_supplier.IndustryArticlePage",
    "find_a_supplier.IndustryContactPage",
    "find_a_supplier.IndustryLandingPage",
    "find_a_supplier.IndustryPage",
    "find_a_supplier.LandingPage",
]
INVEST_PAGE_TYPES = [
    "invest.InfoPage",
    "invest.InvestHomePage",
    # "invest.RegionLandingPage",  # CMS-413
    "invest.SectorLandingPage",
    "invest.SectorPage",
    "invest.SetupGuideLandingPage",
    "invest.SetupGuidePage",
]
NON_INVEST_PAGE_TYPES = [] + FAS_PAGE_TYPES + EXRED_PAGE_TYPES
ALL_PAGE_TYPES = [] + FAS_PAGE_TYPES + EXRED_PAGE_TYPES + INVEST_PAGE_TYPES


async def fetch(endpoints: List[str]):
    async_loop = asyncio.get_event_loop()
    async with async_cms_client() as client:
        futures = [
            async_loop.run_in_executor(None, client.get, endpoint)
            for endpoint in endpoints
        ]
        return await asyncio.gather(*futures)


def status_error(expected_status_code: int, response: AbstractCMSResponse):
    return (
        f"{response.raw_response.request.method} {response.raw_response.url} "
        f"returned {response.status_code} instead of expected "
        f"{expected_status_code}\n"
        f"REQ headers: {pformat(response.raw_response.request.headers)}\n"
        f"RSP headers: {pformat(response.raw_response.headers)}"
    )


def get_and_assert(url: str, status_code: int):
    response = requests.get(url)
    msg = f"Expected {status_code} but got {response.status_code} from {url}"
    assert response.status_code == status_code, msg


def get_page_ids_by_type(page_type: str) -> Tuple[List[int], int]:
    page_ids = []

    # get first page of results
    relative_url = DIRECTORY_CMS_API_PAGES_ENDPOINT
    endpoint = f"{relative_url}?type={page_type}"
    response = cms_api_client.get(endpoint)
    total_response_time = response.raw_response.elapsed.total_seconds()
    assert response.status_code == 200, status_error(200, response)

    # get IDs of all pages from the response
    content = response.json()
    page_ids += [page["meta"]["pk"] for page in content["items"]]

    total_count = content["meta"]["total_count"]
    if total_count > len(page_ids):
        print(
            f"Found more than {len(content['items'])} pages of {page_type} "
            f"type. Will fetch details of all remaining pages"
        )
    while len(page_ids) < total_count:
        offset = len(content["items"])
        endpoint = f"{relative_url}?type={page_type}&offset={offset}"
        response = cms_api_client.get(endpoint)
        total_response_time += response.raw_response.elapsed.total_seconds()
        assert response.status_code == 200, status_error(200, response)
        content = response.json()
        page_ids += [page["meta"]["pk"] for page in content["items"]]

    assert len(list(sorted(page_ids))) == total_count
    return page_ids, total_response_time


def get_pages_from_api(page_types: list) -> List[AbstractCMSResponse]:
    page_ids = []
    api_endpoints = []
    responses = []
    for page_type in page_types:
        page_ids_of_type, responses_time = get_page_ids_by_type(page_type)
        count = str(len(page_ids_of_type)).rjust(2, " ")
        print(f"Found {count} {page_type} pages in {responses_time}s")
        page_ids += page_ids_of_type
    base = urljoin(
        DIRECTORY_CMS_API_CLIENT_BASE_URL, DIRECTORY_CMS_API_PAGES_ENDPOINT
    )
    api_endpoints += [f"{base}{page_id}/" for page_id in page_ids]
    loop = asyncio.get_event_loop()
    responses += loop.run_until_complete(fetch(api_endpoints))
    failed = [
        f"{r.raw_response.url} -> {r.status_code}"
        for r in responses
        if r.status_code != 200
    ]
    msg = f"BUG CMS-490: Got non 200 OK response from CMS API for {failed}"
    assert all(r.status_code == 200 for r in responses), msg
    return responses


def invest_find_draft_urls(responses: List[AbstractCMSResponse]) -> List[str]:
    """
    Invest app includes language code in the endpoint rather than using ?lang=
    query param, thus it requires different processing.
    """
    result = []
    for response in responses:
        page = response.json()
        draft_token = page["meta"]["draft_token"]
        if draft_token is not None:
            live_url = response.json()["meta"]["url"]
            parsed = urlparse(live_url)
            languages = response.json()["meta"]["languages"]
            language_codes = [language[0] for language in languages]
            for code in language_codes:
                if code == "en-gb":
                    url = live_url
                else:
                    scheme = parsed.scheme
                    netloc = parsed.netloc
                    url = f"{scheme}://{netloc}/{code}{parsed.path}"
                print(f"INVEST DRAFT URL: {url}")
                if url.endswith("uk-regions/") or url.endswith("uk-regions"):
                    continue

                draft_url = f"{url}?draft_token={draft_token}"

                # this is added because of BUG CMS-416
                if "setup-guide-landing" in url:
                    draft_url = draft_url.replace(
                        "setup-guide-landing", "uk-setup-guide"
                    )
                if "setup-guides" in draft_url:
                    draft_url = draft_url.replace(
                        "setup-guides", "uk-setup-guide"
                    )

                result.append(draft_url)

    return result


def invest_find_published_translated_urls(
    responses: List[AbstractCMSResponse]
) -> List[str]:
    """
    Invest app includes language code in the endpoint rather than using ?lang=
    query param, thus it requires different processing.
    """
    result = []
    for response in responses:
        live_url = response.json()["meta"]["url"]
        parsed = urlparse(live_url)
        lang_codes = [lang[0] for lang in response.json()["meta"]["languages"]]
        for code in lang_codes:

            if code == "en-gb":
                url = live_url
            else:
                url = f"{parsed.scheme}://{parsed.netloc}/{code}{parsed.path}"

            # this is added because of BUG CMS-416
            if "setup-guides" in url:
                url = url.replace("setup-guides", "uk-setup-guide")
            if "setup-guide-landing" in url:
                url = url.replace("setup-guide-landing", "uk-setup-guide")
            if "performance-dashboard-" in url:
                url = url.replace(
                    "performance-dashboard-", "performance-dashboard/"
                )
            # this was added because of CMS-413
            if url.endswith("uk-regions/") or url.endswith("uk-regions"):
                continue

            result.append(url)

    return result


def find_draft_urls(responses: List[AbstractCMSResponse]) -> List[str]:
    result = []
    for response in responses:
        if response.status_code == 200:
            page = response.json()
            draft_token = page["meta"]["draft_token"]
            if draft_token is not None:
                url = page["meta"]["url"]
                draft_url = f"{url}?draft_token={draft_token}"
                lang_codes = [lang[0] for lang in page["meta"]["languages"]]
                for code in lang_codes:
                    lang_url = f"{draft_url}&lang={code}"
                    result.append(lang_url)
        else:
            logging.error(
                f"Expected 200 but got {response.status_code} from "
                f"{response.raw_response.url}"
            )
    return result


def check_for_special_cases(url: str) -> str:
    # this was added because of BUG CMS-416
    if "setup-guides" in url:
        url = url.replace("setup-guides", "uk-setup-guide")
    if "setup-guide-landing" in url:
        url = url.replace("setup-guide-landing", "uk-setup-guide")
    if "performance-dashboard-" in url:
        url = url.replace("performance-dashboard-", "performance-dashboard/")
    return url


def find_published_urls(responses: List[AbstractCMSResponse]) -> List[str]:
    result = []
    for response in responses:
        page = response.json()
        url = check_for_special_cases(page["meta"]["url"])
        # this was added because of CMS-413
        if url.endswith("uk-regions/") or url.endswith("uk-regions"):
            continue
        result.append(url)
    return result


def find_published_translated_urls(
    responses: List[AbstractCMSResponse]
) -> List[str]:
    result = []
    for response in responses:
        page = response.json()
        url = check_for_special_cases(page["meta"]["url"])
        lang_codes = [lang[0] for lang in page["meta"]["languages"]]
        # this was added because of CMS-413
        if url.endswith("uk-regions/") or url.endswith("uk-regions"):
            continue
        for code in lang_codes:
            lang_url = "{}?lang={}".format(url, code)
            result.append(lang_url)
    return result


INVEST_API_PAGES = get_pages_from_api(INVEST_PAGE_TYPES)
NON_INVEST_API_PAGES = get_pages_from_api(NON_INVEST_PAGE_TYPES)
ALL_API_PAGES = [] + INVEST_API_PAGES + NON_INVEST_API_PAGES
