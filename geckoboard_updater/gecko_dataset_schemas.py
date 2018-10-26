# -*- coding: utf-8 -*-
from collections import namedtuple
from enum import Enum


Schema = namedtuple("Schema", ["dataset_id", "fields", "unique_by"])

DATE_LABEL_QUANTITY = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "label": {"type": "string", "name": "Label", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
DATE_QUANTITY = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
DATE_AUTO_MANUAL = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "auto": {"type": "number", "name": "Automated", "optional": False},
    "manual": {"type": "number", "name": "Manually", "optional": False},
}
DATE_ENVIRONMENT_ERRORS_FAILURES_SCANNED = {
    "date": {"type": "datetime", "name": "Date", "optional": False},
    "environment": {"type": "string", "name": "Environment", "optional": False},
    "errors": {"type": "number", "name": "Errors", "optional": False},
    "failures": {"type": "number", "name": "Failures", "optional": False},
    "tests": {"type": "number", "name": "Tests", "optional": False},
}

# values can be optional
# it allows for sending results for endpoints that returned failures
LOCUST_RESULTS_DISTRIBUTION = {
    "date": {"type": "datetime", "name": "Date", "optional": False},
    "name": {"type": "string", "name": "Name", "optional": False},
    "requests": {"type": "number", "name": "# requests", "optional": True},
    "50": {"type": "number", "name": "50%", "optional": True},
    "75": {"type": "number", "name": "75%", "optional": True},
    "90": {"type": "number", "name": "90%", "optional": True},
    "95": {"type": "number", "name": "95%", "optional": True},
    "98": {"type": "number", "name": "98%", "optional": True},
    "99": {"type": "number", "name": "99%", "optional": True},
    "100": {"type": "number", "name": "100%", "optional": True},
}
LOCUST_RESULTS_REQUESTS = {
    "date": {"type": "datetime", "name": "Date", "optional": False},
    "name": {"type": "string", "name": "Name", "optional": False},
    "requests": {"type": "number", "name": "# requests", "optional": True},
    "failures": {"type": "number", "name": "Failures", "optional": True},
    "median_response_time": {"type": "number", "name": "Med resp time", "optional": True},
    "average_response_time": {"type": "number", "name": "Avg resp time", "optional": True},
    "min_response_time": {"type": "number", "name": "Min resp time", "optional": True},
    "max_response_time": {"type": "number", "name": "Max resp time", "optional": True},
    "average_content_size": {"type": "number", "name": "Avg content size", "optional": True},
    "requests_per_s": {"type": "number", "name": "RPS", "optional": True},
}
DATE = ["date"]
DATE_ENVIRONMENT = ["date", "environment"]
DATE_LABEL = ["date", "label"]
DATE_NAME = ["date", "name"]


def bugs_on_board_by_labels(team: str) -> Schema:
    """Number of bugs on the Kanban/Sprint board grouped by labels"""
    return Schema(
        dataset_id=f"{team}.bugs_on_board_by_labels",
        fields=DATE_LABEL_QUANTITY,
        unique_by=DATE_LABEL
    )


def unlabelled_bugs_on_board(team: str) -> Schema:
    """Number of bugs on Kanban/Sprint board without a `qa_*` label"""
    return Schema(
        dataset_id=f"{team}.unlabelled_bugs_on_board",
        fields=DATE_QUANTITY,
        unique_by=DATE
    )


def bugs_in_backlog_by_labels(team: str) -> Schema:
    """Number of bugs in the backlog grouped by labels"""
    return Schema(
        dataset_id=f"{team}.bugs_in_backlog_by_labels",
        fields=DATE_LABEL_QUANTITY,
        unique_by=DATE_LABEL,
    )


def unlabelled_bugs_in_backlog(team: str) -> Schema:
    """Number of bugs in backlog without a `qa_*` label"""
    return Schema(
        dataset_id=f"{team}.unlabelled_bugs_in_backlog",
        fields=DATE_QUANTITY,
        unique_by=DATE,
    )


def bugs_in_backlog(team: str) -> Schema:
    """Number of all bugs in backlog"""
    return Schema(
        dataset_id=f"{team}.bugs_in_backlog",
        fields=DATE_QUANTITY,
        unique_by=DATE,
    )


def bugs_auto_vs_manual(team: str) -> Schema:
    """Number of bugs on the Kanban/Sprint board discovered manually or by
    automated tests"""
    return Schema(
        dataset_id=f"{team}.bugs_auto_vs_manual",
        fields=DATE_AUTO_MANUAL,
        unique_by=DATE,
    )


def bugs_closed_today(team: str) -> Schema:
    """Number of bugs closed today"""
    return Schema(
        dataset_id=f"{team}.bugs_closed_today",
        fields=DATE_QUANTITY,
        unique_by=DATE,
    )


def tickets_closed_today(team: str) -> Schema:
    """Number of tickets (without bugs) closed today"""
    return Schema(
        dataset_id=f"{team}.tickets_closed_today",
        fields=DATE_QUANTITY,
        unique_by=DATE,
    )


def tickets_on_board(team: str) -> Schema:
    """Number of tickets (with bugs) on Sprint/Kanban board"""
    return Schema(
        dataset_id=f"{team}.tickets_on_board",
        fields=DATE_QUANTITY,
        unique_by=DATE,
    )


def bugs_per_service(team: str) -> Schema:
    """Number of bugs per service (only for tickets with appropriate tags)"""
    return Schema(
        dataset_id=f"{team}.bugs_per_service",
        fields=DATE_LABEL_QUANTITY,
        unique_by=DATE_LABEL,
    )


def bad_links_per_environment(team: str) -> Schema:
    """Number of bad (dead or invalid) links per environment"""
    return Schema(
        dataset_id=f"{team}.bad_links_per_environment",
        fields=DATE_ENVIRONMENT_ERRORS_FAILURES_SCANNED,
        unique_by=DATE_ENVIRONMENT,
    )


def content_diffs_per_environment(team: str) -> Schema:
    """Number of content differences per service per environment"""
    return Schema(
        dataset_id=f"{team}.content_diffs_per_environment",
        fields=DATE_ENVIRONMENT_ERRORS_FAILURES_SCANNED,
        unique_by=DATE_ENVIRONMENT,
    )


def bad_cms_pages_per_environment(team: str) -> Schema:
    """Number of bad CMS pages per environment"""
    return Schema(
        dataset_id=f"{team}.bad_cms_pages_per_environment",
        fields=DATE_ENVIRONMENT_ERRORS_FAILURES_SCANNED,
        unique_by=DATE_ENVIRONMENT,
    )


def load_tests_result_distribution(environment: str, service: str) -> Schema:
    """Load test (locustio) result (percentile) distribution"""
    return Schema(
        dataset_id=f"load_tests.result_distribution_{environment}_{service}",
        fields=LOCUST_RESULTS_DISTRIBUTION,
        unique_by=DATE_NAME,
    )


def load_tests_result_requests(environment: str, service: str) -> Schema:
    """Load test (locustio) requests requests"""
    return Schema(
        dataset_id=f"load_tests.result_requests_{environment}_{service}",
        fields=LOCUST_RESULTS_REQUESTS,
        unique_by=DATE_NAME,
    )


class ContentDatasetSchemas(Enum):
    """Content Team Geckoboard Dataset schemas"""
    BAD_CMS_PAGES_PER_ENVIRONMENT = bad_cms_pages_per_environment("content")
    BAD_LINKS_PER_ENVIRONMENT = bad_links_per_environment("content")
    BUGS_AUTO_VS_MANUAL = bugs_auto_vs_manual("content")
    BUGS_CLOSED_TODAY = bugs_closed_today("content")
    BUGS_IN_BACKLOG = bugs_in_backlog("content")
    BUGS_IN_BACKLOG_BY_LABELS = bugs_in_backlog_by_labels("content")
    BUGS_ON_BOARD_BY_LABELS = bugs_on_board_by_labels("content")
    BUGS_PER_SERVICE = bugs_per_service("content")
    PAGE_DIFFS_PER_ENVIRONMENT = content_diffs_per_environment("content")
    TICKETS_CLOSED_TODAY = tickets_closed_today("content")
    TICKETS_ON_BOARD = tickets_on_board("content")
    UNLABELLED_BUGS_IN_BACKLOG = unlabelled_bugs_in_backlog("content")
    UNLABELLED_BUGS_ON_BOARD = unlabelled_bugs_on_board("content")


class ToolsDatasetSchemas(Enum):
    """Tools Team Geckoboard Dataset schemas"""
    BUGS_AUTO_VS_MANUAL = bugs_auto_vs_manual("tools")
    BUGS_CLOSED_TODAY = bugs_closed_today("tools")
    BUGS_IN_BACKLOG = bugs_in_backlog("tools")
    BUGS_IN_BACKLOG_BY_LABELS = bugs_in_backlog_by_labels("tools")
    BUGS_ON_BOARD_BY_LABELS = bugs_on_board_by_labels("tools")
    BUGS_PER_SERVICE = bugs_per_service("tools")
    TICKETS_CLOSED_TODAY = tickets_closed_today("tools")
    TICKETS_ON_BOARD = tickets_on_board("tools")
    UNLABELLED_BUGS_IN_BACKLOG = unlabelled_bugs_in_backlog("tools")
    UNLABELLED_BUGS_ON_BOARD = unlabelled_bugs_on_board("tools")

    LOAD_TESTS_STAGE_CMS_RESULT_DISTRIBUTION = load_tests_result_distribution("stage", "cms")
    LOAD_TESTS_STAGE_FAB_RESULT_DISTRIBUTION = load_tests_result_distribution("stage", "fab")
    LOAD_TESTS_STAGE_FAS_RESULT_DISTRIBUTION = load_tests_result_distribution("stage", "fas")
    LOAD_TESTS_STAGE_INVEST_RESULT_DISTRIBUTION = load_tests_result_distribution("stage", "invest")

    LOAD_TESTS_STAGE_CMS_RESULT_REQUESTS = load_tests_result_requests("stage", "cms")
    LOAD_TESTS_STAGE_FAB_RESULT_REQUESTS = load_tests_result_requests("stage", "fab")
    LOAD_TESTS_STAGE_FAS_RESULT_REQUESTS = load_tests_result_requests("stage", "fas")
    LOAD_TESTS_STAGE_INVEST_RESULT_REQUESTS = load_tests_result_requests("stage", "invest")
