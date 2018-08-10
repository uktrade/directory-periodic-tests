#!/usr/bin/env python3
import glob
import os
import sys
from collections import namedtuple
from typing import List, Tuple

from bs4 import BeautifulSoup

REPORT_FILE = os.getenv("REPORT_FILE", "index.html")
REPORT_DIRECTORY = os.getenv("REPORT_DIRECTORY", "./reports")

Summary = namedtuple(
    "Summary", ["filename", "url", "errors", "warnings", "notices"]
)


def find_html_report_files() -> List[str]:
    path = os.path.join(REPORT_DIRECTORY, "*.html")
    files = glob.glob(path)
    try:
        files.remove(os.path.join(REPORT_DIRECTORY, REPORT_FILE))
    except ValueError:
        pass
    return files


def extract_summary_from_report_file(file_path: str) -> Summary:
    with open(file_path, "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.div.h1.text
    errors, warnings, notices = (
        int(word)
        for span in soup.find_all("span")
        for word in span.text.split()
        if word and word.isdigit()
    )
    url_start = h1.find('"') + 1
    url_stop = h1.rfind('"')
    url = h1[url_start:url_stop]
    file_name = os.path.basename(file_path)

    return Summary(file_name, url, errors, warnings, notices)


def get_report_summaries(html_report_file_paths: List[str]) -> List[Summary]:
    summaries = []
    for report_file_path in html_report_file_paths:
        summaries.append(extract_summary_from_report_file(report_file_path))

    return sorted(summaries, key=lambda summary: (summary.errors, summary.url), reverse=True)


def generate_report_index(summaries: List[Summary]) -> str:
    doc_template = """<html>
    <body>
        <table> 
        <tr>
            <th>URL</th>
            <th>Errors</th>
            <th>Warnings</th>
            <th>Notices</th>
        </tr>
        {rows}
        </table> 
    </body>
    </html>
    """
    rows = []
    for summary in summaries:
        filename = summary.filename
        url = summary.url
        errors = summary.errors
        warnings = summary.warnings
        notices = summary.notices
        row = """
        <tr>
            <td><a href=\"{filename}\">{url}</a></td>
            <td style="background-color:#ff9696;text-align:center">{errors}</td>
            <td style="background-color:#e7c12b;text-align:center">{warnings}</td>
            <td style="background-color:#b6d0ff;text-align:center">{notices}</td>
        </tr>
        """.format(
            filename=filename,
            url=url,
            errors=errors,
            warnings=warnings,
            notices=notices,
        )
        rows.append(row)
    return doc_template.format(rows="\n\t".join(rows))


def save_report_index(html: str):
    path = os.path.join(REPORT_DIRECTORY, REPORT_FILE)
    with open(path, "w") as report:
        report.write(html)


if __name__ == "__main__":
    html_report_file_paths = find_html_report_files()
    summaries = get_report_summaries(html_report_file_paths)
    html = generate_report_index(summaries)
    save_report_index(html)
    number_of_errors = sum(summary.errors for summary in summaries)
    if number_of_errors > 0:
        sys.stderr.write(
            "Pa11y found {} issues on {} pages. Please check the index.html\n"
            .format(number_of_errors, len(summaries))
        )
        sys.exit(number_of_errors)
    else:
        sys.stdout.write("Pa11y found no errors")
