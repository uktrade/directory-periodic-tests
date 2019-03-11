from collections import namedtuple
from retrying import retry

import requests
from behave.runner import Context
from urllib.parse import urljoin
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

BASICAUTH_USER_DEV = os.environ["BASICAUTH_USER_DEV"]
BASICAUTH_PASS_DEV = os.environ["BASICAUTH_PASS_DEV"]
BASICAUTH_USER_STAGE = os.environ["BASICAUTH_USER_STAGE"]
BASICAUTH_PASS_STAGE = os.environ["BASICAUTH_PASS_STAGE"]

RequestResults = namedtuple(
                    "RequestResults",
                    ["service", "environment", "endpoint", "url", "headers"]
                )

SERVICES = {
    "invest": {
        "dev": "https://invest.great.dev.uktrade.io/",
        "stage": "https://invest.great.staging.uktrade.io/",
        "prod": "https://invest.great.gov.uk/",
    },
    "fas": {
        "dev": "https://great.dev.uktrade.io/trade/",
        "stage": "https://great.staging.uktrade.io/trade/",
        "prod": "https://www.great.gov.uk/trade/",
    },
    "fab": {
        "dev": "https://great.dev.uktrade.io/find-a-buyer/",
        "stage": "https://great.staging.uktrade.io/find-a-buyer/",
        "prod": "https://find-a-buyer.export.great.gov.uk/",
    },
    "exread": {
        "dev": "https://great.dev.uktrade.io/",
        "stage": "https://great.staging.uktrade.io/",
        "prod": "https://www.great.gov.uk/",
    },
    "sso": {
        "dev": "https://great.dev.uktrade.io/sso/",
        "stage": "https://great.staging.uktrade.io/sso/",
        "prod": "https://sso.trade.great.gov.uk/",
    },
    "soo": {
        "dev": "https://selling-online-overseas.export.great.dev.uktrade.io/",
        "stage": "https://selling-online-overseas.export.great.staging.uktrade.io/",
        "prod": "https://selling-online-overseas.export.great.gov.uk/",
    },
    "profile": {
        "dev": "https://great.dev.uktrade.io/profile/",
        "stage": "https://great.staging.uktrade.io/profile/",
        "prod": "https://profile.great.gov.uk/",
    },
    "exopps": {
        "dev": "https://export-opportunities-continuous-deployment.cloudapps.digital/",
        "stage": "https://opportunities.export.great.staging.uktrade.io/",
        "prod": "https://opportunities.export.great.gov.uk/",
    },
}


def retry_if_network_error(exception: Exception) -> bool:
    return isinstance(exception, (Timeout, ConnectionError, TooManyRedirects))


def basic_auth(env: str):
    if env.lower() == "dev":
        return BASICAUTH_USER_DEV, BASICAUTH_PASS_DEV
    elif env.lower() == "stage":
        return BASICAUTH_USER_STAGE, BASICAUTH_PASS_STAGE
    else:
        return None


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
    response = requests.get(url, auth=basic_auth(environment))
    error = f"Expected 200 got {response.status_code} from {response.url}"
    assert response.status_code == 200, error
    headers = response.headers
    context.result = RequestResults(service, environment, endpoint, url, headers)


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
