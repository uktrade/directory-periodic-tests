# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List

from circleclient.circleclient import CircleClient

# Mapping of CircleCI job names to human friendly ones
DIRECTORY_TESTS_JOB_NAME_MAPPINGS = {
    "browser_all_chrome_dev":       "Dev Chrome",
    "browser_all_firefox_dev":      "Dev Firefox",
    "func_fab_test_dev":            "Dev FAB",
    "func_fas_test_dev":            "Dev FAS",
    "smoke_tests_dev":              "Dev Smoke",
    "func_sso_test_dev":            "Dev SSO",
    "func_sud_test_dev":            "Dev SUD",

    "browser_all_chrome_stage":     "Stage Chrome",
    "browser_all_firefox_stage":    "Stage Firefox",
    "func_fab_test_stage":          "Stage FAB",
    "func_fas_test_stage":          "Stage FAS",
    "smoke_tests_stage":            "Stage Smoke",
    "func_sso_test_stage":          "Stage SSO",
    "func_sud_test_stage":          "Stage SUD",

    "load_fab_tests_stage":         "Load STAGE FAB",
    "load_cms_tests_stage":         "Load STAGE CMS",
    "load_fas_tests_stage":         "Load STAGE FAS",
    "load_invest_tests_stage":      "Load STAGE Invest",
}

DIRECTORY_SERVICE_JOB_NAME_MAPPINGS = {
    "test":                         "Unit Tests",
    "deploy_to_dev":                "Deploy to Dev",
    "integration_tests":            "Integration Tests",
}

DIRECTORY_CH_SEARCH_JOB_NAME_MAPPINGS = {
    "test":                         "Unit Tests",
}


def recent_builds(
        circle_ci_client: CircleClient,
        project: str,
        *,
        username: str = "uktrade",
        limit: int = 10,
        branch: str = "master"
) -> List[dict]:
    return circle_ci_client.build.recent(
        username=username, project=project, limit=limit, branch=branch
    )


def last_build_per_job(builds: List[dict], job_mappings: dict) -> dict:
    last_builds = {}
    for build in builds:
        if "workflows" not in build:
            print(f"Ignoring legacy CircleCI 1.0  build #{build['build_num']} "
                  f"for {build['reponame']}")
            continue
        if build["workflows"]["job_name"] in job_mappings:
            if build["workflows"]["job_name"] not in last_builds:
                last_builds[build["workflows"]["job_name"]] = build
                continue
    return last_builds


def last_workflow_test_results(builds: dict, job_name_mappings: dict) -> dict:
    result = {}
    github_avatar = "https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png"
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    for job_name, build in builds.items():
        friendly_name = job_name_mappings[job_name]

        build_time = 0
        if build["build_time_millis"]:
            build_time = round(build["build_time_millis"] / 1000)

        if build["user"]["is_user"]:
            user_avatar = build["user"]["avatar_url"]
            user_name = build["user"]["name"]
        else:
            user_avatar = github_avatar
            user_name = "github"

        datetime_object = datetime.strptime(build["start_time"], date_format)
        last_build_date = datetime_object.strftime("%d %b %H:%M")

        result[friendly_name] = {
            "start_time": last_build_date,
            "build_time": build_time,
            "build_url": build["build_url"],
            "status": build["status"],
            "user_avatar": user_avatar,
            "user_name": user_name,
        }

    return result


def last_test_results(
        circle_ci_client: CircleClient, project_name: str,
        job_name_mappings: dict, *, limit: int = 10) -> dict:
    recent = recent_builds(circle_ci_client, project_name, limit=limit)
    build_per_job = last_build_per_job(recent, job_name_mappings)
    return last_workflow_test_results(build_per_job, job_name_mappings)


def last_directory_tests_results(circle_ci_client: CircleClient) -> dict:
    return last_test_results(
        circle_ci_client,
        "directory-tests",
        job_name_mappings=DIRECTORY_TESTS_JOB_NAME_MAPPINGS,
        limit=100
    )


def last_directory_service_build_results(circle_ci_client: CircleClient) -> dict:
    return {
        "API": last_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-api",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "FAS": last_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-ui-supplier",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "FAB": last_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-ui-buyer",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "ExRed": last_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-ui-export-readiness",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "SSO": last_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-sso",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "SUD": last_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-sso-profile",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "SSO Proxy": last_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-sso-proxy",
            job_name_mappings=DIRECTORY_SERVICE_JOB_NAME_MAPPINGS,
        ),
        "CH Search": last_test_results(
            circle_ci_client=circle_ci_client,
            project_name="directory-companies-house-search",
            job_name_mappings=DIRECTORY_CH_SEARCH_JOB_NAME_MAPPINGS,
        ),
    }
