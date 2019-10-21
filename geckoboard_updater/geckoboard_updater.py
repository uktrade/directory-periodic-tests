#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from datetime import date

from circleclient import circleclient
from geckoboard.client import Client as GeckoClient
from jira import JIRA as JiraClient

from gecko_dataset_schemas import DatasetSchemas
from gecko_helpers import (
    create_datasets,
    push_directory_service_build_results,
    push_directory_tests_results,
    push_jira_query_links,
    push_links_to_useful_content_test_jobs,
    push_periodic_tests_results,
)

# Env Vars
GECKOBOARD_API_KEY = os.environ["GECKOBOARD_API_KEY"]
GECKOBOARD_TEST_RESULTS_WIDGET_KEY = os.environ[
    "GECKOBOARD_TEST_RESULTS_WIDGET_KEY"
]
GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY = os.environ[
    "GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY"
]
GECKOBOARD_PERIODIC_TESTS_RESULTS_WIDGET_KEY = os.environ[
    "GECKOBOARD_PERIODIC_TESTS_RESULTS_WIDGET_KEY"
]
GECKOBOARD_LINKS_TO_USEFUL_CONTENT_TEST_JOBS_WIDGET_KEY = os.environ[
    "GECKOBOARD_LINKS_TO_USEFUL_CONTENT_TEST_JOBS_WIDGET_KEY"
]
GECKOBOARD_CONTENT_JIRA_QUERY_LINKS_WIDGET_KEY = os.environ[
    "GECKOBOARD_CONTENT_JIRA_QUERY_LINKS_WIDGET_KEY"
]
GECKOBOARD_TOOLS_JIRA_QUERY_LINKS_WIDGET_KEY = os.environ[
    "GECKOBOARD_TOOLS_JIRA_QUERY_LINKS_WIDGET_KEY"
]
GECKOBOARD_PUSH_URL = os.getenv(
    "GECKOBOARD_PUSH_URL", "https://push.geckoboard.com/v1/send/"
)
JIRA_HOST = os.environ["JIRA_HOST"]
JIRA_USERNAME = os.environ["JIRA_USERNAME"]
JIRA_TOKEN = os.environ["JIRA_TOKEN"]
CIRCLE_CI_API_TOKEN = os.environ["CIRCLE_CI_API_TOKEN"]

# other variables
TODAY = date.today().isoformat()

# Clients
JIRA_CLIENT = JiraClient(JIRA_HOST, basic_auth=(JIRA_USERNAME, JIRA_TOKEN))
GECKO_CLIENT = GeckoClient(GECKOBOARD_API_KEY)
CIRCLE_CI_CLIENT = circleclient.CircleClient(CIRCLE_CI_API_TOKEN)


if __name__ == "__main__":
    print("Creating Geckoboard datasets")
    DATASETS = create_datasets(DatasetSchemas, GECKO_CLIENT)

    print("Fetching stats from Jira")
    from jira_results import *

    print("Pushing Jira stats to Geckoboard")
    DATASETS.JIRA_BUGS_BY_LABELS.dataset.post(jira_bugs_by_labels)
    DATASETS.JIRA_BUG_AND_TICKET_COUNTERS.dataset.post(
        jira_bug_and_ticket_counters
    )

    print("Fetching test results from CircleCi")
    from circleci_results import *

    print("Pushing periodic tests results to Geckoboard")
    DATASETS.PERIODIC_TESTS_RESULTS.dataset.post(
        circle_ci_periodic_tests_results
    )
    print("Pushing load tests result distribution results to Geckoboard")
    DATASETS.LOAD_TESTS_RESULT_DISTRIBUTION.dataset.post(
        load_tests_response_times_distributions
    )
    print("Pushing load test response times metrics to Geckoboard")
    DATASETS.LOAD_TESTS_RESULT_REQUESTS.dataset.post(
        load_tests_response_times_metrics
    )

    print(f"Pushing text widget data to GeckoBoard")
    push_directory_service_build_results(
        CIRCLE_CI_CLIENT,
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_TEST_RESULTS_WIDGET_KEY,
    )
    push_directory_tests_results(
        CIRCLE_CI_CLIENT,
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY,
    )
    push_periodic_tests_results(
        CIRCLE_CI_CLIENT,
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_PERIODIC_TESTS_RESULTS_WIDGET_KEY,
    )
    push_links_to_useful_content_test_jobs(
        CIRCLE_CI_CLIENT,
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_LINKS_TO_USEFUL_CONTENT_TEST_JOBS_WIDGET_KEY,
    )
    push_jira_query_links(
        content_jira_links,
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_CONTENT_JIRA_QUERY_LINKS_WIDGET_KEY,
    )
    push_jira_query_links(
        tools_jira_links,
        GECKOBOARD_PUSH_URL,
        GECKOBOARD_API_KEY,
        GECKOBOARD_TOOLS_JIRA_QUERY_LINKS_WIDGET_KEY,
    )
