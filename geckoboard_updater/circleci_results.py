from circleci_helpers import (
    DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS,
    last_load_test_artifacts,
    get_results_distribution,
    get_load_tests_requests_results,
    last_content_diff_results,
    DIRECTORY_CONTENT_DIFF_JOB_NAME_MAPPINGS
)
from geckoboard_updater import CIRCLE_CI_CLIENT


CONTENT_DIFF_RESULTS = last_content_diff_results(
    CIRCLE_CI_CLIENT,
    "directory-periodic-tests",
    DIRECTORY_CONTENT_DIFF_JOB_NAME_MAPPINGS
)

LOAD_TESTS_ARTIFACTS = last_load_test_artifacts(
    CIRCLE_CI_CLIENT,
    "directory-tests",
    job_name_mappings=DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS
)

LOAD_TESTS_RESPONSE_TIMES_DISTRIBUTIONS = get_results_distribution(LOAD_TESTS_ARTIFACTS)
LOAD_TESTS_RESPONSE_TIMES_METRICS = get_load_tests_requests_results(LOAD_TESTS_ARTIFACTS)
