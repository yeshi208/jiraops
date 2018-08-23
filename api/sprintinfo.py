#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/22 10:15
# @Author  : Renyue
# @Site    : 
# @File    : sprintinfo.py
# @Software: PyCharm

from api.configuration import configuration as conf
import api.jiragent
import re

# Data structure
# projectsdata:
#     key:project name
#     value:sprintsdata
#         key:id
#         value:sprintdata
#             sprint
#             issuelist
#             delayissuelist
# if sprint is closed
#             alltime
#             front feature size
#             back feature size
#             front debt size
#             back debt size
#             delay front task(feature/debt) size
# if sprint is active
#             alltime
#             front feature size
#             back feature size
#             front debt size
#             back debt size
# if sprint is future
#             alltime
#             front feature size
#             back feature size
#             front debt size
#             back debt size

class SprintData:
    def __init__(self, sprint):
        self.sprint = sprint
        self.issueList = []
        self.allSize = 0
        self.frontFeatureSize = 0
        self.frontDebtSize = 0
        self.backFeatureSize = 0
        self.backDebtSize = 0
        self.delayFrontFeatureSize = 0
        self.delayFrontDebtSize = 0
        self.delayBackFeatureSize = 0
        self.delayBackdebtSize = 0
        self.sprintDelayIssueList = []

class ProjectData:
    def __init__(self, project, sprintsdata):
        self.project = project
        self.sprintsdata = sprintsdata
        self.delayIssueList = []

class SprintInfo:
    def __init__(self):
        self.projectsData = {}
        self.construct_projects_data()

    def __str__(self):
        string = ''
        for name, p in self.projectsData.items():
            string += "Project:"+ name  + '\n'
            string += "    Delay issue count = " + str(len(p.delayIssueList)) + '\n'
            for id, s in p.sprintsdata.items():
                string += "    Sprint:" +  s.sprint.name + '\n'
                string += "        Delay issue count     " + str(len(s.sprintDelayIssueList)) + '\n'
                string += "        All size              " + str(s.allSize) + '\n'
                string += "        FrontDebtSize         " + str(s.frontDebtSize) + '\n'
                string += "        FrontFeatureSize      " + str(s.frontFeatureSize) + '\n'
                string += "        BackDebtSize          " + str(s.backDebtSize) + '\n'
                string += "        BackFeatureSize       " + str(s.backFeatureSize) + '\n'
                string += "        DelayFrontFeatureSize " + str(s.delayFrontFeatureSize) + '\n'
                string += "        DelayFrontDebtSize    " + str(s.delayFrontDebtSize) + '\n'
                string += "        DelayBackFeatureSize  " + str(s.delayBackFeatureSize) + '\n'
                string += "        DelayBackdebtSize     " + str(s.delayBackdebtSize) + '\n'

                validSprints = api.jiragent.JiraProxy().get_valid_sprints(p.project)
                vs = []
                for s1 in validSprints:
                    vs.append(s1.id)
                for issue in s.sprintDelayIssueList:
                    sprint = self.get_feature_sprints(issue, vs)
                    sprint = [p.sprintsdata[int(i)].sprint.name for i in sprint]
                    string += "            Delay Issue:" + issue.__str__()  + " ["+ ":".join(sprint) + "]" + '\n'
                if conf.cleaninfo == 0:
                    for issue in s.issueList:
                        string += "            Issue:" + issue.__str__() + '\n'

            if conf.cleaninfo == 0:
                for issue in p.delayIssueList:
                    string += "    Whole project delay issue:" + issue.__str__() + '\n'
        return string

    def construct_projects_data(self):
        for project in conf.projects:
            sprintsdata = {}
            for sprint in api.jiragent.JiraProxy().get_valid_sprints(project):
                sprintsdata[sprint.id] = SprintData(sprint)
            self.projectsData[project['name']] = ProjectData(project, sprintsdata)

    def gain_issues_for_projects_data(self):
        for name, p in self.projectsData.items():
            self.gain_issues_for_single_project(p)

    # jira.client.ResultList: 'append', 'clear', 'copy', 'count', 'current', 'extend', 'index', 'insert', 'isLast', 'iterable', 'maxResults', 'next', 'pop', 'remove', 'reverse', 'sort', 'startAt', 'total'
    # jira.resources.Issue: 'add_field_value', 'delete', 'expand', 'fields', 'find', 'id', 'key', 'permalink', 'raw', 'self', 'update'
    # fileds: 'aggregateprogress', 'aggregatetimeestimate', 'aggregatetimeoriginalestimate', 'aggregatetimespent', 'assignee', 'components', 'created', 'creator', 'customfield_10000', 'customfield_10001', 'customfield_10002',
    # 'customfield_10004', 'customfield_10005', 'customfield_10006', 'customfield_10010', 'customfield_10200', 'customfield_10400', 'customfield_10401', 'customfield_10402', 'customfield_10403', 'customfield_10404',
    # 'customfield_10405', 'customfield_10406', 'customfield_10407', 'customfield_10408', 'customfield_10409', 'customfield_10500', 'customfield_10501', 'customfield_10502', 'customfield_10700', 'customfield_10705',
    # 'customfield_10710', 'customfield_10711', 'customfield_10713', 'customfield_10714', 'customfield_10715', 'customfield_10717', 'customfield_10721', 'customfield_10723', 'customfield_10724', 'customfield_10800',
    # 'customfield_10900', 'customfield_10902', 'customfield_10903', 'customfield_10904', 'customfield_10908', 'customfield_10913', 'customfield_10915', 'customfield_10916', 'customfield_11000', 'customfield_11001',
    # 'customfield_11002', 'customfield_11109', 'customfield_11110', 'customfield_11111', 'customfield_11112', 'customfield_11113', 'customfield_11114', 'customfield_11115', 'customfield_11203', 'customfield_11205',
    # 'customfield_11300', 'customfield_11301', 'customfield_11302', 'customfield_11303', 'customfield_11304', 'customfield_11305', 'customfield_11306', 'customfield_11307', 'customfield_11500', 'customfield_11600',
    # 'customfield_12002', 'description', 'duedate', 'environment', 'fixVersions', 'issuelinks', 'issuetype', 'labels', 'lastViewed', 'parent', 'priority', 'progress', 'project', 'reporter', 'resolution', 'resolutiondate',
    # 'status', 'subtasks', 'summary', 'timeestimate', 'timeoriginalestimate', 'timespent', 'updated', 'versions', 'votes', 'watches', 'workratio'

    #jira.resources.Status 'delete', 'description', 'find', 'iconUrl', 'id', 'name', 'raw', 'self', 'statusCategory', 'update'
    #jira.resources.Resolution  'delete', 'description', 'find', 'id', 'name', 'raw', 'self', 'update'

    # com.atlassian.greenhopper.service.sprint.Sprint
    def gain_issues_for_single_project(self, p):
        for id, s in p.sprintsdata.items():
            jql = "project = " + p.project['name'] + " AND sprint = " + str(id)
            if conf.debug == '1':
                print('jql:', jql)
            issueList = api.jiragent.JiraProxy().get_all_issues(jql) #jira.client.ResultList which contains jira.resources.Issue
            for issue in issueList:
                if self.is_delayed_issue(issue):
                    if id==1939:
                        print("+++++>", issue, self.get_issue_size(issue))
                    if issue not in self.projectsData[p.project['name']].delayIssueList:
                        self.projectsData[p.project['name']].delayIssueList.append(issue)
                else:
                    self.projectsData[p.project['name']].sprintsdata[id].issueList.append(issue)
                    if id == 1939:
                        print("====>", issue, self.get_issue_size(issue))

    def is_delayed_issue(self, issue):
        return True if len(issue.fields.customfield_10005) > 1 else False

    def is_dropped_issue(self, issue):
        # status id is 6 means 关闭
        # resolution id is 1 means 解决
        # may need custom for different project
        return True if (issue.fields.status.id == 6 and issue.fields.resolution.id != 1) else False

    def get_issue_size(self, issue):
        if not self.is_dropped_issue(issue):
            if issue.fields.timespent is not None:
                return issue.fields.timespent / 3600
            elif issue.fields.timeestimate is not None:
                return issue.fields.timeestimate / 3600
            elif issue.fields.timeoriginalestimate is not None:
                return issue.fields.timeoriginalestimate / 3600
            else:
                if conf.debug == '1':
                    print(issue.key, issue.fields.summary, " has not time")
        return 0

    def is_valid_feature(self, p, issue):
        return self.is_front_debt(p, issue) or self.is_front_feature(p, issue) or self.is_back_debt(p, issue) or self.is_back_feature(p, issue)

    def is_front_feature(self, p, issue):
        assignees = p.project['front'].split(',')
        if (issue.fields.assignee is not None) and (issue.fields.assignee.name in assignees):
            types = p.project['feature'].split(',')
            if (issue.fields.issuetype is not None) and (issue.fields.issuetype.id in types):
                if conf.debug == '1':
                    print('is_front_feature:', issue)
                return True
        return False

    def is_front_debt(self, p, issue):
        assignees = p.project['front'].split(',')
        if (issue.fields.assignee is not None) and (issue.fields.assignee.name in assignees):
            types = p.project['techdebt'].split(',')
            if (issue.fields.issuetype is not None) and (issue.fields.issuetype.id in types):
                if conf.debug == '1':
                    print('is_front_debt:', issue)
                return True
        return False
    def is_back_feature(self, p, issue):
        assignees = p.project['back'].split(',')
        if (issue.fields.assignee is not None) and (issue.fields.assignee.name in assignees):
            types = p.project['feature'].split(',')
            if (issue.fields.issuetype is not None) and (issue.fields.issuetype.id in types):
                if conf.debug == '1':
                    print('is_back_feature:', issue)
                return True
        return False
    def is_back_debt(self, p, issue):
        assignees = p.project['back'].split(',')
        if (issue.fields.assignee is not None) and (issue.fields.assignee.name in assignees):
            types = p.project['techdebt'].split(',')
            if (issue.fields.issuetype is not None) and (issue.fields.issuetype.id in types):
                if conf.debug == '1':
                    print('is_back_debt:', issue)
                return True
        return False

    # 1st step is to calculate all of the size information except delay feature
    def calculate_no_delay_size(self):
        for name, p in self.projectsData.items():
            for id, s in p.sprintsdata.items():
                for issue in s.issueList:
                    size = self.get_issue_size(issue)
                    if self.is_valid_feature(p, issue):
                        s.allSize += size
                    if self.is_front_feature(p, issue):
                        s.frontFeatureSize += size
                    elif self.is_front_debt(p, issue):
                        s.frontDebtSize += size
                    elif self.is_back_feature(p, issue):
                        s.backFeatureSize += size
                    elif self.is_back_debt(p, issue):
                        s.backDebtSize += size
                    else:
                        if conf.debug == '1':
                            print('Invalid feature: ', issue)

    def get_feature_sprints(self, issue, validSprints):
        ids = []
        for sprint in issue.fields.customfield_10005:
            id = re.findall("id=\d+", sprint)[0].split('=')[1]
            if int(id) in validSprints:
                ids.append(id)
        return ids

    #2nd step is to calculate all of the size infomation of delay feature
    def calculate_delay_size(self):
        for name, p in self.projectsData.items():
            validSprints = api.jiragent.JiraProxy().get_valid_sprints(p.project)
            vs = []
            for s in validSprints:
                vs.append(s.id)
            for issue in p.delayIssueList:
                size = self.get_issue_size(issue)
                #print("delay feature", issue, size)
                sprints = self.get_feature_sprints(issue, vs)
                #print(sprints)
                for sprint in sprints:
                    if self.is_valid_feature(p, issue):
                        p.sprintsdata[int(sprint)].allSize += size/len(sprints)
                    if self.is_front_feature(p, issue):
                        p.sprintsdata[int(sprint)].frontFeatureSize += size/len(sprints)
                        p.sprintsdata[int(sprint)].delayFrontFeatureSize += size / len(sprints)
                        p.sprintsdata[int(sprint)].sprintDelayIssueList.append(issue)
                        #print("add front feature", issue)
                    elif self.is_front_debt(p, issue):
                        p.sprintsdata[int(sprint)].frontDebtSize += size/len(sprints)
                        p.sprintsdata[int(sprint)].delayFrontDebtSize += size / len(sprints)
                        p.sprintsdata[int(sprint)].sprintDelayIssueList.append(issue)
                        #print("add front debt", issue)
                    elif self.is_back_feature(p, issue):
                        p.sprintsdata[int(sprint)].backFeatureSize += size/len(sprints)
                        p.sprintsdata[int(sprint)].delayBackFeatureSize += size / len(sprints)
                        p.sprintsdata[int(sprint)].sprintDelayIssueList.append(issue)
                        #print("add back feature", issue)
                    elif self.is_back_debt(p, issue):
                        p.sprintsdata[int(sprint)].backDebtSize += size/len(sprints)
                        p.sprintsdata[int(sprint)].delayBackdebtSize += size / len(sprints)
                        p.sprintsdata[int(sprint)].sprintDelayIssueList.append(issue)
                        #print("add back debt", issue)
                    else:
                        if conf.debug == '1':
                            print('Invalid feature: ', issue)


if __name__ == '__main__':
    pass
else:
    # Singleton mode, we could use the following import statement to import connection
    # from api.sprintinfo import sprintInfo
    sprintInfo = SprintInfo()
