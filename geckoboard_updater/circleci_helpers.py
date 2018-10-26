# -*- coding: utf-8 -*-
import csv
from io import StringIO
from collections import defaultdict
from datetime import datetime
from os.path import basename, splitext
from typing import List
from xml.etree import ElementTree

import requests
from circleclient.circleclient import CircleClient

# Mapping of CircleCI job names to human friendly ones
DIRECTORY_CONTENT_DIFF_JOB_NAME_MAPPINGS = {
    "exred_compare_prod_and_dev_pages":     "ExRed Prod Dev",
    "exred_compare_prod_and_stage_pages":   "ExRed Prod Stage",
    "exred_compare_stage_and_dev_pages":    "ExRed Stage Dev",

    "fas_compare_prod_and_dev_pages":       "FAS Prod Dev",
    "fas_compare_prod_and_stage_pages":     "FAS Prod Stage",
    "fas_compare_stage_and_dev_pages":      "FAS Stage Dev",

    "invest_compare_prod_and_dev_pages":    "Invest Prod Dev",
    "invest_compare_prod_and_stage_pages":  "Invest Prod Stage",
    "invest_compare_stage_and_dev_pages":   "Invest Stage Dev",
}

DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS = {
    "load_fab_tests_stage":         "Load STAGE FAB",
    "load_cms_tests_stage":         "Load STAGE CMS",
    "load_fas_tests_stage":         "Load STAGE FAS",
    "load_invest_tests_stage":      "Load STAGE Invest",
}

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
}

DIRECTORY_TESTS_JOB_NAME_MAPPINGS.update(DIRECTORY_LOAD_TESTS_JOB_NAME_MAPPINGS)

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
            friendly_name = job_mappings[build["workflows"]["job_name"]]
            if friendly_name not in last_builds:
                last_builds[friendly_name] = build
                continue
    return last_builds


def get_build_artifacts(
        circle_ci_client: CircleClient, builds: dict, extentions: List[str],
        *, username: str = "uktrade", decode_content: bool = True
) -> dict:
    """Fetch build artifacts that match one of selected file extensions"""

    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    build_artifacts = {}
    for friendly_name, build in builds.items():
        build_num = build["build_num"]
        project_name = build["reponame"]
        datetime_object = datetime.strptime(build["start_time"], date_format)
        run_date = datetime_object.strftime("%Y-%m-%dT%H:%M:%S.00+00:00")
        artifacts = circle_ci_client.build.artifacts(
            username, project_name, build_num
        )
        if artifacts:
            for artifact in artifacts:
                artifact["date"] = run_date
                artifact["build_num"] = build_num
            build_artifacts[friendly_name] = artifacts

    artifact_urls = defaultdict(list)
    for friendly_name, artifacts in build_artifacts.items():
        for artifact in artifacts:
            filename = basename(artifact["path"])
            _, extension = splitext(filename)
            if extension in extentions:
                url = {
                    "filename": filename,
                    "url": artifact["url"],
                    "date": artifact["date"],
                    "build_num": artifact["build_num"],
                }
                artifact_urls[friendly_name].append(url)
                print(f"Found '{friendly_name}' build artifact {filename} in "
                      f"build #{artifact['build_num']}")

    results = defaultdict(list)
    for friendly_name, artifacts in artifact_urls.items():
        for artifact in artifacts:
            filename = artifact["filename"]
            url = artifact["url"]
            build_num = artifact["build_num"]
            print(f"Fetching '{friendly_name}' build artifact: '{filename}' "
                  f"from build #{build_num}")
            response = requests.get(url)
            error = (f"Could not get {url} as CircleCI responded with "
                     f"{response.status_code}: {response.content}")
            assert response.status_code == 200, error
            if decode_content:
                content = response.content.decode("utf-8")
            else:
                content = response.content
            artifact.update({"content": content})
            results[friendly_name].append(artifact)

    return dict(results)


def xml_report_summary(xml_report: str) -> dict:
    """Extract root level attributes from XML (Junit) report

    JUnit report should contain following attributes:
        {'disabled': '0',
         'errors': '0',
         'failures': '9',
         'tests': '1421',
         'time': '655.9097394943237'}
    Only a subset of those attributes will be returned.
    """
    root = ElementTree.fromstring(xml_report)
    attributes = root.attrib
    return {
        "tests": int(attributes["tests"]),
        "errors": int(attributes["errors"]),
        "failures": int(attributes["failures"]),
    }


def last_workflow_test_results(builds: dict, job_name_mappings: dict) -> dict:
    result = {}
    github_avatar = "https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png"
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    for job_name, build in builds.items():

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

        result[job_name] = {
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


def parse_result_distribution_csv(
        artifact: dict, *,
        ignored_results: List[str] = ["total"],
        ignored_percentiles: List[str] = ["66%", "80%"],
) -> List[dict]:

    content = artifact["content"]
    run_date = artifact["date"]

    parsed_results = [
        dict(endpoint)
        for endpoint in csv.DictReader(StringIO(content))
    ]

    clean_results = []
    for result in parsed_results:
        clean_result = {}
        if result["Name"].lower() in ignored_results:
            continue
        for key, value in result.items():
            if key in ignored_percentiles:
                continue
            clean_key = key.replace("# ", "").replace("%", "").strip().lower()
            if value == "N/A":
                clean_result[clean_key] = None
            else:
                clean_value = int(value) if value.isnumeric() else value
                clean_result[clean_key] = clean_value

        clean_result["date"] = run_date
        clean_results.append(clean_result)
    return clean_results


def parse_result_requests_csv(
        artifact: dict, *,
        ignored_results: List[str] = ["total"],
) -> List[dict]:

    content = artifact["content"]
    run_date = artifact["date"]

    parsed_results = [
        dict(endpoint)
        for endpoint in csv.DictReader(StringIO(content))
    ]

    clean_results = []
    for result in parsed_results:
        clean_result = {}
        if result["Name"].lower() in ignored_results:
            continue
        method = result["Method"]
        name = result["Name"]
        result["Name"] = f"{method} {name}"
        result.pop("Method")
        for key, value in result.items():
            clean_key = key.replace("# ", "").replace("/", " per ").replace(" ", "_").strip().lower()
            if value == "N/A":
                clean_result[clean_key] = None
            else:
                if clean_key == "requests_per_s":
                    clean_value = float(value)
                else:
                    clean_value = int(value) if value.isnumeric() else value
                clean_result[clean_key] = clean_value
        clean_result["date"] = run_date
        clean_results.append(clean_result)
    return clean_results


def get_results_distribution(
        build_artifacts: dict, *,
        artifact_filename: str = "results_distribution.csv") -> dict:
    results = {}
    for friendly_name, artifacts in build_artifacts.items():
        for artifact in artifacts:
            if artifact["filename"] == artifact_filename:
                parsed = parse_result_distribution_csv(artifact)
                results[friendly_name] = parsed

    return results


def get_results_requests(
        build_artifacts: dict, *,
        artifact_filename: str = "results_requests.csv") -> dict:
    results = {}
    for friendly_name, artifacts in build_artifacts.items():
        for artifact in artifacts:
            if artifact["filename"] == artifact_filename:
                parsed = parse_result_requests_csv(artifact)
                results[friendly_name] = parsed

    return results


def last_load_test_artifacts(
        circle_ci_client: CircleClient, project_name: str,
        job_name_mappings: dict, *, limit: int = 50) -> dict:
    recent = recent_builds(circle_ci_client, project_name, limit=limit)
    filtered_builds = last_build_per_job(recent, job_name_mappings)
    return get_build_artifacts(circle_ci_client, filtered_builds, extentions=[".csv"])


def parse_junit_results(build_artifacts: dict) -> List[dict]:
    results = []
    for friendly_name, artifacts in build_artifacts.items():
        for artifact in artifacts:
            if artifact["filename"].endswith(".xml"):
                parsed = xml_report_summary(artifact["content"])
                parsed["environment"] = friendly_name
                parsed["date"] = artifact["date"]
                results.append(parsed)

    return results


def last_content_diff_results(
        circle_ci_client: CircleClient, project_name: str,
        job_name_mappings: dict, *, limit: int = 100) -> List[dict]:
    recent = recent_builds(circle_ci_client, project_name, limit=limit)
    filtered_builds = last_build_per_job(recent, job_name_mappings)
    artifacts = get_build_artifacts(
        circle_ci_client, filtered_builds, extentions=[".xml"])
    return parse_junit_results(artifacts)
