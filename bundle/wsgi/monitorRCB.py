#   Copyright (c) 2013-2015, University of Bern, Switzerland.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.



"""
Monitor for RCB.
Version 1.0
"""

from zabbix_api import ZabbixAPI
import time
import traceback
import sys

MAAS_UID = 'admin'
MAAS_PWD = 'zabbix'

RCB_CPU = 0
RCB_LOAD = 1
RCB_TOTAL_MEMORY = 2
RCB_AVAILABLE_MEMORY = 3
class RCBaaSMonitor(object):

    def __init__(self, maas_endpoint):
        """
        Initialize the RCBaaS Monitor object
        """
        # Connect to MaaS
        if maas_endpoint is None:
            self.maas_endpoint = '160.85.4.27'
        else:
            self.maas_endpoint = maas_endpoint
        self.server = 'http://' + self.maas_endpoint + '/zabbix'
        self.username = MAAS_UID
        self.password = MAAS_PWD
        self.connFailed = False
        self.metrics = [RCB_CPU, RCB_LOAD, RCB_TOTAL_MEMORY, RCB_AVAILABLE_MEMORY]

        # Zabbix API
        self.zapi = ZabbixAPI(server=self.server)
        for i in range(1,4):
            try:
                print('*** Connecting to MaaS')
                self.zapi.login(self.username, self.password)
                print('*** Connected to MaaS')
                self.connFailed = False
            except Exception as e:
                #print('*** Caught exception: %s: %s' % (e.__class__, e))
                #traceback.print_exc()
                print('*** Connection to MaaS has failed! Retrying ('+str(i)+').')
                self.connFailed = True
            time.sleep(3)
        if self.connFailed:
            print('*** Connection to MaaS has failed! Waiting for an update to try again.')
        self.__metrics = []

    def get(self, host_name):
        measured_values = {}
        for metric in self.metrics:
            measured_values[metric] = self.get_value(metric, host_name)
            if measured_values[metric] is None:
                return
        return measured_values

    def get_value(self, metric, host_name):
        item=""

        if metric == RCB_CPU:
            item = "system.cpu.util[,idle]"

        if metric == RCB_LOAD:
            item = "system.cpu.load[percpu,avg1]"

        if metric == RCB_TOTAL_MEMORY:
            item = "vm.memory.size[total]"

        if metric == RCB_AVAILABLE_MEMORY:
            item = "vm.memory.size[available]"

        try:
            hostid = self.zapi.host.get({"filter":{"host":host_name}})[0]["hostid"]
        except:
            print "WARNING: Host " + host + " not found"
            return

        try:
            value = self.zapi.item.get({"output":"extend","hostids":hostid,"filter":{"key_":item}})[0]["lastvalue"]
            return float(value)
        except Exception as e:
            print "ERROR: User metric not found"
            traceback.print_exc()
