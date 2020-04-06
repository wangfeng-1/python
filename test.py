#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:wangfeng

import requests
import re
import json


class Zabbix:

    def __init__(self, url, header, username, password):
        self.url = url
        self.header = header
        self.username = username
        self.password = password

    def getToken(self):
        # 获取Token并返回字符Token字符串
        data = {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {"user": self.username,"password": self.password},
                "id": 1,
                "auth": None
                }
        token = requests.post(url=self.url, headers=self.header, data=json.dumps(data))
        return json.loads(token.content)["result"]
    def getAllHost(self):
        # 获取所有主机信息

        data = {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": ["hostid",
                               "host"],
                    # "selectGroups": "extend",
                    # "selectInterfaces": ["interfaceid","ip"]
                },
                "id": 2,
                "auth": self.getToken()
                }
        hosts = requests.post(url=self.url, headers=self.header, data=json.dumps(data))
        return json.loads(hosts.content)["result"]


if __name__ == "__main__":
    header = {"Content-Type": "application/json-rpc"}
    url = "http://47.103.0.139:8080/api_jsonrpc.php"
    test = Zabbix(url=url, header=header, username="admin", password="rpjPxN7hM")
    for i  in test.getAllHost():
        print(i["host"])
