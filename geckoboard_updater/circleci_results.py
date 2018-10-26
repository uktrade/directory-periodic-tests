from circleci_helpers import (
    DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS,
    last_load_test_artifacts,
    get_results_distribution,
    get_results_requests
)
from geckoboard_updater import CIRCLE_CI_CLIENT


LOAD_TESTS_ARTIFACTS = last_load_test_artifacts(
    CIRCLE_CI_CLIENT,
    "directory-tests",
    job_name_mappings=DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS
)

RESULTS_DISTRIBUTIONS = get_results_distribution(LOAD_TESTS_ARTIFACTS)
RESULTS_REQUESTS = get_results_requests(LOAD_TESTS_ARTIFACTS)


def get_distribution(environment: str, service: str):
    job_name = f"load_{service}_tests_{environment}".lower()
    friendly_name = DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS[job_name]
    return RESULTS_DISTRIBUTIONS[friendly_name]


def get_requests(environment: str, service: str):
    job_name = f"load_{service}_tests_{environment}".lower()
    friendly_name = DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS[job_name]
    return RESULTS_REQUESTS[friendly_name]


load_test_stage_cms_result_distribution = get_distribution("stage", "cms")
load_test_stage_fab_result_distribution = get_distribution("stage", "fab")
load_test_stage_fas_result_distribution = get_distribution("stage", "fas")
load_test_stage_invest_result_distribution = get_distribution("stage", "invest")

load_test_stage_cms_result_requests = get_requests("stage", "cms")
load_test_stage_fab_result_requests = get_requests("stage", "fab")
load_test_stage_fas_result_requests = get_requests("stage", "fas")
load_test_stage_invest_result_requests = get_requests("stage", "invest")
