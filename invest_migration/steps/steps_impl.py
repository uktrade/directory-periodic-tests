# -*- coding: utf-8 -*-
import difflib
from typing import List
from urllib.parse import urljoin

import requests
from behave.runner import Context
from bs4 import BeautifulSoup
from retrying import retry
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


SITES = {
    "dev": "https://dev.invest.directory.uktrade.io/",
    "prod": "https://invest.great.gov.uk/"
}


def retry_if_network_error(exception: Exception) -> bool:
    return isinstance(exception, (Timeout, ConnectionError, TooManyRedirects))


def get_text(content: str, section_name: str) -> List[str]:
    soup = BeautifulSoup(content, "lxml")
    section = soup.find(section_name)

    for element in section.findAll(["script", "css", "img", "style"]):
        element.extract()
    for element in section.select("#beta-bar"):
        element.extract()

    lines = [
        line.strip()
        for line in section.get_text().splitlines()
        if line.strip()
    ]

    return lines


@retry(
    wait_fixed=30000,
    stop_max_attempt_number=3,
    retry_on_exception=retry_if_network_error,
    wrap_exception=False,
)
def extract_page_content(
        context: Context, section: str, endpoint: str, site_a: str, site_b: str):
    site_a = SITES[site_a.lower()]
    site_b = SITES[site_b.lower()]
    url_a = urljoin(site_a, endpoint)
    url_b = urljoin(site_b, endpoint)

    content_a = requests.get(url_a).content
    content_b = requests.get(url_b).content

    text_a = get_text(content_a, section)
    text_b = get_text(content_b, section)

    contents = {
        "endpoint": endpoint,
        "site_a": {
            "site": site_a,
            "url": url_a,
            "text": text_a,
        },
        "site_b": {
            "site": site_b,
            "url": url_b,
            "text": text_b,
        },
    }

    context.contents = contents


def look_for_differences(context):
    contents = context.contents
    endpoint = contents["endpoint"]
    url_a = contents["site_a"]["url"]
    url_b = contents["site_b"]["url"]
    text_a = contents["site_a"]["text"]
    text_b = contents["site_b"]["text"]
    from_desc_url_a = f"<a href='{url_a}' target=_blank>{url_a}</a>"
    from_desc_url_b = f"<a href='{url_b}' target=_blank>{url_b}</a>"
    html = difflib.HtmlDiff(tabsize=4, wrapcolumn=120).make_file(
        text_a, text_b, fromdesc=from_desc_url_a, todesc=from_desc_url_b,
        context=True, numlines=1)

    clean_endpoint = endpoint[1:-1].replace("/", "_")
    clean_endpoint = clean_endpoint or "home"
    report_name = "./reports/{}.html".format(clean_endpoint)
    with open(report_name, "w") as file:
        file.write(html)
    no_differences = "No Differences Found" in html
    assert no_differences, f"Found differences on {endpoint} see {report_name}"
