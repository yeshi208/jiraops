#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/7 16:16
# @Author  : Renyue
# @Site    : 
# @File    : main.py
# @Software: PyCharm

from api.connection import connection as con
from api.configuration import configuration as conf
from api.sprintinfo import sprintInfo
import api.jiragent

if __name__ == '__main__':
    sprintInfo.gain_issues_for_projects_data()
    sprintInfo.calculate_no_delay_size()
    sprintInfo.calculate_delay_size()
    print(sprintInfo)



