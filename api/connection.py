#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/7 15:54
# @Author  : Renyue
# @Site    : 
# @File    : connection.py
# @Software: PyCharm

from jira import JIRA
from api.configuration import configuration as con

class Connection:
    def __init__(self, url=con.url, username=con.username, password=con.password):
        self.username = username
        self.password = password
        self.url = url
        self.jira = None
        self.connect()

    def connect(self):
        if self.jira is None:
            try:
                self.jira = JIRA(self.url, basic_auth=(self.username, self.password))
            except Exception as e:
                print(e)

if __name__ == '__main__':
    pass
else:
    # Singleton mode, we could use the following import statement to import connection
    # from api.connection import connection
    connection = Connection()
