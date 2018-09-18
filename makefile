# default to TRADE DEV environment if TEST_ENV is not set
TEST_ENV ?= DEV

PYLINKVALIDATE_ENV_VARS_PROD := \
	export IGNORED_PREFIXES="https://www.nationalarchives.gov.uk/doc/open-government-licence,https://www.contactus.trade.gov.uk/office-finder/,http://mojolife.org.uk/,http://www.epcmortgage.org.uk/,https://invest.great.gov.uk/pt/industries/financial-services/,https://invest.great.gov.uk/de/industries/food-and-drink/,https://www.airforilfe.net,https://www.callidusgroup.co.uk,http://www.mbe-intl.com,http://www.jubaris.co.uk,http://www.elearningschool.co.uk,https://www.rmlgroup.com,https://www.gov.uk/tendering-for-public-sector-contracts/overview,https://www.contactus.trade.gov.uk/enquiry/topic,https://trade.great.gov.uk/search/,https://www.linkedin.com,https://twitter.com,https://public-directory-supplier-gds.s3.amazonaws.com,https://www.facebook.com,https://directory-cms-public.s3.amazonaws.com,https://uk.linkedin.com/,http://www.linkedin.com,http://exportbritain.org.uk/international-directory/,http://p2pfa.info/platforms/,http://www.ftsolutions.co.uk,http://www.export.org.uk/page/Market_Selection,http://www.macduffshipdesign.com,https://www.pwc.co.uk/" && \
	export TEST_URLS="https://www.great.gov.uk/ https://trade.great.gov.uk/ https://find-a-buyer.export.great.gov.uk/ https://sso.trade.great.gov.uk/accounts/login/ https://profile.great.gov.uk/about/ https://invest.great.gov.uk/ https://opportunities.export.great.gov.uk/ https://selling-online-overseas.export.great.gov.uk/ https://dev.invest.directory.uktrade.io/high-potential-opportunities/lightweight-structures/ https://dev.invest.directory.uktrade.io/high-potential-opportunities/agritech/ https://dev.invest.directory.uktrade.io/high-potential-opportunities/rail-infrastructure/"

PYLINKVALIDATE_ENV_VARS_STAGE := \
	export IGNORED_PREFIXES="https://www.nationalarchives.gov.uk/doc/open-government-licence,https://www.contactus.trade.gov.uk/office-finder/,http://mojolife.org.uk/,http://www.epcmortgage.org.uk/,https://invest.great.gov.uk/pt/industries/financial-services/,https://invest.great.gov.uk/de/industries/food-and-drink/,https://www.airforilfe.net,https://www.callidusgroup.co.uk,http://www.mbe-intl.com,http://www.jubaris.co.uk,http://www.elearningschool.co.uk,https://www.rmlgroup.com,https://www.gov.uk/tendering-for-public-sector-contracts/overview,https://www.contactus.trade.gov.uk,https://stage.supplier.directory.uktrade.io/search/,https://stage.supplier.directory.uktrade.io/suppliers/,https://www.linkedin.com,https://uk.linkedin.com/,http://www.linkedin.com,https://twitter.com,https://www.facebook.com,http://exportbritain.org.uk/international-directory/,http://p2pfa.info/platforms/,http://www.ftsolutions.co.uk,http://www.export.org.uk/page/Market_Selection,http://www.macduffshipdesign.com,https://www.pwc.co.uk/" && \
	export TEST_URLS="https://stage.exportreadiness.directory.uktrade.io/ https://stage.supplier.directory.uktrade.io/ https://stage.buyer.directory.uktrade.io/ https://stage.sso.uktrade.io/accounts/login/ https://stage.profile.uktrade.io/about/ https://invest.great.uat.uktrade.io/ https://selling-online-overseas.export.staging.uktrade.io/ https://opportunities.export.staging.uktrade.io/"

PYLINKVALIDATE_ENV_VARS_DEV := \
	export IGNORED_PREFIXES="https://www.nationalarchives.gov.uk/doc/open-government-licence,https://www.contactus.trade.gov.uk/office-finder/,http://mojolife.org.uk/,http://www.epcmortgage.org.uk/,https://invest.great.gov.uk/pt/industries/financial-services/,https://invest.great.gov.uk/de/industries/food-and-drink/,https://www.airforilfe.net,https://www.callidusgroup.co.uk,http://www.mbe-intl.com,http://www.jubaris.co.uk,http://www.elearningschool.co.uk,https://www.rmlgroup.com,https://www.gov.uk/tendering-for-public-sector-contracts/overview,https://www.contactus.trade.gov.uk,https://dev.supplier.directory.uktrade.io/search/,https://dev.supplier.directory.uktrade.io/suppliers/,https://www.linkedin.com,https://uk.linkedin.com/,http://www.linkedin.com,https://twitter.com,https://www.facebook.com,http://exportbritain.org.uk/international-directory/,http://p2pfa.info/platforms/,http://www.ftsolutions.co.uk,http://www.export.org.uk/page/Market_Selection,http://www.macduffshipdesign.com,https://www.pwc.co.uk/" && \
	export TEST_URLS="https://dev.exportreadiness.directory.uktrade.io/ https://dev.supplier.directory.uktrade.io/ https://dev.buyer.directory.uktrade.io/ https://www.dev.sso.uktrade.io/accounts/login/ https://dev.profile.uktrade.io/about/"

dead_links_check:
	$(PYLINKVALIDATE_ENV_VARS_$(TEST_ENV)) && \
	echo "Running pylinkvalidate against: $${TEST_URLS} environment" && \
	pylinkvalidate.py \
	    --progress \
	    --console \
	    --timeout=55 \
	    --depth=5 \
	    --workers=10 \
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


cms_pages_check:
	echo "Running CMS pages check against: $(CMS_URL)" && \
	pytest --junit-xml=./reports/cms_pages.xml cms_pages/


# compare contents of Staging & Dev environments by default
ENVS_TO_COMPARE ?= stage_dev

invest_compare_content:
	behave -k -t ~wip --junit --junit-directory=./reports/ invest_migration/features/$(ENVS_TO_COMPARE).feature


check_for_x_robots_tag_header:
	behave -k -t ~wip -t ~fixme --junit --junit-directory=./reports/ x_robots_header/


clean:
	rm -fr ./reports/*.json ./reports/*.html ./reports/*.xml ./reports/*.log

