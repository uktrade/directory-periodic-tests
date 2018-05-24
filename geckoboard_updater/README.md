Geckoboard Updater
------------------

A script that extracts data from Jira & CircleCi and pushes it to Geckoboard.


# Requirements

* Python 3.5+ (it should work with Python 2.7 as well)
* [circleclient](https://pypi.org/project/circleclient/) → CircleCI API client
* [geckoboard.py](https://pypi.org/project/geckoboard.py/) → Geckoboard
    Datasetss API client
* [jira](https://pypi.org/project/jira/) → Jira REST API client


# Environment variables

Here's a list of required environment variables:

* `CIRCLE_CI_API_TOKEN` → API token which you can get [here](https://circleci.com/account/api)
* `GECKOBOARD_API_KEY` → API key which you can get [here](https://app.geckoboard.com/account/details)
* `GECKOBOARD_PUSH_URL` → Set it if you have a private instance of Geckoboard otherwise it will default to: `https://push.geckoboard.com/v1/send/`
* `GECKOBOARD_TEST_RESULTS_WIDGET_KEY` → Custom widget key, to which a HTML test
    results report is sent
* `JIRA_HOST` → URL to your Jira instance e.g.: `https://{your_orgranisation}.atlassian.net/`
* `JIRA_USERNAME` → Jira username [^1]
* `JIRA_PASSWORD` →  Jira password [^1]

[^1]: → will be replaced with [OAuth Access Tokens](https://developer.atlassian.com/server/jira/platform/oauth/)


# Running

Once all required environment variables are set, simply run it:
```
./geckoboard_updater.py
```

# Jira labels

This script requires that bugs raised in Jira are labelled with tags prefixed 
with `qa_`, e.g.:

* `qa_accessibility` → accessibility issue
* `qa_backend` → backend issue, e.g. caching, DB, parsing etc.
* `qa_browser` → a browser compatibility issue
* `qa_content` → content related issues, typos, missing or invalid text etc.
* `qa_functional` → functional issue
* `qa_mobile` → an issue affecting only mobile devices
* `qa_ui` → UI specific issue e.g. missing or invalid styling etc.

These labels will be used to generate datasets for Geckoboard widgets.


## Special Jira labels

There are also three Jira labels that have special purpose:

* `qa_auto` & `qa_manual` → tags issues which were found by automated tests or
    during manual testing. They're used to create a widget that compares the
    number of bugs found both ways.
* `qa_automated_scenario` → tag `Task` or `Sub-task` for automating a test
    scenario. This is used to generate the `Scenarios to automate` counter.


# CircleCI build status report

This script also connects to CircleCI and extracts information about recent
builds for designated projects. It supports both `v1` and `v2` CircleCI jobs.

Please refer to function: `circle_ci_get_last_test_results_per_project()` for
more details.

Below is a list of currently monitored projects:

* [directory-api](https://github.com/uktrade/directory-api)
* [directory-companies-house-search](https://github.com/uktrade/directory-companies-house-search)
* [directory-sso](https://github.com/uktrade/directory-sso)
* [directory-sso-profile](https://github.com/uktrade/directory-sso-profile)
* [directory-sso-proxy](https://github.com/uktrade/directory-sso-proxy)
* [directory-ui-buyer](https://github.com/uktrade/directory-ui-buyer)
* [directory-ui-export-readiness](https://github.com/uktrade/directory-ui-export-readiness)
* [directory-ui-supplier](https://github.com/uktrade/directory-ui-supplier)

