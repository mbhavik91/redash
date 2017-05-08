import json
import logging
import requests
import os
from jira import JIRA

from redash.destinations import *

class Jira(BaseDestination):

    @classmethod
    def configuration_schema(cls):
        return {
            'type': 'object',
            'properties': {
                'project_name': {
                    'type': 'string',
                    'title': 'Project Name'
                },
                'summary': {
                    'type': 'string',
                    'title': 'Summary'
                },
                'description': {
                    'type': 'string',
                    'title': 'Description'
                },
                'priority': {
                    'type': 'string',
                    'title': 'Priority'
                },
                'assignee': {
                    'type': 'string',
                    'title': 'Assignee'
                },
                'username': {
                    'type': 'string',
                    'title': 'JIRA Username'
                },
                'password': {
                    'type': 'string',
                    'title': 'JIRA Password'
                },
                'server_url': {
                    'type': 'string',
                    'title': 'JIRA Server URL'
                }              
            }
        }

    @classmethod
    def icon(cls):
        return 'fa-jira'

    def notify(self, alert, query, user, new_state, app, host, options):
            
        try:
            if options.get('project_name'): project = options.get('project_name')
            if options.get('summary'): summary = options.get('summary')
            if options.get('description'): description = options.get('description')
            if options.get('priority'): priority = options.get('priority')
            if options.get('assignee'): assignee = options.get('assignee')
            if options.get('username'): username = options.get('username')
            if options.get('password'): password = options.get('password')
            if options.get('server_url'): server_url = options.get('server_url')
        except Exception:
            logging.exception("Failed to get the inputs {0},{1},{2},{3},{4}".format(project,summary,description,priority,assignee))
            
        try:
            authed_jira = JIRA(server_url, basic_auth=(username, password))
            create_issue = authed_jira.create_issue(project=project, summary=summary,description=description, issuetype={'name': 'Bug'},assignee={'name':assignee}, priority={'name':priority})
            logging.error('JIRA created {0}'.format(create_issue))
        except Exception:
            logging.exception("JIRA create ERROR.")

register(Jira)
