.PHONY: clean

clean:
	rm -fr ./reports/*.json ./reports/*.html ./reports/*.xml ./reports/*.log

# default to TRADE DEV environment if TEST_ENV is not set
TEST_ENV ?= DEV

PYLINKVALIDATE_ENV_VARS_PROD := \
	export IGNORED_PREFIXES="\
	https://www.great.gov.uk/profile/static/, \
	https://www.great.gov.uk/sso/accounts/login/, \
	https://www.great.gov.uk/sso/accounts/password/reset/, \
	https://www.great.gov.uk/sso/accounts/signup/, \
	https://www.great.gov.uk/sso/static/, \
	https://www.great.gov.uk/trade/search/?term=, \
	https://www.great.gov.uk/trade/static/, \
	https://www.great.gov.uk/trade/suppliers/, \
	https://www.great.gov.uk/static/, \
	https://cms.trade.great.gov.uk/documents/, \
	https://directory-cms-public.s3.amazonaws.com, \
	https://selling-online-overseas.export.great.gov.uk/static/, \
	https://www.great.gov.uk/export-opportunities/opportunities/1, \
	https://www.great.gov.uk/export-opportunities/opportunities/2, \
	https://www.great.gov.uk/export-opportunities/opportunities/3, \
	https://www.great.gov.uk/export-opportunities/opportunities/4, \
	https://www.great.gov.uk/export-opportunities/opportunities/5, \
	https://www.great.gov.uk/export-opportunities/opportunities/6, \
	https://www.great.gov.uk/export-opportunities/opportunities/7, \
	https://www.great.gov.uk/export-opportunities/opportunities/8, \
	https://www.great.gov.uk/export-opportunities/opportunities/9, \
	https://www.great.gov.uk/export-opportunities/opportunities/b, \
	https://www.great.gov.uk/export-opportunities/opportunities/c, \
	https://www.great.gov.uk/export-opportunities/opportunities/d, \
	https://www.great.gov.uk/export-opportunities/opportunities/e, \
	https://www.great.gov.uk/export-opportunities/opportunities/f, \
	https://www.great.gov.uk/export-opportunities/opportunities/g, \
	https://www.great.gov.uk/export-opportunities/opportunities/h, \
	https://www.great.gov.uk/export-opportunities/opportunities/j, \
	https://www.great.gov.uk/export-opportunities/opportunities/k, \
	https://www.great.gov.uk/export-opportunities/opportunities/l, \
	https://www.great.gov.uk/export-opportunities/opportunities/m, \
	https://www.great.gov.uk/export-opportunities/opportunities/n, \
	https://www.great.gov.uk/export-opportunities/opportunities/o, \
	https://www.great.gov.uk/export-opportunities/opportunities/p, \
	https://www.great.gov.uk/export-opportunities/opportunities/r, \
	https://www.great.gov.uk/export-opportunities/opportunities/s, \
	https://www.great.gov.uk/export-opportunities/opportunities/t, \
	https://www.great.gov.uk/export-opportunities/opportunities/u, \
	https://www.great.gov.uk/export-opportunities/opportunities/w, \
	https://www.great.gov.uk/export-opportunities/opportunities/z, \
	https://opportunities.export.great.gov.uk/opportunities/1, \
	https://opportunities.export.great.gov.uk/opportunities/2, \
	https://opportunities.export.great.gov.uk/opportunities/3, \
	https://opportunities.export.great.gov.uk/opportunities/4, \
	https://opportunities.export.great.gov.uk/opportunities/5, \
	https://opportunities.export.great.gov.uk/opportunities/6, \
	https://opportunities.export.great.gov.uk/opportunities/7, \
	https://opportunities.export.great.gov.uk/opportunities/8, \
	https://opportunities.export.great.gov.uk/opportunities/9, \
	https://opportunities.export.great.gov.uk/opportunities/b, \
	https://opportunities.export.great.gov.uk/opportunities/c, \
	https://opportunities.export.great.gov.uk/opportunities/d, \
	https://opportunities.export.great.gov.uk/opportunities/e, \
	https://opportunities.export.great.gov.uk/opportunities/f, \
	https://opportunities.export.great.gov.uk/opportunities/g, \
	https://opportunities.export.great.gov.uk/opportunities/h, \
	https://opportunities.export.great.gov.uk/opportunities/j, \
	https://opportunities.export.great.gov.uk/opportunities/k, \
	https://opportunities.export.great.gov.uk/opportunities/l, \
	https://opportunities.export.great.gov.uk/opportunities/m, \
	https://opportunities.export.great.gov.uk/opportunities/n, \
	https://opportunities.export.great.gov.uk/opportunities/o, \
	https://opportunities.export.great.gov.uk/opportunities/p, \
	https://opportunities.export.great.gov.uk/opportunities/r, \
	https://opportunities.export.great.gov.uk/opportunities/s, \
	https://opportunities.export.great.gov.uk/opportunities/t, \
	https://opportunities.export.great.gov.uk/opportunities/u, \
	https://opportunities.export.great.gov.uk/opportunities/w, \
	https://opportunities.export.great.gov.uk/opportunities/z, \
	https://opportunities.export.great.gov.uk/opportunities?paged=, \
	https://www.contactus.trade.gov.uk/office-finder/, \
	https://s3.eu-west-2.amazonaws.com/, \
	https://d3zwahhsvfb28.cloudfront.net, \
	https://seao.ca/OpportunityPublication, \
	http://www.linkedin.com, \
	http://ted.europa.eu, \
	https://twitter.com, \
	https://uk.linkedin.com/, \
	https://www.facebook.com, \
	https://www.facebook.com/login.php, \
	https://www.linkedin.com \
	" && \
	export TEST_URLS="\
	https://www.great.gov.uk/ \
	https://www.great.gov.uk/community/ \
	https://www.great.gov.uk/contact/ \
	https://www.great.gov.uk/contact/selling-online-overseas/organisation/ \
	https://www.great.gov.uk/find-a-buyer/ \
	https://www.great.gov.uk/sso/accounts/login/ \
	https://www.great.gov.uk/profile/about/ \
	https://www.great.gov.uk/trade/ \
	https://invest.great.gov.uk/ \
	https://invest.great.gov.uk/high-potential-opportunities/lightweight-structures/ \
	https://invest.great.gov.uk/high-potential-opportunities/food-production/ \
	https://invest.great.gov.uk/high-potential-opportunities/rail-infrastructure/ \
	https://opportunities.export.great.gov.uk/ \
	https://selling-online-overseas.export.great.gov.uk/ \
	https://selling-online-overseas.export.great.gov.uk/markets/results/ \
	"

PYLINKVALIDATE_ENV_VARS_UAT := \
	export IGNORED_PREFIXES="\
	https://great.uat.uktrade.io/international/static/, \
	https://great.uat.uktrade.io/find-a-buyer/static/,\
	https://great.uat.uktrade.io/profile/static/,\
	https://great.uat.uktrade.io/sso/accounts/login/?next,\
	https://great.uat.uktrade.io/sso/accounts/password/reset/?next,\
	https://great.uat.uktrade.io/sso/accounts/signup/?next,\
	https://great.uat.uktrade.io/sso/static/,\
	https://great.uat.uktrade.io/static/,\
	https://great.uat.uktrade.io/trade/search/?term=,\
	https://great.uat.uktrade.io/trade/static/,\
	https://great.uat.uktrade.io/trade/suppliers/,\
	https://invest.great.uat.uktrade.io/static/,\
	https://opportunities.export.great.uat.uktrade.io/assets/,\
	https://opportunities.export.great.uat.uktrade.io/opportunities?,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/a,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/b,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/c,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/d,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/m,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/f,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/g,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/h,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/j,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/k,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/m,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/n,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/m,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/p,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/r,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/s,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/t,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/w,\
	https://opportunities.export.great.uat.uktrade.io/opportunities/z,\
	https://great.uat.uktrade.io/contact/selling-online-overseas/static/,\
	https://www.contactus.trade.gov.uk/office-finder,\
	http://www.export.org.uk/page/Market_Selection,\
	https://www.gov.uk/tendering-for-public-sector-contracts/overview,\
	http://exportbritain.org.uk/international-directory/,\
	http://mojolife.org.uk/,\
	http://p2pfa.info/platforms/,\
	http://www.elearningschool.co.uk,\
	http://www.epcmortgage.org.uk/,\
	http://www.ftsolutions.co.uk,\
	http://www.jubaris.co.uk,\
	http://www.linkedin.com,\
	http://www.macduffshipdesign.com,\
	http://www.mbe-intl.com,\
	https://twitter.com,\
	https://uk.linkedin.com/,\
	https://www.airforilfe.net,\
	https://www.callidusgroup.co.uk,\
	https://www.facebook.com,\
	https://www.linkedin.com,\
	https://www.nationalarchives.gov.uk/doc/open-government-licence,\
	https://www.pwc.co.uk/,https://www.rmlgroup.com\
	" && \
	export TEST_URLS="\
	https://great.uat.uktrade.io/international/ \
	https://great.uat.uktrade.io/international/content/industries/ \
	https://great.uat.uktrade.io/international/content/how-to-setup-in-the-uk/ \
	https://great.uat.uktrade.io/international/content/how-to-do-business-with-the-uk/ \
	https://great.uat.uktrade.io/ \
	https://great.uat.uktrade.io/community \
	https://great.uat.uktrade.io/trade/ \
	https://great.uat.uktrade.io/find-a-buyer/ \
	https://great.uat.uktrade.io/sso/accounts/login/ \
	https://great.uat.uktrade.io/profile/about/ \
	https://great.uat.uktrade.io/contact/selling-online-overseas/ \
	https://great.uat.uktrade.io/contact/selling-online-overseas/markets/results/ \
	https://invest.great.uat.uktrade.io/ \
	https://invest.great.uat.uktrade.io/high-potential-opportunities/lightweight-structures/ \
	https://invest.great.uat.uktrade.io/high-potential-opportunities/food-production/ \
	https://invest.great.uat.uktrade.io/high-potential-opportunities/rail-infrastructure/ \
	https://opportunities.export.great.uat.uktrade.io/ \
	https://opportunities.export.great.uat.uktrade.io/opportunities?s=shoes&areas[]=&commit=Find+opportunities \
	"


PYLINKVALIDATE_ENV_VARS_STAGE := \
	export IGNORED_PREFIXES="\
	https://great.preprod.uktrade.io/international/static/, \
	https://great.staging.uktrade.io/find-a-buyer/static/,\
	https://great.staging.uktrade.io/profile/static/,\
	https://great.staging.uktrade.io/sso/accounts/login/?next,\
	https://great.staging.uktrade.io/sso/accounts/password/reset/?next,\
	https://great.staging.uktrade.io/sso/accounts/signup/?next,\
	https://great.staging.uktrade.io/sso/static/,\
	https://great.staging.uktrade.io/static/,\
	https://great.staging.uktrade.io/trade/search/?term=,\
	https://great.staging.uktrade.io/trade/static/,\
	https://great.staging.uktrade.io/trade/suppliers/,\
	https://invest.great.staging.uktrade.io/static/,\
	https://opportunities.export.great.staging.uktrade.io/assets/,\
	https://opportunities.export.great.staging.uktrade.io/opportunities?,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/a,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/b,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/c,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/d,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/m,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/f,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/g,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/h,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/j,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/k,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/m,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/n,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/m,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/p,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/r,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/s,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/t,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/w,\
	https://opportunities.export.great.staging.uktrade.io/opportunities/z,\
	https://great.staging.uktrade.io/export-opportunities/opportunities?,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/a,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/b,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/c,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/d,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/m,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/f,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/g,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/h,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/j,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/k,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/m,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/n,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/m,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/p,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/r,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/s,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/t,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/w,\
	https://great.staging.uktrade.io/export-opportunities/opportunities/z,\
	https://great.staging.uktrade.io/contact/selling-online-overseas/static/,\
	https://www.contactus.trade.gov.uk/office-finder,\
	http://www.export.org.uk/page/Market_Selection,\
	https://www.gov.uk/tendering-for-public-sector-contracts/overview,\
	http://exportbritain.org.uk/international-directory/,\
	http://mojolife.org.uk/,\
	http://p2pfa.info/platforms/,\
	http://www.elearningschool.co.uk,\
	http://www.epcmortgage.org.uk/,\
	http://www.ftsolutions.co.uk,\
	http://www.jubaris.co.uk,\
	http://www.linkedin.com,\
	http://www.macduffshipdesign.com,\
	http://www.mbe-intl.com,\
	https://twitter.com,\
	https://uk.linkedin.com/,\
	https://www.airforilfe.net,\
	https://www.callidusgroup.co.uk,\
	https://www.facebook.com,\
	https://www.linkedin.com,\
	https://www.nationalarchives.gov.uk/doc/open-government-licence,\
	https://www.pwc.co.uk/,https://www.rmlgroup.com\
	" && \
	export TEST_URLS="\
	https://great.staging.uktrade.io/international/ \
	https://great.staging.uktrade.io/international/content/industries/ \
	https://great.staging.uktrade.io/international/content/how-to-setup-in-the-uk/ \
	https://great.staging.uktrade.io/ \
	https://great.staging.uktrade.io/community \
	https://great.staging.uktrade.io/trade/ \
	https://great.staging.uktrade.io/find-a-buyer/ \
	https://great.staging.uktrade.io/sso/accounts/login/ \
	https://great.staging.uktrade.io/profile/about/ \
	https://great.staging.uktrade.io/contact/selling-online-overseas/ \
	https://great.staging.uktrade.io/contact/selling-online-overseas/markets/results/ \
	https://invest.great.staging.uktrade.io/ \
	https://invest.great.staging.uktrade.io/high-potential-opportunities/lightweight-structures/ \
	https://invest.great.staging.uktrade.io/high-potential-opportunities/food-production/ \
	https://invest.great.staging.uktrade.io/high-potential-opportunities/rail-infrastructure/ \
	https://opportunities.export.great.staging.uktrade.io/ \
	https://opportunities.export.great.staging.uktrade.io/opportunities?s=shoes&areas[]=&commit=Find+opportunities \
	"

PYLINKVALIDATE_ENV_VARS_DEV := \
	export IGNORED_PREFIXES="\
	https://great.dev.uktrade.io/find-a-buyer/static/,\
	https://great.dev.uktrade.io/profile/static/,\
	https://great.dev.uktrade.io/sso/accounts/login/?next,\
	https://great.dev.uktrade.io/sso/accounts/password/reset/?next,\
	https://great.dev.uktrade.io/sso/accounts/signup/?next,\
	https://great.dev.uktrade.io/sso/static/,\
	https://great.dev.uktrade.io/static/,\
	https://great.dev.uktrade.io/international/static/,\
	https://great.dev.uktrade.io/trade/search/?term=,\
	https://great.dev.uktrade.io/trade/static/,\
	https://great.dev.uktrade.io/trade/suppliers/,\
	https://invest.great.dev.uktrade.io/static/,\
	https://selling-online-overseas.export.great.dev.uktrade.io/static/,\
	http://exportbritain.org.uk/international-directory/,\
	http://mojolife.org.uk/,\
	http://p2pfa.info/platforms/,\
	http://www.elearningschool.co.uk,\
	http://www.epcmortgage.org.uk/,\
	http://www.export.org.uk/page/Market_Selection,\
	http://www.ftsolutions.co.uk,\
	http://www.jubaris.co.uk,\
	http://www.linkedin.com,\
	http://www.macduffshipdesign.com,\
	http://www.mbe-intl.com,\
	https://twitter.com,\
	https://uk.linkedin.com/,\
	https://www.airforilfe.net,\
	https://www.callidusgroup.co.uk,\
	https://www.contactus.trade.gov.uk,\
	https://www.facebook.com,\
	https://www.gov.uk/tendering-for-public-sector-contracts/overview,\
	https://www.linkedin.com,\
	https://www.nationalarchives.gov.uk/doc/open-government-licence,\
	https://www.pwc.co.uk/,\
	https://www.rmlgroup.com\
	" && \
	export TEST_URLS="\
	https://great.dev.uktrade.io/ \
	https://great.dev.uktrade.io/community/ \
	https://great.dev.uktrade.io/international/ \
	https://great.dev.uktrade.io/trade/ \
	https://great.dev.uktrade.io/find-a-buyer/ \
	https://great.dev.uktrade.io/sso/accounts/login/ \
	https://great.dev.uktrade.io/profile/about/ \
	https://invest.great.dev.uktrade.io/ \
	https://invest.great.dev.uktrade.io/high-potential-opportunities/lightweight-structures/ \
	https://invest.great.dev.uktrade.io/high-potential-opportunities/food-production/ \
	https://invest.great.dev.uktrade.io/high-potential-opportunities/rail-infrastructure/ \
	https://selling-online-overseas.export.great.dev.uktrade.io/ \
	https://selling-online-overseas.export.great.dev.uktrade.io/markets/results/ \
	"

BASIC_AUTH := $(shell echo -n $(BASICAUTH_USER_$(TEST_ENV)):$(BASICAUTH_PASS_$(TEST_ENV)) | base64)

# Testing Production systems will check outside links
# Testing non-Production systems will not check outside links & HAWK cookie
# will be used.
ifndef BASICAUTH_USER_DEV
  $(error BASICAUTH_USER_DEV is undefined)
endif
ifndef BASICAUTH_PASS_DEV
  $(error BASICAUTH_PASS_DEV is undefined)
endif
ifndef BASICAUTH_USER_UAT
  $(error BASICAUTH_USER_UAT is undefined)
endif
ifndef BASICAUTH_USER_STAGE
  $(error BASICAUTH_USER_STAGE is undefined)
endif
ifndef BASICAUTH_PASS_STAGE
  $(error BASICAUTH_PASS_STAGE is undefined)
endif

ifeq ($(TEST_ENV),PROD)
	AUTH=
	TEST_OUTSIDE=--test-outside
else
ifeq ($(TEST_ENV),UAT)
	AUTH=--header='Authorization: Basic ${BASIC_AUTH}'
	TEST_OUTSIDE=
endif
ifeq ($(TEST_ENV),STAGE)
	AUTH=--header='Authorization: Basic ${BASIC_AUTH}'
	TEST_OUTSIDE=
endif
ifeq ($(TEST_ENV),DEV)
	AUTH=--header='Authorization: Basic ${BASIC_AUTH}'
	TEST_OUTSIDE=
endif
endif

dead_links_check:
	$(PYLINKVALIDATE_ENV_VARS_$(TEST_ENV)) && \
	echo -e "Running pylinkvalidate against: $${TEST_URLS}\n" && \
	echo -e "IGNORED_PREFIXES: `echo $${IGNORED_PREFIXES} | tr -d [:space:]`\n" && \
	pylinkvalidate.py \
	    --progress \
	    --console \
	    --timeout=55 \
	    --depth=5 \
	    --workers=10 \
	    --types=a \
	    $(TEST_OUTSIDE) \
	    --parser=lxml \
	    --format=junit \
	    --output="./reports/dead_links_report.xml" \
	    --header="Connection: keep-alive" \
	    --header="Pragma: no-cache" \
	    --header="Cache-Control: no-cache" \
	    --header="Upgrade-Insecure-Requests: 1" \
	    --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8" \
	    --header="DNT: 1" \
	    --header="User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36 link-checker-qa" \
	    $(AUTH) \
	    --ignore=`echo $${IGNORED_PREFIXES} | tr -d [:space:]` \
	    $${TEST_URLS}

dead_links_check_with_json_report:
	$(PYLINKVALIDATE_ENV_VARS_$(TEST_ENV)) && \
	echo -e "Running pylinkvalidate against: $${TEST_URLS}\n" && \
	echo -e "IGNORED_PREFIXES: `echo $${IGNORED_PREFIXES} | tr -d [:space:]`\n" && \
	pylinkvalidate.py \
	    --progress \
	    --console \
	    --timeout=55 \
	    --depth=5 \
	    --workers=10 \
	    --types=a,img,link,script \
	    $(TEST_OUTSIDE) \
	    --report-type=all \
	    --parser=lxml \
	    --format=json \
	    --output="./reports/dead_links_report.json" \
	    --header="Connection: keep-alive" \
	    --header="Pragma: no-cache" \
	    --header="Cache-Control: no-cache" \
	    --header="Upgrade-Insecure-Requests: 1" \
	    --header="Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8" \
	    --header="DNT: 1" \
	    --header="User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36 link-checker-qa" \
	    $(AUTH) \
	    --ignore=`echo $${IGNORED_PREFIXES} | tr -d [:space:]` \
	    $${TEST_URLS}

cms_pages_check:
	echo "Running CMS pages check against: $(DIRECTORY_CMS_API_CLIENT_BASE_URL)" && \
	pytest --capture=no --verbose --junit-xml=./reports/cms_pages.xml cms_pages/


# compare contents of Staging & Dev environments by default
SERVICE ?= invest
ENVS_TO_COMPARE ?= stage_dev

compare_content:
	behave -k -t ~wip --junit --junit-directory=./reports/ content_diff/features/$(SERVICE)_$(ENVS_TO_COMPARE).feature

