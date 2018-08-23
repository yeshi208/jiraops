#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/21 11:58
# @Author  : Renyue
# @Site    : 
# @File    : configuration.py
# @Software: PyCharm

import configparser

class Configuration:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("configuration.ini", encoding="utf-8-sig")

        # get GLOBAL information
        self.debug = self.config['GLOBAL']['debug']
        self.maxqueryresult = self.config['GLOBAL']['maxqueryresult']
        self.cleaninfo = self.config['GLOBAL']['cleaninfo']

        # get SERVER information
        self.url = self.config['SERVER']['url']
        self.username = self.config['SERVER']['username']
        self.password = self.config['SERVER']['password']

        # get PROJECT information
        projectsNameList = self.config['PROJECTS']['namelist']
        self.projects = []
        for name in projectsNameList.split(','):
            project = {}
            project['name'] = name
            project['startsprint'] = self.config[name]['startsprint']
            project['sm'] = self.config[name]['sm']
            project['front'] = self.config[name]['front']
            project['back'] = self.config[name]['back']
            project['techdebt'] = self.config[name]['techdebt']
            project['feature'] = self.config[name]['feature']
            project['po'] = self.config[name]['po']
            project['qc'] = self.config[name]['qc']
            project['boardid'] = self.config[name]['boardid']
            project['sprintheader'] = self.config[name]['sprintheader']
            self.projects.append(project)

if __name__ == '__main__':
    pass
else:
    # Singleton mode, we could use the following import statement to import configuration
    # from api.configuration import configuration
    configuration = Configuration()