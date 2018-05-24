Periodical tests & tasks
------------------------

This repository contains simple tests & tasks that have to be run periodically.


# Dead links

This script will look for internal and external links that return status codes
other than `200 OK`.

An example error will look like this:
```ascii
ERROR Crawled 2055 urls with 13 error(s) in 128.82 seconds

  not found (404): https://invest.great.gov.uk/privacy-and-cookies/fair-processing-notice-export-opportunities
    from https://www.great.gov.uk/terms-and-conditions/
    from https://www.great.gov.uk/international/terms-and-conditions/?lang=en-gb
...
```

## Requirements

```shell
mkvirtualenv -p python3.5 dead_links
pip install -r requirements_dead_links.txt
```

## Running

```shell
TEST_ENV=DEV make dead_links_check
TEST_ENV=STAGE make dead_links_check
TEST_ENV=PROD make dead_links_check
```

# Geckoboard updater

Please refer to the documentation in `./geckoboard_updater` directory

