Geckoboard Updater
------------------

A script that extracts data from Jira & CircleCi and pushes it to Geckoboard.

How this script works:
* CircleCI workflows, which run smoke, functional, load & browser tests are 
    controlled by this [config.yml](https://github.com/uktrade/directory-tests/blob/master/.circleci/config.yml)
* Geckoboards are updated by `geckoboard_updater` script which is part of this repo
* `geckoboard_updater` is periodically run on CircleCI (check 
    [.circleci/config.yml](https://github.com/uktrade/directory-periodic-tests/blob/master/.circleci/config.yml))
* It polls CircleCI and Jira in order to extract test build data & load test 
    results from CircleCI and tickets metadata from Jira
* Once the data is pulled from both CircleCI & Jira it's transformed into 
    simple JSON data structures which can be processed by Geckoboard. 
    In Geckoboard's lingo they call them `datasets` (defined with `dataset schemas` 
    which have to be pushed to Geckoboard before you send any datatests)
* Once datasets are pushed to GeckoBoard then you can visualize data using various diagrams


# Requirements

* Python 3.5+ (it should work with Python 2.7 as well)
* [circleclient](https://pypi.org/project/circleclient/) → CircleCI API client
* [geckoboard.py](https://pypi.org/project/geckoboard.py/) → Geckoboard
    Datasetss API client
* [jira](https://pypi.org/project/jira/) → Jira REST API client


# Environment variables

All env variables are in rattic (look for Geckoboard updater)
Here's a list of required environment variables:

* `CIRCLE_CI_API_TOKEN` → API token which you can get [here](https://circleci.com/account/api)
* `GECKOBOARD_API_KEY` → API key which you can get [here](https://app.geckoboard.com/account/details)
* `GECKOBOARD_TEST_RESULTS_WIDGET_KEY` → Custom widget key, to which a HTML test results report is sent, [QA dashboard dashboard](https://app.geckoboard.com/edit/dashboards/264228)
* `GECKOBOARD_DIRECTORY_TESTS_RESULTS_WIDGET_KEY` → Custom widget key, [QA dashboard dashboard](https://app.geckoboard.com/edit/dashboards/264228)
* `GECKOBOARD_PERIODIC_TESTS_RESULTS_WIDGET_KEY` → Custom widget key, [QA dashboard dashboard](https://app.geckoboard.com/edit/dashboards/264228)
* `GECKOBOARD_CONTENT_JIRA_QUERY_LINKS_WIDGET_KEY` → Custom widget key, [CMS - Jira stats dashboard](https://app.geckoboard.com/edit/dashboards/296262)
* `GECKOBOARD_LINKS_TO_USEFUL_CONTENT_TEST_JOBS_WIDGET_KEY` → Custom widget key, [CMS - content stats dashboard](https://app.geckoboard.com/edit/dashboards/277009)
* `GECKOBOARD_TOOLS_JIRA_QUERY_LINKS_WIDGET_KEY` → Custom widget key, [TT - Jira stats](https://app.geckoboard.com/edit/dashboards/296257)
* `JIRA_HOST` → URL to your Jira instance e.g.: `https://{your_orgranisation}.atlassian.net/`
* `JIRA_USERNAME` → Jira username
* `JIRA_TOKEN` →  Jira API Token [^1]

Optional env var:
* `GECKOBOARD_PUSH_URL` → Set it if you have a private instance of Geckoboard otherwise it will default to: `https://push.geckoboard.com/v1/send/`


[^1]: → more on [Jira API Tokens](https://confluence.atlassian.com/cloud/api-tokens-938839638.html) used by [Python Jira REST API client](https://jira.readthedocs.io/en/latest/examples.html#http-basic)


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

