import glob
from typing import List

import os

from behave.runner import Context

REPORT_FILE = os.getenv("REPORT_FILE", "index.html")
REPORT_DIRECTORY = os.getenv("REPORT_DIRECTORY", "./reports")


def find_html_report_files() -> List[str]:
    path = os.path.join(REPORT_DIRECTORY, "*.html")
    file_paths = glob.glob(path)
    try:
        file_paths.remove(os.path.join(REPORT_DIRECTORY, REPORT_FILE))
    except ValueError:
        pass
    return file_paths


def generate_report_index(file_paths: List[str]) -> str:
    doc_template = """<html>
    <body>
        <table> 
        <tr>
            <th>Report</th>
        </tr>
        {rows}
        </table> 
    </body>
    </html>
    """
    rows = []
    for path in file_paths:
        file_name = path.replace("./reports/", "")
        row = f"""
        <tr>
            <td><a href="{file_name}">{file_name}</a></td>
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
