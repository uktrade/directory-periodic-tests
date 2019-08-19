#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from datetime import datetime

TEST_ENV = os.environ["TEST_ENV"]

VARS = {
    "DEV": {
        "URL": os.environ["DEV_DIRECTORY_CMS_API_CLIENT_BASE_URL"],
        "KEY": os.environ["DEV_DIRECTORY_CMS_API_CLIENT_API_KEY"],
    },
    "STAGE": {
        "URL": os.environ["STAGE_DIRECTORY_CMS_API_CLIENT_BASE_URL"],
        "KEY": os.environ["STAGE_DIRECTORY_CMS_API_CLIENT_API_KEY"],
    },
    "PROD": {
        "URL": os.environ["PROD_DIRECTORY_CMS_API_CLIENT_BASE_URL"],
        "KEY": os.environ["PROD_DIRECTORY_CMS_API_CLIENT_API_KEY"],
    },
}

DIRECTORY_CMS_API_CLIENT_BASE_URL = VARS[TEST_ENV]["URL"]
DIRECTORY_CMS_API_CLIENT_API_KEY = VARS[TEST_ENV]["KEY"]

from django.conf import settings

settings.configure(
    DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS=30,
    DIRECTORY_CMS_API_CLIENT_BASE_URL=DIRECTORY_CMS_API_CLIENT_BASE_URL, 
    DIRECTORY_CMS_API_CLIENT_API_KEY=DIRECTORY_CMS_API_CLIENT_API_KEY, 
    DIRECTORY_CMS_API_CLIENT_SENDER_ID="directory",
    DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT=30,
    DIRECTORY_CMS_API_CLIENT_SERVICE_NAME="FIND_A_SUPPLIER",
    DIRECTORY_CMS_API_CLIENT_CACHE_EXPIRE_SECONDS=30,
    CACHES={ 
        'cms_fallback': { 
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 
            'LOCATION': 'unique-snowflake', 
        } 
    } 
)
 
from directory_cms_client.client import cms_api_client


def international_pages_status_report() -> dict:
    types = cms_api_client.get("api/pages/types/").json()["types"]
    international_types = [t for t in types if t.startswith("great_international.")]
    skipped_types = {
        "wagtailcore.page",
        "components.bannercomponent",
        "great_international.baseinternationalsectorpage",
        "great_international.capitalinvestopportunitypage",
        "great_international.internationalcapitalinvestlandingpage",
    }

    result = {}
    for page_type in set(international_types) - skipped_types:
        try:
            print(page_type)
            page_type_summary = []
            resp = cms_api_client.get(f"api/pages/?type={page_type}").json()
            if "items" not in resp:
                continue
            for page in resp["items"]:
                page_type_summary.append(
                    {
                        "id": page["id"],
                        "title": page["title"],
                        "languages": [l[0] for l in page["meta"]["languages"]],
                        "url": page["meta"]["url"],
                        "last_published_at": page["last_published_at"],
                        "draft_token": page["meta"]["draft_token"],
                    })
            result[page_type] = page_type_summary
        except requests.exceptions.HTTPError as ex:
            print(f"There was a problem with getting list of '{page_type}' pages: {ex}")

    return result


def generate_html_report(report: dict):
    table_template = """<table style="border: 1px solid black;width:75%;margin-left:12%;margin-right:13%;"> 
<thead>
<tr style="font-size:16pt">
<th style="padding:5px;text-align:left">ID</th>
<th style="padding:5px;text-align:left">Title</th>
<th style="padding:5px;text-align:left">Published</th>
<th style="padding:5px;text-align:left">Draft</th>
<th style="padding:5px;text-align:left">Languages</th>
</tr>
</thead>
{tbodies}
</table>"""
    tbody_template = """<tbody>
    <tr><th colspan="5" style="font-size:16pt;color:black;background-color:lightgray;text-align:left">{page_type}</th></tr>
{rows}
</tbody>"""
    page_row_template = """<tr style="font-size:14pt">
<td><a href="{url}" target="_blank">{id}</a></td>
<td><a href="{url}" target="_blank">{title}</a></td>
<td>{last_published_at}</td>
<td>{draft}</td>
<td>{languages}</td>
</tr>"""
    tbodies = ""
    for page_type, summaries in report.items():
        rows = ""
        for summary in summaries:
            if summary["last_published_at"]:
                last_published_at = datetime.strftime(
                    datetime.strptime(summary["last_published_at"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                    "%Y-%m-%d %H:%M:%S"
                )
            else:
                last_published_at = ""
            rows += page_row_template.format(
                id=summary["id"],
                url=summary["url"],
                title=summary["title"],
                last_published_at=last_published_at,
                draft=f"<a href='{summary['url']}?draft_token={summary['draft_token']}' target='_blank'>draft</a>" if summary["draft_token"] else "",
                languages=", ".join([f"<a href='{summary['url']}?lang={l}' target='_blank'>{l}</a>" for l in summary["languages"]])
            )
        if rows:
            tbodies += tbody_template.format(page_type=page_type.replace("great_international.", ""), rows=rows)
    return table_template.format(tbodies=tbodies)


def save_report(content: str):
    with open("./reports/index.html", "w") as report_file:
        report_file.write(content)


if __name__ == "__main__":
    report = international_pages_status_report()
    html = generate_html_report(report)
    save_report(html)
