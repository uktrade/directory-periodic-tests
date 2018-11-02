#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from datetime import date

from geckoboard.client import Client as GeckoClient
from jira import JIRA as JiraClient
from circleclient import circleclient

from gecko_dataset_schemas import DatasetSchemas
from gecko_helpers import (
    create_datasets,
    push_directory_tests_results,
    push_directory_service_build_results,
)

# Env Vars
GECKOBOARD_API_KEY = os.environ["GECKOBOARD_API_KEY"]
GECKOBOARD_TEST_RESULTS_WIDGET_KEY = os.environ[
    "GECKOBOARD_TEST_RESULTS_WIDGET_KEY"
]
GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY = os.environ[
    "GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY"
]
GECKOBOARD_PUSH_URL = os.getenv(
    "GECKOBOARD_PUSH_URL", "https://push.geckoboard.com/v1/send/"
)
JIRA_HOST = os.environ["JIRA_HOST"]
JIRA_USERNAME = os.environ["JIRA_USERNAME"]
JIRA_PASSWORD = os.environ["JIRA_PASSWORD"]
CIRCLE_CI_API_TOKEN = os.environ["CIRCLE_CI_API_TOKEN"]

# other variables
TODAY = date.today().isoformat()

# Clients
JIRA_CLIENT = JiraClient(JIRA_HOST, auth=(JIRA_USERNAME, JIRA_PASSWORD))
GECKO_CLIENT = GeckoClient(GECKOBOARD_API_KEY)
CIRCLE_CI_CLIENT = circleclient.CircleClient(CIRCLE_CI_API_TOKEN)


if __name__ == "__main__":
    DATASETS = create_datasets(DatasetSchemas, GECKO_CLIENT)

    from jira_results import *
    DATASETS.JIRA_BUGS_BY_LABELS.dataset.post(jira_bugs_by_labels)
    DATASETS.JIRA_BUG_AND_TICKET_COUNTERS.dataset.post(jira_bug_and_ticket_counters)

    from circleci_results import *
    DATASETS.PERIODIC_TESTS_RESULTS.dataset.post(circle_ci_periodic_tests_results)
    DATASETS.LOAD_TESTS_RESULT_DISTRIBUTION.dataset.post(load_tests_response_times_distributions)
    DATASETS.LOAD_TESTS_RESULT_REQUESTS.dataset.post(load_tests_response_times_metrics)

    push_directory_service_build_results(
        CIRCLE_CI_CLIENT, GECKOBOARD_PUSH_URL, GECKOBOARD_API_KEY,
        GECKOBOARD_TEST_RESULTS_WIDGET_KEY)
    push_directory_tests_results(
        CIRCLE_CI_CLIENT, GECKOBOARD_PUSH_URL, GECKOBOARD_API_KEY,
        GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY)
