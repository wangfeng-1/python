#!/usr/bin/python3.6
# Author:       wangfeng
# Mail:
from pyzabbix import ZabbixAPI
import sys
from re import compile,IGNORECASE
ZABBIX_SERVER = ""
USER = ""
PASSWORD = ""
HOSTNAME = ""
URL=""
def login(ZABBIX_SERVER,USER,PASSWORD):
  zapi = ZabbixAPI(ZABBIX_SERVER)
  zapi.login(USER,PASSWORD)
  return zapi
def gethostid(auth,HOSTNAME):
  request = ZabbixAPI.do_request(auth, 'host.get', params={ "filter": {"host":HOSTNAME}})
  if request['result']:
    return request['result'][0]['hostid']
  else:
    print ("找不到该主机")
    sys.exit(1)
def getapplicationid(auth,hostid):
  try:
    request = ZabbixAPI.do_request(auth, 'application.create', params={"name": "web监控","hostid": hostid})
  except Exception as e:
    print(e)
  request = ZabbixAPI.do_request(auth, 'application.get', params={"hostids": hostid})
  for num in range(0,len (request['result'])):
    if request['result'][num]['name'] == "web监控":
      return request['result'][num]['applicationid']
def create_web_scenario(auth,URL,hostid,applicationid):
  request = ZabbixAPI.do_request(auth, 'httptest.get', params={ "filter": {"name": URL}})
  if request['result']:
    print('该web监控已经添加过了' )
  else:
    try:
      ZabbixAPI.do_request(auth, 'httptest.create',params={"name": URL,"hostid": hostid,"applicationid": applicationid, "delay": '60',"retries": '3', "steps": [ { 'name': URL, 'url': URL, 'no': '1'} ] } )
    except Exception as e:
      print(e)
def create_trigger(auth,HOSTNAME,URL):
  expression="{"+"{0}:web.test.fail[{1}].last()".format(HOSTNAME,URL)+"}"+"<>0"
  try:
    ZabbixAPI.do_request(auth, 'trigger.create', params={"description": "从监控机（172.18.11.34）访问{0}出现问题,如果网络和主机性能没问题，并且是单节点报错请尝试重启对应的tomcat".format(URL),"expression": expression,"priority":5})
  except Exception as e:
    print(e)

auth = login(ZABBIX_SERVER,USER,PASSWORD)
hostid = gethostid(auth,HOSTNAME)
applicationid=getapplicationid(auth,hostid)
create_web_scenario(auth,URL,hostid,applicationid)
create_trigger(auth,HOSTNAME,URL)