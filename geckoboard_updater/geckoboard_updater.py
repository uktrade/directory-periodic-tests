#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from datetime import date

from geckoboard.client import Client as GeckoClient
from jira import JIRA as JiraClient
from circleclient import circleclient

from gecko_dataset_schemas import (
    ContentDatasetSchemas,
    ToolsDatasetSchemas,
)
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
    # Geckoboard Datasets (with schemas)
    CONTENT_DATASETS = create_datasets(ContentDatasetSchemas, GECKO_CLIENT)
    TOOLS_DATASETS = create_datasets(ToolsDatasetSchemas, GECKO_CLIENT)

    from jira_results import *

    # CONTENT_DATASETS.BAD_CMS_PAGES_PER_ENVIRONMENT.dataset.post()
    # CONTENT_DATASETS.BAD_LINKS_PER_ENVIRONMENT.dataset.post()
    # CONTENT_DATASETS.PAGE_DIFFS_PER_ENVIRONMENT.dataset.post()
    CONTENT_DATASETS.BUGS_AUTO_VS_MANUAL.dataset.post(content_bugs_manual_vs_automated)
    CONTENT_DATASETS.BUGS_CLOSED_TODAY.dataset.post(content_bugs_closed_today)
    CONTENT_DATASETS.BUGS_IN_BACKLOG.dataset.post(content_bugs_in_backlog)
    CONTENT_DATASETS.BUGS_IN_BACKLOG_BY_LABELS.dataset.post(content_bugs_in_backlog_by_labels)
    CONTENT_DATASETS.BUGS_ON_BOARD_BY_LABELS.dataset.post(content_bugs_on_board_by_labels)
    CONTENT_DATASETS.BUGS_PER_SERVICE.dataset.post(content_bugs_per_service)
    CONTENT_DATASETS.TICKETS_CLOSED_TODAY.dataset.post(content_tickets_closed_today)
    CONTENT_DATASETS.TICKETS_ON_BOARD.dataset.post(content_tickets_on_board)
    CONTENT_DATASETS.UNLABELLED_BUGS_IN_BACKLOG.dataset.post(content_unlabelled_bugs_in_backlog)
    CONTENT_DATASETS.UNLABELLED_BUGS_ON_BOARD.dataset.post(content_unlabelled_bugs_on_board)

    # TOOLS_DATASETS.BAD_CMS_PAGES_PER_ENVIRONMENT.dataset.post()
    # TOOLS_DATASETS.BAD_LINKS_PER_ENVIRONMENT.dataset.post()
    # TOOLS_DATASETS.PAGE_DIFFS_PER_ENVIRONMENT.dataset.post()
    TOOLS_DATASETS.BUGS_AUTO_VS_MANUAL.dataset.post(tools_bugs_manual_vs_automated)
    TOOLS_DATASETS.BUGS_CLOSED_TODAY.dataset.post(tools_bugs_closed_today)
    TOOLS_DATASETS.BUGS_IN_BACKLOG.dataset.post(tools_bugs_in_backlog)
    TOOLS_DATASETS.BUGS_IN_BACKLOG_BY_LABELS.dataset.post(tools_bugs_in_backlog_by_labels)
    TOOLS_DATASETS.BUGS_ON_BOARD_BY_LABELS.dataset.post(tools_bugs_on_board_by_labels)
    TOOLS_DATASETS.BUGS_PER_SERVICE.dataset.post(tools_bugs_per_service)
    TOOLS_DATASETS.TICKETS_CLOSED_TODAY.dataset.post(tools_tickets_closed_today)
    TOOLS_DATASETS.TICKETS_ON_BOARD.dataset.post(tools_tickets_on_board)
    TOOLS_DATASETS.UNLABELLED_BUGS_IN_BACKLOG.dataset.post(tools_unlabelled_bugs_in_backlog)
    TOOLS_DATASETS.UNLABELLED_BUGS_ON_BOARD.dataset.post(tools_unlabelled_bugs_on_board)

    push_directory_service_build_results(
        CIRCLE_CI_CLIENT, GECKOBOARD_PUSH_URL, GECKOBOARD_API_KEY,
        GECKOBOARD_TEST_RESULTS_WIDGET_KEY)

    push_directory_tests_results(
        CIRCLE_CI_CLIENT, GECKOBOARD_PUSH_URL, GECKOBOARD_API_KEY,
        GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY)
