#!/usr/bin/env python3
import glob
import os
from collections import namedtuple
from typing import List, Tuple

from bs4 import BeautifulSoup

REPORT_FILE = os.getenv("REPORT_FILE", "index.html")

Summary = namedtuple(
    "Summary", ["filename", "url", "errors", "warnings", "notices"]
)


def find_html_report_files() -> List[str]:
    files = glob.glob("*.html")
    try:
        files.remove(REPORT_FILE)
    except ValueError:
        pass
    return files


def extract_summary_from_report_file(filename: str) -> Summary:
    with open(filename, "r") as f:
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

    return Summary(filename, url, errors, warnings, notices)


def get_report_summaries(html_report_file_names: List[str]) -> List[Summary]:
    summaries = []
    for report_filename in html_report_file_names:
        summaries.append(extract_summary_from_report_file(report_filename))

    return sorted(summaries, key=lambda summary: summary.url)


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
    with open(REPORT_FILE, "w") as report:
        report.write(html)


if __name__ == "__main__":
    html_report_file_names = find_html_report_files()
    summaries = get_report_summaries(html_report_file_names)
    html = generate_report_index(summaries)
    save_report_index(html)
