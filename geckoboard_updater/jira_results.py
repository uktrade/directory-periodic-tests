# -*- coding: utf-8 -*-
from jira_helpers import (
    jira_links,
    label_counters,
    tickets_by_labels,
    tickets_per_service,
    total_tickets,
    unlabelled_tickets,
)
from jira_queries import *

content_bugs_manual_vs_automated = label_counters(
    jql=ContentJQLs.BUGS_MANUAL_VS_AUTOMATED, look_for=["auto", "manual"]
)
content_bugs_closed_today = total_tickets(
    jql=ContentJQLs.BUGS_CLOSED_TODAY
)
content_bugs_in_backlog_by_labels = tickets_by_labels(
    jql=ContentJQLs.BUGS_IN_BACKLOG, ignored_labels=["auto", "manual"]
)
content_bugs_on_board_by_labels = tickets_by_labels(
    jql=ContentJQLs.BUGS_ON_BOARD, ignored_labels=["auto", "manual"]
)
content_unlabelled_bugs_on_board = unlabelled_tickets(
    jql=ContentJQLs.BUGS_ON_BOARD
)
content_unlabelled_bugs_in_backlog = unlabelled_tickets(
    jql=ContentJQLs.BUGS_IN_BACKLOG
)
content_bugs_in_backlog = total_tickets(
    jql=ContentJQLs.BUGS_IN_BACKLOG
)
content_scenarios_to_automate = total_tickets(
    jql=ContentJQLs.SCENARIOS_TO_AUTOMATE
)
content_tickets_closed_today = total_tickets(
    jql=ContentJQLs.TICKETS_CLOSED_TODAY
)
content_bugs_per_service = tickets_per_service(
    jql=ContentJQLs.BUGS_PER_SERVICE, look_for=SERVICE_TAGS
)
content_tickets_on_board = total_tickets(
    jql=ContentJQLs.TICKETS_ON_BOARD
)
content_jira_links = jira_links(ContentJQLs)


tools_bugs_manual_vs_automated = label_counters(
    jql=ToolsJQLs.BUGS_MANUAL_VS_AUTOMATED, look_for=["auto", "manual"]
)
tools_bugs_closed_today = total_tickets(
    jql=ToolsJQLs.BUGS_CLOSED_TODAY
)
tools_bugs_in_backlog_by_labels = tickets_by_labels(
    jql=ToolsJQLs.BUGS_IN_BACKLOG, ignored_labels=["auto", "manual"]
)
tools_bugs_in_backlog = total_tickets(
    jql=ToolsJQLs.BUGS_IN_BACKLOG
)
tools_bugs_on_board_by_labels = tickets_by_labels(
    jql=ToolsJQLs.BUGS_ON_BOARD, ignored_labels=["auto", "manual"]
)
tools_unlabelled_bugs_on_board = unlabelled_tickets(
    jql=ToolsJQLs.BUGS_ON_BOARD
)
tools_unlabelled_bugs_in_backlog = unlabelled_tickets(
    jql=ToolsJQLs.BUGS_IN_BACKLOG
)
tools_scenarios_to_automate = total_tickets(
    jql=ToolsJQLs.SCENARIOS_TO_AUTOMATE
)
tools_tickets_closed_today = total_tickets(
    jql=ToolsJQLs.TICKETS_CLOSED_TODAY
)
tools_bugs_per_service = tickets_per_service(
    jql=ToolsJQLs.BUGS_PER_SERVICE, look_for=SERVICE_TAGS
)
tools_tickets_on_board = total_tickets(
    jql=ToolsJQLs.TICKETS_ON_BOARD
)
tools_jira_links = jira_links(ToolsJQLs)
