# -*- coding: utf-8 -*-
from collections import namedtuple
from enum import EnumMeta, Enum

import requests
from circleclient.circleclient import CircleClient
from geckoboard.client import Client as GeckoClient
from geckoboard.dataset import Dataset

from circleci_helpers import (
    last_directory_tests_results,
    last_directory_service_build_results
)
from gecko_dataset_schemas import Schema


DatasetAndSchema = namedtuple("DatasetAndSchema", ["dataset", "schema"])


class Datasets(Enum):
    """Geckoboard Dataset enumeration."""

    @property
    def dataset(self) -> Dataset:
        return self.value.dataset

    @property
    def schema(self) -> Schema:
        return self.value.schema


def create_datasets(
        dataset_enum: EnumMeta, gecko_client: GeckoClient) -> Datasets:
    """
    More on datasets.find_or_create()
    https://developer.geckoboard.com/api-reference/python/#findorcreate
    """
    dasets = {
        key: DatasetAndSchema(
            dataset=gecko_client.datasets.find_or_create(*schema.value),
            schema=schema.value
        )
        for key, schema
        in dataset_enum.__members__.items()
    }
    return Datasets(value="Datasets", names=dasets)


def job_status_color(status: str) -> str:
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


def widget_text_for_directory_tests(test_results: dict) -> str:
    table_template = """<table style="width:100%">
<thead>
<tr style="font-size:14pt">
<th>Name</th><th>When</th><th>Time</th><th>Status</th>
</tr>
</thead>
<tbody>
{rows}
</tbody></table>"""
    row_template = """<tr style="font-size:14pt">
<td>{name}</td>
<td><img src="{user_avatar}" title="{user_name}" width="25" height="25"/>{start_time}</td>
<td>{build_time}</td>
<td><a target="_blank" href="{build_url}" style="color:{status_color}">{status}</a></td>
</tr>"""
    rows = ""
    for friendly_name, result in test_results.items():
        rows += row_template.format(
            name=friendly_name,
            status_color=job_status_color(result["status"]),
            **result
        )
    return table_template.format(rows=rows)


def widget_text_for_service_build(build_results: dict) -> str:
    table_template = """<table style="width:100%">
<thead>
<tr style="font-size:14pt">
<th>Name</th><th>When</th><th>Time</th><th>Unit</th><th>Deploy</th><th>Integration</th>
</tr>
</thead><tbody>
{rows}
</tbody></table>"""
    row_template = """<tr style="font-size:14pt">
<td>{name}</td>
<td><img src="{user_avatar}" title="{user_name}" width="25" height="25"/>{start_time}</td>
<td>{build_time}</td>
{unit}
{deploy}
{integration}
</tr>"""
    job_status_template = """<td><a target="_blank" href="{build_url}" style="color:{status_color}">{status}</a></td>"""
    empty_row = "<td>N/A</td>"
    rows = ""
    for friendly_name, results in build_results.items():
        deploy = integration = empty_row
        unit = job_status_template.format(
            status_color=job_status_color(results["Unit Tests"]["status"]),
            **results["Unit Tests"])
        if "Deploy to Dev" in results:
            deploy = job_status_template.format(
                status_color=job_status_color(results["Deploy to Dev"]["status"]),
                **results["Deploy to Dev"])
        if "Integration Tests" in results:
            integration = job_status_template.format(
                status_color=job_status_color(results["Integration Tests"]["status"]),
                **results["Integration Tests"])
        rows += row_template.format(
            name=friendly_name,
            unit=unit,
            deploy=deploy,
            integration=integration,
            **results["Unit Tests"]
        )
    return table_template.format(rows=rows)


def push_widget_text(push_url: str, api_key: str, widget_key: str, text: str):
    message = {
        "api_key": api_key,
        "data": {"item": [{"text": text, "type": 0}]},
    }
    url = push_url + widget_key
    response = requests.post(url, json=message)
    error = f"Expected 200 but got {response.status_code} → {response.content}"
    assert response.status_code == 200, error


def push_directory_tests_results(
        circle_ci_client: CircleClient, geckoboard_push_url: str,
        geckoboard_api_key: str, widget_key: str):
    last_test_results = last_directory_tests_results(circle_ci_client)
    text = widget_text_for_directory_tests(last_test_results)
    push_widget_text(geckoboard_push_url, geckoboard_api_key, widget_key, text)


def push_directory_service_build_results(
        circle_ci_client: CircleClient, geckoboard_push_url: str,
        geckoboard_api_key: str, widget_key: str):
    last_service_build_results = last_directory_service_build_results(circle_ci_client)
    text = widget_text_for_service_build(last_service_build_results)
    push_widget_text(geckoboard_push_url, geckoboard_api_key, widget_key, text)
