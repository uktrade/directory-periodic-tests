import glob
from typing import List

import os

from behave.runner import Context
from collections import namedtuple


REPORT_FILE = os.getenv("REPORT_FILE", "index.html")
REPORT_DIRECTORY = os.getenv("REPORT_DIRECTORY", "./reports")

Summary = namedtuple(
    "Summary", ["file_name", "result", "color"]
)


def find_html_report_files() -> List[str]:
    path = os.path.join(REPORT_DIRECTORY, "*.html")
    file_paths = glob.glob(path)
    try:
        file_paths.remove(os.path.join(REPORT_DIRECTORY, REPORT_FILE))
    except ValueError:
        pass
    return file_paths


def extract_summary_from_report_file(file_path: str) -> Summary:
    with open(file_path, "r") as f:
        html = f.read().replace("&nbsp;", " ")

    result = "Found differences"
    no_differences_found = "No Differences Found"
    not_found = "This page cannot be found"
    color = "#ff0040"

    if no_differences_found in html:
        result = no_differences_found
        color = "#00ff80"
    if not_found in html:
        result = not_found
        color = "#00bfff"

    file_name = file_path.replace("./reports/", "")
    return Summary(file_name, result, color)


def get_report_summaries(html_report_file_paths: List[str]) -> List[Summary]:
    summaries = []
    for report_file_path in html_report_file_paths:
        summaries.append(extract_summary_from_report_file(report_file_path))

    return sorted(summaries, key=lambda summary: summary.file_name)


def generate_report_index(summaries: List[Summary]) -> str:

    doc_template = """<html>
    <body>
        <table> 
        <tr>
            <th>Report</th>
            <th>Result</th>
        </tr>
        {rows}
        </table> 
    </body>
    </html>
    """
    rows = []
    for summary in sorted(summaries):
        file_name = summary.file_name
        result = summary.result
        color = summary.color
        row = f"""
        <tr>
            <td><a href="{file_name}">{file_name}</a></td>
            <td style="background-color:{color};text-align:center">{result}</td>
        </tr>
        """
        rows.append(row)
    return doc_template.format(rows="\n\t".join(rows))


def save_report_index(html: str):
    path = os.path.join(REPORT_DIRECTORY, REPORT_FILE)
    with open(path, "w") as report:
        report.write(html)


def after_all(context: Context):
    html_report_file_paths = find_html_report_files()
    html = generate_report_index(html_report_file_paths)
    save_report_index(html)
