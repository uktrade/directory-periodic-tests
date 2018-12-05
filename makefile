# default to TRADE DEV environment if TEST_ENV is not set
TEST_ENV ?= DEV

PYLINKVALIDATE_ENV_VARS_PROD := \
	export IGNORED_PREFIXES="http://exportbritain.org.uk/international-directory/,http://mojolife.org.uk/,http://p2pfa.info/platforms/,http://www.elearningschool.co.uk,http://www.epcmortgage.org.uk/,http://www.export.org.uk/page/Market_Selection,http://www.ftsolutions.co.uk,http://www.jubaris.co.uk,http://www.linkedin.com,http://www.macduffshipdesign.com,http://www.mbe-intl.com,https://directory-cms-public.s3.amazonaws.com,https://public-directory-supplier-gds.s3.amazonaws.com,https://trade.great.gov.uk/search/,https://twitter.com,https://uk.linkedin.com/,https://www.airforilfe.net,https://www.callidusgroup.co.uk,https://www.contactus.trade.gov.uk/office-finder/,https://www.facebook.com,https://www.gov.uk/tendering-for-public-sector-contracts,https://www.great.gov.uk/sso/accounts/login/?next=,https://www.great.gov.uk/sso/accounts/password/reset/?next=,https://www.great.gov.uk/sso/accounts/signup/?next=,https://www.linkedin.com,https://www.nationalarchives.gov.uk/doc/open-government-licence,https://www.pwc.co.uk/,https://www.rmlgroup.com,https://invest.great.gov.uk/de/industries/food-and-drink,https://invest.great.gov.uk/pt/industries/financial-services,https://www.contactus.trade.gov.uk/office-finder" && \
	export TEST_URLS="https://www.great.gov.uk/ https://www.great.gov.uk/find-a-buyer/ https://www.great.gov.uk/sso/accounts/login/ https://www.great.gov.uk/profile/about/ https://invest.great.gov.uk/ https://trade.great.gov.uk/ https://opportunities.export.great.gov.uk/ https://selling-online-overseas.export.great.gov.uk/ https://selling-online-overseas.export.great.gov.uk/markets/results/"

PYLINKVALIDATE_ENV_VARS_STAGE := \
	export IGNORED_PREFIXES="http://exportbritain.org.uk/international-directory/,http://mojolife.org.uk/,http://p2pfa.info/platforms/,http://www.elearningschool.co.uk,http://www.epcmortgage.org.uk/,http://www.export.org.uk/page/Market_Selection,http://www.ftsolutions.co.uk,http://www.jubaris.co.uk,http://www.linkedin.com,http://www.macduffshipdesign.com,http://www.mbe-intl.com,https://great.uat.uktrade.io/sso/accounts/login/?next,https://great.uat.uktrade.io/sso/accounts/password/reset/?next,https://great.uat.uktrade.io/sso/accounts/signup/?next,https://great.uat.uktrade.io/trade/search/,https://twitter.com,https://uk.linkedin.com/,https://www.airforilfe.net,https://www.callidusgroup.co.uk,https://www.contactus.trade.gov.uk/office-finder/,https://www.facebook.com,https://www.gov.uk/tendering-for-public-sector-contracts/overview,https://www.linkedin.com,https://www.nationalarchives.gov.uk/doc/open-government-licence,https://www.pwc.co.uk/,https://www.rmlgroup.com,https://www.contactus.trade.gov.uk/office-finder" && \
	export TEST_URLS="https://great.uat.uktrade.io/ https://great.uat.uktrade.io/trade/ https://great.uat.uktrade.io/find-a-buyer/ https://great.uat.uktrade.io/sso/accounts/login/ https://great.uat.uktrade.io/profile/about https://invest.great.uat.uktrade.io/ https://selling-online-overseas.export.staging.uktrade.io/ https://opportunities.export.staging.uktrade.io/"

PYLINKVALIDATE_ENV_VARS_DEV := \
	export IGNORED_PREFIXES="https://www.nationalarchives.gov.uk/doc/open-government-licence,https://www.contactus.trade.gov.uk/office-finder/,http://mojolife.org.uk/,http://www.epcmortgage.org.uk/,https://invest.great.gov.uk/pt/industries/financial-services/,https://invest.great.gov.uk/de/industries/food-and-drink/,https://www.airforilfe.net,https://www.callidusgroup.co.uk,http://www.mbe-intl.com,http://www.jubaris.co.uk,http://www.elearningschool.co.uk,https://www.rmlgroup.com,https://www.gov.uk/tendering-for-public-sector-contracts/overview,https://www.contactus.trade.gov.uk,https://dev.supplier.directory.uktrade.io/search/,https://dev.supplier.directory.uktrade.io/suppliers/,https://www.linkedin.com,https://uk.linkedin.com/,http://www.linkedin.com,https://twitter.com,https://www.facebook.com,http://exportbritain.org.uk/international-directory/,http://p2pfa.info/platforms/,http://www.ftsolutions.co.uk,http://www.export.org.uk/page/Market_Selection,http://www.macduffshipdesign.com,https://www.pwc.co.uk/,https://dev.sso.uktrade.io/accounts/signup/?next=,https://dev.sso.uktrade.io/accounts/login/?next=,https://www.dev.sso.uktrade.io/accounts/password/reset/?next=" && \
	export TEST_URLS="https://dev.exportreadiness.directory.uktrade.io/ https://dev.supplier.directory.uktrade.io/ https://dev.buyer.directory.uktrade.io/ https://www.dev.sso.uktrade.io/accounts/login/ https://dev.profile.uktrade.io/about/ https://dev.invest.directory.uktrade.io/high-potential-opportunities/lightweight-structures/ https://dev.invest.directory.uktrade.io/high-potential-opportunities/agritech/ https://dev.invest.directory.uktrade.io/high-potential-opportunities/rail-infrastructure/"

dead_links_check:
	$(PYLINKVALIDATE_ENV_VARS_$(TEST_ENV)) && \
	echo "Running pylinkvalidate against: $${TEST_URLS} environment" && \
	pylinkvalidate.py \
	    --progress \
	    --console \
	    --timeout=55 \
	    --depth=5 \
	    --workers=5 \
	    --test-outside \
	    --parser=lxml \
	    --format=junit \
	    --output=./reports/dead_links_report.xml \
	    --header="Connection: keep-alive" \
	    --header="Pragma: no-cache" \
	    --header="Cache-Control: no-cache" \
	    --header="Upgrade-Insecure-Requests: 1" \
	    --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8" \
	    --header="DNT: 1" \
	    --header="Accept-Encoding: gzip, deflate" \
	    --header="User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36 link-checker-qa" \
	    --ignore="$${IGNORED_PREFIXES}" \
	    $${TEST_URLS}


dead_links_check_with_json_report:
	$(PYLINKVALIDATE_ENV_VARS_$(TEST_ENV)) && \
	echo "Running pylinkvalidate against: $${TEST_URLS} environment" && \
	pylinkvalidate.py \
	    --progress \
	    --console \
	    --timeout=55 \
	    --depth=5 \
	    --workers=10 \
	    --test-outside \
	    --report-type=all \
	    --parser=lxml \
	    --format=json \
	    --output=./reports/dead_links_report.json \
	    --header="Connection: keep-alive" \
	    --header="Pragma: no-cache" \
	    --header="Cache-Control: no-cache" \
	    --header="Upgrade-Insecure-Requests: 1" \
	    --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8" \
	    --header="DNT: 1" \
	    --header="Accept-Encoding: gzip, deflate" \
	    --header="User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36 link-checker-qa" \
	    --ignore="$${IGNORED_PREFIXES}" \
	    $${TEST_URLS}


cms_pages_check:
	echo "Running CMS pages check against: $(DIRECTORY_CMS_API_CLIENT_BASE_URL)" && \
	pytest --capture=no --verbose --junit-xml=./reports/cms_pages.xml cms_pages/


# compare contents of Staging & Dev environments by default
SERVICE ?= invest
ENVS_TO_COMPARE ?= stage_dev

compare_content:
	behave -k -t ~wip --junit --junit-directory=./reports/ content_diff/features/$(SERVICE)_$(ENVS_TO_COMPARE).feature


check_for_x_robots_tag_header:
	behave -k -t ~wip -t ~fixme --junit --junit-directory=./reports/ x_robots_header/


clean:
	rm -fr ./reports/*.json ./reports/*.html ./reports/*.xml ./reports/*.log

