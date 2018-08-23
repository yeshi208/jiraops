#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/21 14:59
# @Author  : Renyue
# @Site    : 
# @File    : qulitycheck.py
# @Software: PyCharm

from api.connection import connection as con
from api.configuration import configuration as conf
class QulityCheck:
    def __init__(self):
        pass

    def do_health_check_on_all_projects(self):
        for project in conf.projects:
            self.is_project_health(project)

    def is_project_health(self, project, sprint):
        searchString = "project=" + project['name'] + " AND " + project['qc'] + " AND sprint=" + sprint
        print(searchString)
        issues_in_proj = con.jira.search_issues(searchString)
        if issues_in_proj is not None:
            print("the project has some problem")

            for issue in issues_in_proj:
                print(dir(issue), dir(issue.fields))
                print(issue.key, issue.fields.assignee, issue.fields.summary)
            return False
        return True
if __name__ == '__main__':
    qc = QulityCheck()
    qc.do_health_check_on_all_projects()