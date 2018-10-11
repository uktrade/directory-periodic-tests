#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import os
import xml.etree.ElementTree as ET
from collections import namedtuple, Counter
from datetime import date, datetime
from typing import List

import requests
from geckoboard.client import Client as GeckoClient
from jira import JIRA as JiraClient
from circleclient import circleclient

# Get credentials from env variables
GECKOBOARD_API_KEY = os.environ["GECKOBOARD_API_KEY"]
GECKOBOARD_TEST_RESULTS_WIDGET_KEY = os.environ[
    "GECKOBOARD_TEST_RESULTS_WIDGET_KEY"
]
GECKOBOARD_PUSH_URL = os.getenv(
    "GECKOBOARD_PUSH_URL", "https://push.geckoboard.com/v1/send/"
)
JIRA_HOST = os.environ["JIRA_HOST"]
JIRA_USERNAME = os.environ["JIRA_USERNAME"]
JIRA_PASSWORD = os.environ["JIRA_PASSWORD"]
CIRCLE_CI_API_TOKEN = os.environ["CIRCLE_CI_API_TOKEN"]

# Instantiate clients
JIRA_CLIENT = JiraClient(JIRA_HOST, auth=(JIRA_USERNAME, JIRA_PASSWORD))
GECKO_CLIENT = GeckoClient(GECKOBOARD_API_KEY)
CIRCLE_CI_CLIENT = circleclient.CircleClient(CIRCLE_CI_API_TOKEN)

# other variables
TODAY = date.today().isoformat()

# Service tags used in Jira to indicate service affected by given bug
SERVICE_TAGS = [
    "admin",
    "api",
    "cms",
    "contact-us",
    "css-components",
    "exopps",
    "exred",
    "fab",
    "fas",
    "gds",
    "header-footer",
    "soo",
    "sso",
    "sso-profile",
    "sso-proxy",
    "sud",
]

# Jira JQL queries
JQL_KANBAN_BUGS = """
project = TT 
AND issuetype = Bug 
AND status != Backlog 
AND status != Done 
ORDER BY created DESC"""

JQL_BACKLOG_BUGS = """
project = TT 
AND issuetype = Bug 
AND status = Backlog 
ORDER BY created DESC"""

JQL_MANUAL_VS_AUTOMATED = """
project = TT 
AND resolution = Unresolved 
AND labels in (qa_auto, qa_manual) 
ORDER BY priority DESC, updated DESC"""

JQL_SCENARIOS_TO_AUTOMATE = """
project = TT 
AND issuetype in (Task, Sub-task) 
AND resolution = Unresolved 
AND labels = qa_automated_scenario 
ORDER BY created DESC"""

JQL_BUGS_CLOSED_TODAY = """
PROJECT in (TT) 
AND issuetype = Bug 
AND Status CHANGED FROM (Backlog, Planning, "Blocked!", "Design To Do", 
"Design - ready", "Design - in Progress", "Sign-off", "User research", 
"Dev - Planning", "Dev - selected", "Dev To Do", "Dev - ready", 
"Dev - in progress", "Dev - code review", Testing) 
TO (Closed, Done, "Release Candidate", Release) 
DURING (-0d, now()) 
ORDER BY key ASC, updated DESC
"""

JQL_TICKETS_CLOSED_TODAY = """
PROJECT in (TT) 
AND issuetype != Bug 
AND Status CHANGED FROM (Backlog, Planning, "Blocked!", "Design To Do", 
"Design - ready", "Design - in Progress", "Sign-off", "User research", 
"Dev - Planning", "Dev - selected", "Dev To Do", "Dev - ready", 
"Dev - in progress", "Dev - code review", Testing) 
TO (Closed, Done, "Release Candidate", Release) 
DURING (-0d, now()) 
ORDER BY key ASC, updated DESC
"""

JQL_BUGS_PER_SERVICE = """
project = TT 
AND issuetype = Bug 
AND labels IN ({service_tags})
AND created >= "-90d"
ORDER BY labels DESC, priority DESC, updated DESC
""".format(
    service_tags=", ".join(SERVICE_TAGS)
)


# Mapping of CircleCI job names to more human friendly ones
CIRCLE_CI_DIRECTORY_TESTS_WORKFLOW_JOB_NAME_MAPPINGS = {
    "browser_tests_chrome": "Chrome",
    "browser_tests_firefox": "Firefox",
    "fab_functional_tests": "FAB",
    "fas_functional_tests": "FAS",
    "smoke_tests": "Smoke",
    "sso_functional_tests": "SSO",
    "sud_functional_tests": "SUD",
}

CIRCLE_CI_DIRECTORY_WORKFLOW_JOB_NAME_MAPPINGS = {
    "test": "Unit Tests",
    "deploy_to_dev": "Deploy to Dev",
    "integration_tests": "Integration Tests",
}

CIRCLE_CI_DIRECTORY_CH_SEARCH_WORKFLOW_JOB_NAME_MAPPINGS = {
    "test": "Unit Tests",
}


DIRECTORY_PROJECTS_WITH_WORKFLOW = [
    "API",
    "ExRed",
    "FAB",
    "FAS",
    "SSO Proxy",
    "SSO",
    "SUD",
]


# Geckoboard datasets

###############################################################################
# KANBAN BOARD
###############################################################################
# Number of bugs on the Kanban board grouped by label (not in Backlog or Done)
DATASET_ON_KANBAN_BY_LABELS_NAME = "export.bugs_wip_by_labels"
DATASET_ON_KANBAN_BY_LABELS_FIELDS = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "label": {"type": "string", "name": "Label", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
DATASET_ON_KANBAN_BY_LABELS_UNIQUE_BY = ["date", "label"]

# Number of bugs on Kanban board without a `qa_*` label
DATASET_UNLABELLED_ON_KANBAN_NAME = "export.bugs_unlabelled"
DATASET_UNLABELLED_ON_KANBAN_FIELDS = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
DATASET_UNLABELLED_ON_KANBAN_UNIQUE_BY = ["date"]

###############################################################################
# BACKLOG
###############################################################################

# Number of bugs in the Backlog board grouped by label (not in Backlog or Done)
DATASET_BUGS_IN_BACKLOG_BY_LABELS_NAME = "export.bugs_in_backlog_by_labels"
DATASET_BUGS_IN_BACKLOG_BY_LABELS_FIELDS = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "label": {"type": "string", "name": "Label", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
DATASET_BUGS_IN_BACKLOG_BY_LABELS_UNIQUE_BY = ["date", "label"]

# Number of bugs in Backlog without a `qa_*` label
DATASET_UNLABELLED_IN_BACKLOG_NAME = "export.bugs_unlabelled_in_backlog"
DATASET_UNLABELLED_IN_BACKLOG_FIELDS = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
DATASET_UNLABELLED_IN_BACKLOG_UNIQUE_BY = ["date"]

# Number of bugs in the Backlog
DATASET_BUGS_IN_BACKLOG_NAME = "export.bugs_in_backlog"
DATASET_BUGS_IN_BACKLOG_FIELDS = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
DATASET_BUGS_IN_BACKLOG_UNIQUE_BY = ["date"]

###############################################################################
# OTHER
###############################################################################

# Number of scenarios to automate (tagged with `qa_automated_scenario`)
DATASET_TO_AUTOMATE_NAME = "export.scenarios_to_automate"
DATASET_TO_AUTOMATE_FIELDS = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
DATASET_TO_AUTOMATE_UNIQUE_BY = ["date"]

# Number of bugs on the Kanban board discovered manually or by automated tests
DATASET_VS_NAME = "export.bugs_auto_vs_manual"
DATASET_VS_FIELDS = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "auto": {"type": "number", "name": "automated tests", "optional": False},
    "manual": {"type": "number", "name": "manually", "optional": False},
}
DATASET_VS_UNIQUE_BY = ["date"]

# Number of bugs closed today (moved to Close, Release or Release Candidate)
DATASET_BUGS_CLOSED_TODAY_NAME = "export.bugs_closed_today"
DATASET_BUGS_CLOSED_TODAY_FIELDS = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "closed": {
        "type": "number",
        "name": "Bugs closed today",
        "optional": False,
    },
}
DATASET_BUGS_CLOSED_TODAY_UNIQUE_BY = ["date"]

# Number of tickets (without bugs) closed today (moved to Close, Release
# or Release Candidate)
DATASET_TICKETS_CLOSED_TODAY_NAME = "export.tickets_closed_today"
DATASET_TICKETS_CLOSED_TODAY_FIELDS = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "closed": {
        "type": "number",
        "name": "Tickets closed today",
        "optional": False,
    },
}
DATASET_TICKETS_CLOSED_TODAY_UNIQUE_BY = ["date"]

# Number of bugs per service (only counts tickets with appropriate tags)
DATASET_BUGS_PER_SERVICE_NAME = "export.bugs_per_service"
DATASET_BUGS_PER_SERVICE_FIELDS = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "service": {"type": "string", "name": "Service", "optional": False},
    "quantity": {"type": "number", "name": "Quantity", "optional": False},
}
DATASET_BUGS_PER_SERVICE_UNIQUE_BY = ["date", "service"]

# Number of bad (dead or invalid) links per environment
DATASET_BAD_LINKS_PER_ENVIRONMENT_NAME = "export.bad_links_per_environment"
DATASET_BAD_LINKS_PER_ENVIRONMENT_FIELDS = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "environment": {
        "type": "string",
        "name": "Environment",
        "optional": False,
    },
    "errors": {"type": "number", "name": "Errors", "optional": False},
    "failures": {"type": "number", "name": "Failures", "optional": False},
    "scanned_urls": {
        "type": "number",
        "name": "Scanned URLs",
        "optional": False,
    },
}
DATASET_BAD_LINKS_PER_ENVIRONMENT_UNIQUE_BY = ["date", "environment"]



# Number of bad CMS pages per environment
DATASET_BAD_CMS_PAGES_PER_ENVIRONMENT_NAME = "export.bad_cms_pages_per_environment"
DATASET_BAD_CMS_PAGES_PER_ENVIRONMENT_FIELDS = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "environment": {
        "type": "string",
        "name": "Environment",
        "optional": False,
    },
    "errors": {"type": "number", "name": "Errors", "optional": False},
    "failures": {"type": "number", "name": "Failures", "optional": False},
    "scanned_urls": {
        "type": "number",
        "name": "Scanned URLs",
        "optional": False,
    },
}
DATASET_BAD_CMS_PAGES_PER_ENVIRONMENT_UNIQUE_BY = ["date", "environment"]


# Number of content differences per service per environment
DATASET_CONTENT_DIFFS_PER_ENVIRONMENT_NAME = "cms.content_diffs_per_environment"
DATASET_CONTENT_DIFFS_PER_ENVIRONMENT_FIELDS = {
    "date": {"type": "date", "name": "Date", "optional": False},
    "environment": {
        "type": "string",
        "name": "Service & compared Environments",
        "optional": False,
    },
    "errors": {"type": "number", "name": "Errors", "optional": False},
    "failures": {"type": "number", "name": "Failures", "optional": False},
    "scanned_urls": {
        "type": "number",
        "name": "Number of compared pages",
        "optional": False,
    },
}
DATASET_CONTENT_DIFFS_PER_ENVIRONMENT_UNIQUE_BY = ["date", "environment"]


DataSets = namedtuple(
    "DataSets",
    [
        "ON_KANBAN_BY_LABELS",
        "IN_BACKLOG",
        "AUTO_VS_MANUAL",
        "TO_AUTOMATE",
        "UNLABELLED_ON_KANBAN",
        "UNLABELLED_IN_BACKLOG",
        "IN_BACKLOG_BY_LABELS",
        "TICKETS_CLOSED_TODAY",
        "BUGS_CLOSED_TODAY",
        "BUGS_PER_SERVICE",
        "BAD_LINKS_PER_ENVIRONMENT",
        "BAD_CMS_PAGES_PER_ENVIRONMENT",
        "CONTENT_DIFFS_PER_ENVIRONMENT",
    ],
)


def create_datasets(gecko_client: GeckoClient) -> DataSets:
    """
    More on datasets.find_or_create()
    https://developer.geckoboard.com/api-reference/python/#findorcreate
    """
    on_kanban_by_labels = gecko_client.datasets.find_or_create(
        DATASET_ON_KANBAN_BY_LABELS_NAME,
        DATASET_ON_KANBAN_BY_LABELS_FIELDS,
        DATASET_ON_KANBAN_BY_LABELS_UNIQUE_BY,
    )

    in_backlog = gecko_client.datasets.find_or_create(
        DATASET_BUGS_IN_BACKLOG_NAME,
        DATASET_BUGS_IN_BACKLOG_FIELDS,
        DATASET_BUGS_IN_BACKLOG_UNIQUE_BY,
    )

    in_backlog_by_labels = gecko_client.datasets.find_or_create(
        DATASET_BUGS_IN_BACKLOG_BY_LABELS_NAME,
        DATASET_BUGS_IN_BACKLOG_BY_LABELS_FIELDS,
        DATASET_BUGS_IN_BACKLOG_BY_LABELS_UNIQUE_BY,
    )

    auto_vs_manual = gecko_client.datasets.find_or_create(
        DATASET_VS_NAME, DATASET_VS_FIELDS, DATASET_VS_UNIQUE_BY
    )

    to_automate = gecko_client.datasets.find_or_create(
        DATASET_TO_AUTOMATE_NAME,
        DATASET_TO_AUTOMATE_FIELDS,
        DATASET_TO_AUTOMATE_UNIQUE_BY,
    )

    unlabelled_on_kanban = gecko_client.datasets.find_or_create(
        DATASET_UNLABELLED_ON_KANBAN_NAME,
        DATASET_UNLABELLED_ON_KANBAN_FIELDS,
        DATASET_UNLABELLED_ON_KANBAN_UNIQUE_BY,
    )

    unlabelled_in_backlog = gecko_client.datasets.find_or_create(
        DATASET_UNLABELLED_IN_BACKLOG_NAME,
        DATASET_UNLABELLED_IN_BACKLOG_FIELDS,
        DATASET_UNLABELLED_IN_BACKLOG_UNIQUE_BY,
    )

    tickets_closed_today = gecko_client.datasets.find_or_create(
        DATASET_TICKETS_CLOSED_TODAY_NAME,
        DATASET_TICKETS_CLOSED_TODAY_FIELDS,
        DATASET_TICKETS_CLOSED_TODAY_UNIQUE_BY,
    )

    bugs_closed_today = gecko_client.datasets.find_or_create(
        DATASET_BUGS_CLOSED_TODAY_NAME,
        DATASET_BUGS_CLOSED_TODAY_FIELDS,
        DATASET_BUGS_CLOSED_TODAY_UNIQUE_BY,
    )

    bugs_per_service = gecko_client.datasets.find_or_create(
        DATASET_BUGS_PER_SERVICE_NAME,
        DATASET_BUGS_PER_SERVICE_FIELDS,
        DATASET_BUGS_PER_SERVICE_UNIQUE_BY,
    )

    bad_links_per_environment = gecko_client.datasets.find_or_create(
        DATASET_BAD_LINKS_PER_ENVIRONMENT_NAME,
        DATASET_BAD_LINKS_PER_ENVIRONMENT_FIELDS,
        DATASET_BAD_LINKS_PER_ENVIRONMENT_UNIQUE_BY,
    )

    bad_cms_pages_per_environment = gecko_client.datasets.find_or_create(
        DATASET_BAD_CMS_PAGES_PER_ENVIRONMENT_NAME,
        DATASET_BAD_CMS_PAGES_PER_ENVIRONMENT_FIELDS,
        DATASET_BAD_CMS_PAGES_PER_ENVIRONMENT_UNIQUE_BY,
    )

    content_diffs_per_environment = gecko_client.datasets.find_or_create(
        DATASET_CONTENT_DIFFS_PER_ENVIRONMENT_NAME,
        DATASET_CONTENT_DIFFS_PER_ENVIRONMENT_FIELDS,
        DATASET_CONTENT_DIFFS_PER_ENVIRONMENT_UNIQUE_BY,
    )

    return DataSets(
        on_kanban_by_labels,
        in_backlog,
        auto_vs_manual,
        to_automate,
        unlabelled_on_kanban,
        unlabelled_in_backlog,
        in_backlog_by_labels,
        tickets_closed_today,
        bugs_closed_today,
        bugs_per_service,
        bad_links_per_environment,
        bad_cms_pages_per_environment,
        content_diffs_per_environment,
    )


def find_issues(
    jql: str,
    *,
    max_results: int = 100,
    fields: str = "key,labels,summary",
    start_at: int = 0
) -> dict:
    """Run Jira JQL and return result as JSON."""
    return JIRA_CLIENT.search_issues(
        jql_str=jql,
        maxResults=max_results,
        json_result=True,
        fields=fields,
        startAt=start_at,
    )


def find_all_issues(jql: str) -> dict:
    """Iterate over all search result pages and return result as JSON."""
    results = find_issues(jql)
    current_page = 1
    total_pages = math.ceil(results["total"] / len(results["issues"]))
    while (
        len(results["issues"]) < results["total"]
        and current_page < total_pages
    ):
        start_at = current_page * results["maxResults"]
        next_page_results = find_issues(jql, start_at=start_at)
        results["issues"] += next_page_results["issues"]
        current_page += 1
    return results


def count_labels(issues: list) -> Counter:
    counter = Counter()
    for issue in issues:
        for label in issue["fields"]["labels"]:
            counter[label] += 1
    return counter


def filter_labels_by_prefix(
    labels: Counter, prefix: str, *, remove_prefix: bool = True
) -> Counter:
    if prefix:
        labels = dict(
            filter(lambda x: x[0].startswith(prefix), labels.items())
        )
        if remove_prefix:
            labels = {k.replace(prefix, ""): v for k, v in labels.items()}
    return Counter(labels)


def filter_out_ignored_labels(
    counter: Counter, ignored_labels: List[str]
) -> Counter:
    if not ignored_labels:
        return counter
    filtered = filter(lambda x: x[0] not in ignored_labels, counter.items())
    return Counter(dict(filtered))


def filter_by_sought_labels(
    counter: Counter, sought_labels: List[str]
) -> Counter:
    if not sought_labels:
        return counter
    filtered = filter(lambda x: x[0] in sought_labels, counter.items())
    return Counter(dict(filtered))


def get_quantity_per_label(
    jql_query_result: dict,
    *,
    label_prefix: str = "qa_",
    remove_label_prefix: bool = True,
    ignored_labels: List[str] = None,
    look_for: List[str] = None
) -> dict:
    issues = jql_query_result["issues"]
    all_labels = count_labels(issues)
    by_prefix = filter_labels_by_prefix(
        all_labels, label_prefix, remove_prefix=remove_label_prefix
    )
    without_ignored = filter_out_ignored_labels(by_prefix, ignored_labels)
    sought = filter_by_sought_labels(without_ignored, look_for)
    return dict(sought)


def get_number_of_bugs_on_kanban_board_by_labels() -> List[dict]:
    kanban_bugs = find_issues(JQL_KANBAN_BUGS)
    types = get_quantity_per_label(
        kanban_bugs, ignored_labels=["auto", "manual"]
    )
    result = []
    for bug_type in types:
        item = {"date": TODAY, "label": bug_type, "quantity": types[bug_type]}
        result.append(item)
    return result


def get_number_of_bugs_in_backlog_by_labels() -> List[dict]:
    backlog_bugs = find_issues(JQL_BACKLOG_BUGS)
    types = get_quantity_per_label(
        backlog_bugs, ignored_labels=["auto", "manual"]
    )
    result = []
    for bug_type in types:
        item = {"date": TODAY, "label": bug_type, "quantity": types[bug_type]}
        result.append(item)
    return result


def get_number_of_unlabelled_bugs_on_kanban_board() -> List[dict]:
    unlabelled = find_issues(JQL_KANBAN_BUGS)
    number = len(
        [
            issue
            for issue in unlabelled["issues"]
            if not issue["fields"]["labels"]
        ]
    )
    return [{"date": TODAY, "quantity": number}]


def get_number_of_unlabelled_bugs_in_backlog() -> List[dict]:
    unlabelled = find_issues(JQL_BACKLOG_BUGS)
    number = len(
        [
            issue
            for issue in unlabelled["issues"]
            if not issue["fields"]["labels"]
        ]
    )
    return [{"date": TODAY, "quantity": number}]


def get_number_of_automated_vs_manual() -> List[dict]:
    vs = find_issues(JQL_MANUAL_VS_AUTOMATED)
    labels = get_quantity_per_label(vs, look_for=["auto", "manual"])
    auto = labels["auto"]
    manual = labels["manual"]
    return [{"date": TODAY, "auto": auto, "manual": manual}]


def get_number_of_bugs_in_backlog() -> List[dict]:
    bugs_in_backlog = find_issues(JQL_BACKLOG_BUGS)
    dataset = [{"date": TODAY, "quantity": bugs_in_backlog["total"]}]
    return dataset


def get_number_of_scenarios_to_automate() -> List[dict]:
    scenarios_to_automate = find_issues(JQL_SCENARIOS_TO_AUTOMATE)
    return [{"date": TODAY, "quantity": scenarios_to_automate["total"]}]


def get_number_of_bugs_closed_today() -> List[dict]:
    closed = find_issues(JQL_BUGS_CLOSED_TODAY)
    return [{"date": TODAY, "closed": closed["total"]}]


def get_number_of_tickets_closed_today() -> List[dict]:
    closed = find_issues(JQL_TICKETS_CLOSED_TODAY)
    return [{"date": TODAY, "closed": closed["total"]}]


def get_number_of_bugs_per_service() -> List[dict]:
    found_bugs = find_all_issues(JQL_BUGS_PER_SERVICE)
    bugs_per_service = get_quantity_per_label(
        found_bugs, label_prefix=None, look_for=SERVICE_TAGS
    )
    result = []
    for service_tag in bugs_per_service:
        item = {
            "date": TODAY,
            "service": service_tag,
            "quantity": bugs_per_service[service_tag],
        }
        result.append(item)
    return result


def circle_ci_get_recent_builds(
    project: str,
    *,
    username: str = "uktrade",
    limit: int = 20,
    branch: str = "master"
) -> List[dict]:
    return CIRCLE_CI_CLIENT.build.recent(
        username=username, project=project, limit=limit, branch=branch
    )


def circle_ci_get_last_workflow_id(recent_builds: List[dict]) -> str:
    result = ""
    for build in recent_builds:
        if build["status"] == "not_run":
            print(
                "Ignoring skipped {} build: {}".format(
                    build["reponame"], build["build_num"]
                )
            )
            continue
        if "workflows" in build:
            result = build["workflows"]["workflow_id"]
            break
    return result


def circle_ci_get_builds_for_workflow(
    recent_circle_ci_builds: List[dict], last_workflow_id: str
) -> List[dict]:
    return [
        build
        for build in recent_circle_ci_builds
        if "workflows" in build
        and build["workflows"]["workflow_id"] == last_workflow_id
    ]


def circle_ci_get_last_workflow_test_results(
    last_workflow_builds: List[dict], job_name_mappings: dict
) -> dict:
    most_recent_build = last_workflow_builds[0]
    frmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    last_build_date = ""
    if most_recent_build["start_time"]:
        datetime_object = datetime.strptime(
            most_recent_build["start_time"], frmt
        )
        last_build_date = datetime_object.strftime("%d %b %H:%M")
    skipped = True if last_workflow_builds[0]["status"] == "not_run" else False
    if most_recent_build["user"]["is_user"]:
        test_results = {
            "user_avatar": most_recent_build["user"]["avatar_url"],
            "user_name": most_recent_build["user"]["name"],
            "user_login": most_recent_build["user"]["login"],
            "workflow_id": most_recent_build["workflows"]["workflow_id"],
            "last_build_date": last_build_date,
            "skipped": skipped,
        }
    else:
        test_results = {
            "user_avatar": "https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png",
            "user_name": "github",
            "user_login": "github",
            "workflow_id": most_recent_build["workflows"]["workflow_id"],
            "last_build_date": last_build_date,
            "skipped": skipped,
        }
    for build in last_workflow_builds:
        job_name = build["workflows"]["job_name"]
        if job_name in job_name_mappings.keys():
            friendly_name = job_name_mappings[job_name]
            build_time = 0
            if build["build_time_millis"]:
                build_time = round(build["build_time_millis"] / 1000)
            test_results[friendly_name] = {
                "start_time": build["start_time"],
                "stop_time": build["stop_time"],
                "build_time": build_time,
                "build_num": build["build_num"],
                "build_url": build["build_url"],
                "status": build["status"],
            }
    return test_results


def circle_ci_get_last_build_results(build: dict) -> dict:
    frmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    last_build_date = ""
    if build["start_time"]:
        datetime_object = datetime.strptime(build["start_time"], frmt)
        last_build_date = datetime_object.strftime("%d %b %H:%M")
    build_time = None
    if build["build_time_millis"]:
        build_time = round(build["build_time_millis"] / 1000)
    test_results = {
        "user_avatar": build["user"]["avatar_url"],
        "user_name": build["user"]["name"],
        "user_login": build["user"]["login"],
        "last_build_date": last_build_date,
        "start_time": build["start_time"],
        "stop_time": build["stop_time"],
        "build_time": build_time,
        "build_num": build["build_num"],
        "build_url": build["build_url"],
        "status": build["status"],
    }
    return test_results


def circle_ci_get_xml_build_artifact(build: dict) -> str:
    build_number = build["build_num"]
    username = build["username"]
    project_name = build["reponame"]
    build_artifacts = CIRCLE_CI_CLIENT.build.artifacts(
        username, project_name, build_number
    )
    xml_artifact_urls = [
        artifact["url"]
        for artifact in build_artifacts
        if artifact["url"].endswith(".xml")
    ]
    assert (
        len(xml_artifact_urls) == 1
    ), "Expected only 1 xml artifact but found {} in build: #{} - {}".format(
        len(xml_artifact_urls), build["build_num"], build["workflows"]["workflow_name"]
    )
    response = requests.get(xml_artifact_urls[0])
    return response.content.decode("utf-8")


def dead_links_get_xml_report_summary(xml_report: str) -> dict:
    """Extract root level attributes from XML (Junit) report

    JUnit report should contain following attributes:
        {'disabled': '0',
         'errors': '0',
         'failures': '9',
         'tests': '1421',
         'time': '655.9097394943237'}
    Only a subset of those attributes will be returned.
    """
    root = ET.fromstring(xml_report)
    attributes = root.attrib
    return {
        "errors": int(attributes["errors"]),
        "failures": int(attributes["failures"]),
        "scanned_urls": int(attributes["tests"]),
    }


def circle_ci_get_test_results_for_multi_workflow_project(
    project_name: str,
    *,
    ignored_workflows: List[str] = None,
    workflows_name_mappings: dict = None
) -> List[dict]:

    job_statuses_without_artifacts = ["not_run", "queued", "running"]
    recent_builds = circle_ci_get_recent_builds(project_name, limit=100)
    if ignored_workflows:
        recent_builds = [
            build
            for build in recent_builds
            if "workflows" in build
            and build["workflows"]["workflow_name"] not in ignored_workflows
        ]
    workflow_names = set(
        [build["workflows"]["workflow_name"] for build in recent_builds]
    )
    results = []
    for workflow_name in workflow_names:
        for build in recent_builds:
            if build["status"] not in job_statuses_without_artifacts:
                if build["workflows"]["workflow_name"] == workflow_name:
                    report = circle_ci_get_xml_build_artifact(build)
                    print("Parsing XML report for build", build["build_num"])
                    report_summary = dead_links_get_xml_report_summary(report)
                    result = {
                        "date": TODAY,
                        "environment": workflow_name,
                        "errors": report_summary["errors"],
                        "failures": report_summary["failures"],
                        "scanned_urls": report_summary["scanned_urls"],
                    }
                    if workflows_name_mappings:
                        friendly_name = workflows_name_mappings[workflow_name]
                        result["environment"] = friendly_name
                    results.append(result)
                    break
    return results


def circle_ci_get_last_test_results(
    project_name: str,
    *,
    ignored_workflows: List[str] = None,
    limit: int = None,
    job_name_mappings: dict = None
) -> dict:
    recent_builds = circle_ci_get_recent_builds(project_name, limit=limit)
    if ignored_workflows:
        recent_builds = [
            build
            for build in recent_builds
            if build["workflows"]["workflow_name"] not in ignored_workflows
        ]
    last_workflow_id = circle_ci_get_last_workflow_id(recent_builds)
    if last_workflow_id:
        last_workflow_builds = circle_ci_get_builds_for_workflow(
            recent_builds, last_workflow_id
        )
        result = circle_ci_get_last_workflow_test_results(
            last_workflow_builds, job_name_mappings
        )
    else:
        most_recent_build = recent_builds[0]
        result = circle_ci_get_last_build_results(most_recent_build)
    return result


def circle_ci_get_last_dead_urls_tests_results() -> List[dict]:
    ignored_workflows = [
        "refresh_geckoboard_periodically",
        "prod_check_cms_pages",
        "dev_ex_read_accessibility_tests",
        "exred_prod_dev_content_diff",
        "exred_prod_stage_content_diff",
        "exred_stage_dev_content_diff",
        "fas_prod_dev_content_diff",
        "fas_prod_stage_content_diff",
        "fas_stage_dev_content_diff",
        "invest_prod_dev_content_diff",
        "invest_prod_stage_content_diff",
        "invest_stage_dev_content_diff",
        "check_for_x_robots_tag_header_on_all_environments",
    ]
    workflows_name_mappings = {
        "dev_check_for_dead_links": "dev",
        "stage_check_for_dead_links": "stage",
        "prod_check_for_dead_links": "prod",
    }
    return circle_ci_get_test_results_for_multi_workflow_project(
        "directory-periodic-tests",
        ignored_workflows=ignored_workflows,
        workflows_name_mappings=workflows_name_mappings,
    )


def circle_ci_get_last_cms_pages_tests_results() -> List[dict]:
    ignored_workflows = [
        "refresh_geckoboard_periodically",
        "dev_ex_read_accessibility_tests",
        "exred_prod_dev_content_diff",
        "exred_prod_stage_content_diff",
        "exred_stage_dev_content_diff",
        "fas_prod_dev_content_diff",
        "fas_prod_stage_content_diff",
        "fas_stage_dev_content_diff",
        "invest_prod_dev_content_diff",
        "invest_prod_stage_content_diff",
        "invest_stage_dev_content_diff",
        "check_for_x_robots_tag_header_on_all_environments",
        "dev_check_for_dead_links",
        "stage_check_for_dead_links",
        "prod_check_for_dead_links",
    ]
    workflows_name_mappings = {
        "prod_check_cms_pages": "prod"
    }
    return circle_ci_get_test_results_for_multi_workflow_project(
        "directory-periodic-tests",
        ignored_workflows=ignored_workflows,
        workflows_name_mappings=workflows_name_mappings,
    )


def circle_ci_get_last_content_diff_tests_results() -> List[dict]:
    ignored_workflows = [
        "refresh_geckoboard_periodically",
        "dev_ex_read_accessibility_tests",
        "check_for_x_robots_tag_header_on_all_environments",
        "dev_check_for_dead_links",
        "stage_check_for_dead_links",
        "prod_check_for_dead_links",
        "prod_check_cms_pages",
    ]
    workflows_name_mappings = {
        "exred_prod_dev_content_diff": "exred prod dev",
        "exred_prod_stage_content_diff": "exred prod stage",
        "exred_stage_dev_content_diff": "exred stage dev",
        "fas_prod_dev_content_diff": "fas prod dev",
        "fas_prod_stage_content_diff": "fas prod stage",
        "fas_stage_dev_content_diff": "fas stage dev",
        "invest_prod_dev_content_diff": "invest prod dev",
        "invest_prod_stage_content_diff": "invest prod stage",
        "invest_stage_dev_content_diff": "invest stage dev",
    }
    return circle_ci_get_test_results_for_multi_workflow_project(
        "directory-periodic-tests",
        ignored_workflows=ignored_workflows,
        workflows_name_mappings=workflows_name_mappings,
    )


def circle_ci_get_last_test_results_per_project() -> dict:
    return {
        "Tests": circle_ci_get_last_test_results(
            "directory-tests",
            job_name_mappings=CIRCLE_CI_DIRECTORY_TESTS_WORKFLOW_JOB_NAME_MAPPINGS,
        ),
        "API": circle_ci_get_last_test_results(
            "directory-api",
            job_name_mappings=CIRCLE_CI_DIRECTORY_WORKFLOW_JOB_NAME_MAPPINGS,
        ),
        "FAS": circle_ci_get_last_test_results(
            "directory-ui-supplier",
            job_name_mappings=CIRCLE_CI_DIRECTORY_WORKFLOW_JOB_NAME_MAPPINGS,
        ),
        "FAB": circle_ci_get_last_test_results(
            "directory-ui-buyer",
            job_name_mappings=CIRCLE_CI_DIRECTORY_WORKFLOW_JOB_NAME_MAPPINGS,
        ),
        "ExRed": circle_ci_get_last_test_results(
            "directory-ui-export-readiness",
            job_name_mappings=CIRCLE_CI_DIRECTORY_WORKFLOW_JOB_NAME_MAPPINGS,
        ),
        "SSO": circle_ci_get_last_test_results(
            "directory-sso",
            job_name_mappings=CIRCLE_CI_DIRECTORY_WORKFLOW_JOB_NAME_MAPPINGS,
        ),
        "SUD": circle_ci_get_last_test_results(
            "directory-sso-profile",
            job_name_mappings=CIRCLE_CI_DIRECTORY_WORKFLOW_JOB_NAME_MAPPINGS,
        ),
        "SSO Proxy": circle_ci_get_last_test_results(
            "directory-sso-proxy",
            job_name_mappings=CIRCLE_CI_DIRECTORY_WORKFLOW_JOB_NAME_MAPPINGS,
        ),
        "CH Search": circle_ci_get_last_test_results(
            "directory-companies-house-search",
            job_name_mappings=CIRCLE_CI_DIRECTORY_CH_SEARCH_WORKFLOW_JOB_NAME_MAPPINGS,
        ),
    }


def circle_ci_get_job_status_color(status: str) -> str:
    status_colors = {
        "failed": "red",
        "fixed": "green",
        "not_run": "grey",
        "queued": "purple",
        "running": "blue",
        "success": "green",
        "timedout": "red",
        "canceled": "grey",
    }
    return status_colors[status]


def geckoboard_get_build_summary(test_results: dict) -> str:
    if test_results["build_num"]:
        details = {
            "start": test_results["start_time"],
            "stop": test_results["stop_time"],
            "seconds": test_results["build_time"],
            "number": test_results["build_num"],
        }
        msg = (
            "Build #{number} took {seconds} seconds to run. It started at "
            "{start} and finished at {stop}".format(**details)
        )
    else:
        msg = "The build was not executed"

    return msg


def geckoboard_generate_table_rows_for_test_results(
    services_test_results: dict
) -> str:
    workflow_row_template = """
        <tr style="font-size:14pt">
            <td>{service_name}<img src="{user_avatar_url}" alt="{user_name}" width="25" height="25"/></td>
            <td>{last_build_date}</td>
            <td></td>
            <td></td>
            <td></td>
            <td><a target="_blank" href="{smoke_build_url}" style="color:{smoke_status_color}" title="{smoke_build_summary}">{smoke_status}</a></td>
            <td><a target="_blank" href="{fab_build_url}" style="color:{fab_status_color}" title="{fab_build_summary}">{fab_status}</td>
            <td><a target="_blank" href="{fas_build_url}" style="color:{fas_status_color}" title="{fas_build_summary}">{fas_status}</td>
            <td><a target="_blank" href="{sso_build_url}" style="color:{sso_status_color}" title="{sso_build_summary}">{sso_status}</td>
            <td><a target="_blank" href="{sud_build_url}" style="color:{sud_status_color}" title="{sud_build_summary}">{sud_status}</td>
            <td><a target="_blank" href="{chrome_build_url}" style="color:{chrome_status_color}" title="{chrome_build_summary}">{chrome_status}</td>
            <td><a target="_blank" href="{firefox_build_url}" style="color:{firefox_status_color}" title="{firefox_build_summary}">{firefox_status}</td>
        </tr>
    """
    build_row_template = """
        <tr style="font-size:14pt">
            <td>{service_name}<img src="{user_avatar_url}" alt="{user_name}" width="25" height="25"/></td>
            <td>{last_build_date}</td>
            <td></td>
            <td><a target="_blank" href="{build_url}" style="color:{status_color}" title="{summary}">{status}</a></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
    """
    director_build_row_template = """
        <tr style="font-size:14pt">
            <td>{service_name}<img src="{user_avatar_url}" alt="{user_name}" width="25" height="25"/></td>
            <td>{last_build_date}</td>
            <td><a target="_blank" href="{unit_build_url}" style="color:{unit_status_color}" title="{unit_summary}">{unit_status}</a></td>
            <td><a target="_blank" href="{deploy_build_url}" style="color:{deploy_status_color}" title="{deploy_summary}">{deploy_status}</a></td>
            <td><a target="_blank" href="{integration_build_url}" style="color:{integration_status_color}" title="{integration_summary}">{integration_status}</a></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
    """
    empty_result = {
        "build_num": None,
        "build_url": "",
        "build_time": None,
        "start_time": None,
        "status": "not_run",
        "stop_time": None,
    }
    result = ""
    for service_name, test_results in services_test_results.items():
        if service_name in DIRECTORY_PROJECTS_WITH_WORKFLOW:
            unit = test_results.get("Unit Tests", empty_result)
            deploy = test_results.get("Deploy to Dev", empty_result)
            integration = test_results.get("Integration Tests", empty_result)
            result += director_build_row_template.format(
                service_name=service_name,
                user_avatar_url=test_results["user_avatar"],
                user_name=test_results["user_name"],
                last_build_date=test_results["last_build_date"],
                unit_build_url=unit["build_url"],
                unit_status_color=circle_ci_get_job_status_color(
                    unit["status"]
                ),
                unit_summary=geckoboard_get_build_summary(unit),
                unit_status=unit["status"].capitalize(),
                deploy_build_url=deploy["build_url"],
                deploy_status_color=circle_ci_get_job_status_color(
                    deploy["status"]
                ),
                deploy_summary=geckoboard_get_build_summary(deploy),
                deploy_status=deploy["status"].capitalize(),
                integration_build_url=integration["build_url"],
                integration_status_color=circle_ci_get_job_status_color(
                    integration["status"]
                ),
                integration_summary=geckoboard_get_build_summary(integration),
                integration_status=integration["status"].capitalize(),
            )
            continue
        if ("workflow_id" not in test_results) or (test_results["skipped"]):
            result += build_row_template.format(
                service_name=service_name,
                user_avatar_url=test_results["user_avatar"],
                user_name=test_results["user_name"],
                last_build_date=test_results["last_build_date"],
                build_url=test_results["build_url"],
                status_color=circle_ci_get_job_status_color(
                    test_results["status"]
                ),
                summary=geckoboard_get_build_summary(test_results),
                status=test_results["status"].capitalize(),
            )
            continue
        smoke = test_results.get("Smoke", empty_result)
        fab = test_results.get("FAB", empty_result)
        fas = test_results.get("FAS", empty_result)
        sso = test_results.get("SSO", empty_result)
        sud = test_results.get("SUD", empty_result)
        chrome = test_results.get("Chrome", empty_result)
        firefox = test_results.get("Firefox", empty_result)
        result += workflow_row_template.format(
            service_name=service_name,
            user_avatar_url=test_results["user_avatar"],
            user_name=test_results["user_name"],
            last_build_date=test_results["last_build_date"],
            smoke_build_url=smoke["build_url"],
            smoke_status_color=circle_ci_get_job_status_color(smoke["status"]),
            smoke_build_summary=geckoboard_get_build_summary(smoke),
            smoke_status=smoke["status"].capitalize(),
            fab_build_url=fab["build_url"],
            fab_status_color=circle_ci_get_job_status_color(fab["status"]),
            fab_build_summary=geckoboard_get_build_summary(fab),
            fab_status=fab["status"].capitalize(),
            fas_build_url=fas["build_url"],
            fas_status_color=circle_ci_get_job_status_color(fas["status"]),
            fas_build_summary=geckoboard_get_build_summary(fas),
            fas_status=fas["status"].capitalize(),
            sso_build_url=sso["build_url"],
            sso_status_color=circle_ci_get_job_status_color(sso["status"]),
            sso_build_summary=geckoboard_get_build_summary(sso),
            sso_status=sso["status"].capitalize(),
            sud_build_url=sud["build_url"],
            sud_status_color=circle_ci_get_job_status_color(sud["status"]),
            sud_build_summary=geckoboard_get_build_summary(sud),
            sud_status=sud["status"].capitalize(),
            chrome_build_url=chrome["build_url"],
            chrome_status_color=circle_ci_get_job_status_color(
                chrome["status"]
            ),
            chrome_build_summary=geckoboard_get_build_summary(chrome),
            chrome_status=chrome["status"].capitalize(),
            firefox_build_url=firefox["build_url"],
            firefox_status_color=circle_ci_get_job_status_color(
                firefox["status"]
            ),
            firefox_build_summary=geckoboard_get_build_summary(firefox),
            firefox_status=firefox["status"].capitalize(),
        )
    return result


def geckoboard_generate_content_for_test_results_widget_update(
    test_results: dict
) -> dict:
    table_template = """
    <table width="100%">
    <thead>
    <tr style="font-size:14pt">
        <th>Project</th>
        <th>When</th>
        <th>Unit</th>
        <th>Deploy</th>
        <th>Integration</th>
        <th>Smoke</th>
        <th>FAB</th>
        <th>FAS</th>
        <th>SSO</th>
        <th>SUD</th>
        <th>Chrome</th>
        <th>Firefox</th>
    </tr>
    </thead>
    <tbody>
        {rows}
    </tbody>
    </table>
    """
    rows = geckoboard_generate_table_rows_for_test_results(test_results)
    text = table_template.format(rows=rows)
    message = {
        "api_key": GECKOBOARD_API_KEY,
        "data": {"item": [{"text": text, "type": 0}]},
    }
    return message


def geckoboard_push_test_results():
    last_test_results = circle_ci_get_last_test_results_per_project()
    message = geckoboard_generate_content_for_test_results_widget_update(
        last_test_results
    )
    url = GECKOBOARD_PUSH_URL + GECKOBOARD_TEST_RESULTS_WIDGET_KEY
    response = requests.post(url, json=message)
    assert response.status_code == 200


if __name__ == "__main__":
    kanban_bugs_by_labels = get_number_of_bugs_on_kanban_board_by_labels()
    backlog_bugs_by_labels = get_number_of_bugs_in_backlog_by_labels()
    unlabelled_on_kanban = get_number_of_unlabelled_bugs_on_kanban_board()
    unlabelled_in_backlog = get_number_of_unlabelled_bugs_in_backlog()
    auto_vs_manual = get_number_of_automated_vs_manual()
    in_backlog = get_number_of_bugs_in_backlog()
    to_automate = get_number_of_scenarios_to_automate()
    tickets_closed_today = get_number_of_tickets_closed_today()
    bugs_closed_today = get_number_of_bugs_closed_today()
    bugs_per_service = get_number_of_bugs_per_service()
    bad_urls = circle_ci_get_last_dead_urls_tests_results()
    bad_cms_pages = circle_ci_get_last_cms_pages_tests_results()
    content_diffs = circle_ci_get_last_content_diff_tests_results()

    print("Bugs by labels on the Kanban board: ", kanban_bugs_by_labels)
    print("Unlabelled bugs on the Kanban board: ", unlabelled_on_kanban)
    print("Number of bugs in Backlog", in_backlog)
    print("Bugs by labels in the Backlog: ", backlog_bugs_by_labels)
    print("Unlabelled bugs in Backlog: ", unlabelled_in_backlog)
    print("Automated vs Manual: ", auto_vs_manual)
    print("Number of scenarios to automate: ", to_automate)
    print("Number of tickets closed today: ", tickets_closed_today)
    print("Number of bugs closed today: ", bugs_closed_today)
    print("Number of bugs per service: ", bugs_per_service)
    print("CMS - bad URLs per environment: ", bad_urls)
    print("CMS - bad pages on production: ", bad_cms_pages)
    print("Content diff per service:", content_diffs)

    print("Creating datasets in Geckoboard...")
    datasets = create_datasets(GECKO_CLIENT)
    print("All datasets properly created.")

    print("Pushing all datasets to Geckoboard")
    datasets.ON_KANBAN_BY_LABELS.post(kanban_bugs_by_labels)
    datasets.IN_BACKLOG_BY_LABELS.post(backlog_bugs_by_labels)
    datasets.UNLABELLED_ON_KANBAN.post(unlabelled_on_kanban)
    datasets.UNLABELLED_IN_BACKLOG.post(unlabelled_in_backlog)
    datasets.AUTO_VS_MANUAL.post(auto_vs_manual)
    datasets.IN_BACKLOG.post(in_backlog)
    datasets.TO_AUTOMATE.post(to_automate)
    datasets.TICKETS_CLOSED_TODAY.post(tickets_closed_today)
    datasets.BUGS_CLOSED_TODAY.post(bugs_closed_today)
    datasets.BUGS_PER_SERVICE.post(bugs_per_service)
    datasets.BAD_LINKS_PER_ENVIRONMENT.post(bad_urls)
    datasets.BAD_CMS_PAGES_PER_ENVIRONMENT.post(bad_cms_pages)
    datasets.CONTENT_DIFFS_PER_ENVIRONMENT.post(content_diffs)
    print("All datasets pushed")

    print("Pushing tests results to Geckoboard widget")
    geckoboard_push_test_results()
    print("Tests results successfully pushed to Geckoboard widget")
