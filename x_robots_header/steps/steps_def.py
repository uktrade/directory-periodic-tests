# -*- coding: utf-8 -*-
from behave import then, when
from behave.runner import Context

from steps.steps_impl import (
    response_should_contain_header,
    response_should_not_contain_header,
    visit_page,
)


@when('you visit "{endpoint}" on "{service}" ({environment})')
def when_you_visit_page(
        context: Context, endpoint: str, service: str, environment: str):
    visit_page(context, service, environment, endpoint)


@then('the response should NOT contain "{header}" header')
def then_response_should_not_contain_header(context: Context, header: str):
    response_should_not_contain_header(context, header)
 

@then('the response should contain "{header}" header')
def then_response_should_contain_header(context: Context, header: str):
    response_should_contain_header(context, header)
 
