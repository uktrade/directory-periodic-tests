from circleci_helpers import (
    DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS,
    last_load_test_artifacts,
    get_results_distribution,
    get_load_tests_requests_results,
    last_content_diff_results,
    DIRECTORY_CONTENT_DIFF_JOB_NAME_MAPPINGS
)
from geckoboard_updater import CIRCLE_CI_CLIENT


circle_ci_content_diffs = last_content_diff_results(
    CIRCLE_CI_CLIENT,
    "directory-periodic-tests",
    DIRECTORY_CONTENT_DIFF_JOB_NAME_MAPPINGS
)

load_tests_artifacts = last_load_test_artifacts(
    CIRCLE_CI_CLIENT,
    "directory-tests",
    job_name_mappings=DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS
)

load_tests_response_times_distributions = get_results_distribution(load_tests_artifacts)
load_tests_response_times_metrics = get_load_tests_requests_results(load_tests_artifacts)
