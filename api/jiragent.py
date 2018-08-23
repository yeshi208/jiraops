#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/21 18:59
# @Author  : Renyue
# @Site    : 
# @File    : jiragent.py
# @Software: PyCharm
from api.connection import connection as con
from api.configuration import configuration as conf
import operator

# do some filter and sorted work
def filter_sprint_info(sprints, project):
    filter_sprints = {}
    cut_sprints = {}
    for sprint in sprints:
        if sprint.name.startswith(project['sprintheader']):
            filter_sprints[sprint.id] = sprint
        sorted_sprints = sorted(filter_sprints.items(), key=operator.itemgetter(0))  # sort by key
        for key, value in sorted_sprints:
            if key >= int(project['startsprint']):  # start sprints
                cut_sprints[key] = value
    return (list(cut_sprints.values()))

class JiraProxy:
    def __init__(self):
        pass

    def get_valid_sprints(self, project):
        sprints = con.jira.sprints(project['boardid'])
        sorted_sprints = filter_sprint_info(sprints, project)
        return sorted_sprints

    def get_all_issues(self, jql):
        return con.jira.search_issues(jql, maxResults=int(conf.maxqueryresult))
