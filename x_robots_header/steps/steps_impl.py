from collections import namedtuple
from retrying import retry

import requests
from behave.runner import Context
from urllib.parse import urljoin
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


RequestResults = namedtuple(
                    "RequestResults",
                    ["service", "environment", "endpoint", "url", "headers"]
                )

SERVICES = {
    "invest": {
        "dev": "https://dev.invest.directory.uktrade.io/",
        "prod": "https://invest.great.gov.uk/",
    },
    "fas": {
        "dev": "https://dev.supplier.directory.uktrade.io/",
        "stage": "https://stage.supplier.directory.uktrade.io/",
        "prod": "https://trade.great.gov.uk/",
    },
    "fab": {
        "dev": "https://dev.buyer.directory.uktrade.io/",
        "stage": "https://stage.buyer.directory.uktrade.io/",
        "prod": "https://find-a-buyer.export.great.gov.uk/",
    },
    "exread": {
        "dev": "https://dev.exportreadiness.directory.uktrade.io/",
        "stage": "https://stage.exportreadiness.directory.uktrade.io/",
        "prod": "https://www.great.gov.uk/",
    },
    "sso": {
        "dev": "https://dev.sso.uktrade.io/",
        "stage": "https://stage.sso.uktrade.io/",
        "prod": "https://sso.trade.great.gov.uk/",
    },
    "soo": {
        "dev": "https://enav-navigator-dev.cloudapps.digital",
        "stage": "https://selling-online-overseas.export.staging.uktrade.io/",
        "prod": "https://selling-online-overseas.export.great.gov.uk/",
    },
    "profile": {
        "dev": "https://dev.profile.uktrade.io/",
        "stage": "https://stage.profile.uktrade.io/",
        "prod": "https://profile.great.gov.uk/",
    },
    "exopps": {
        "dev": "https://export-opportunities-continuous-deployment.cloudapps.digital/",
        "stage": "https://export-opportunities-staging.cloudapps.digital/",
        "prod": "https://opportunities.export.great.gov.uk/",
    },
    "contact-us": {
        "stage": "https://contact-us.export.staging.uktrade.io",
        "prod": "https://contact-us.export.great.gov.uk/",
    },
}


def retry_if_network_error(exception: Exception) -> bool:
    return isinstance(exception, (Timeout, ConnectionError, TooManyRedirects))


@retry(
    wait_fixed=10000,
    stop_max_attempt_number=2,
    retry_on_exception=retry_if_network_error,
    wrap_exception=False,
)
def visit_page(
    context: Context, service: str, environment: str, endpoint: str
):
    host = SERVICES[service.lower()][environment.lower()]
    url = urljoin(host, endpoint)
    headers = requests.get(url).headers
    context.result = RequestResults(
        service, environment, endpoint, url, headers)


def response_should_not_contain_header(context: Context, header: str):
    assert ":" in header, "Please separate header name with its value with ':'"
    result = context.result
    url = result.url
    headers = {key.lower(): value for key, value in result.headers.items()}
    header_name, header_value = header.split(":")
    error_msg = (f"'{header_name}' is present in the response headers from: "
                 f"{url}: {headers}")
    assert header_name.lower() not in headers, error_msg
 

def response_should_contain_header(context: Context, header: str):
    assert ":" in header, "Please separate header name with its value with ':'"
    result = context.result
    url = result.url
    headers = {key.lower(): value for key, value in result.headers.items()}
    header_name, header_value = header.split(":")
    error_msg = (f"'{header_name}' is not present in the response headers from"
                 f": {url}: {headers}")
    assert header_name.lower() in headers, error_msg
    assert header_value.strip().lower() == headers[header_name.lower()]
