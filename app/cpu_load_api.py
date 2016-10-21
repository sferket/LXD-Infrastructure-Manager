# -*- encoding: utf-8 -*-
##############################################################################
#    Copyright (c) 2016 - Open2bizz
#    Author: Open2bizz
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of the GNU General Public License is available at:
#    <http://www.gnu.org/licenses/gpl.html>.
#
##############################################################################
from time import sleep
import sys
from paramiko import SSHClient, AutoAddPolicy


class GetCpuLoad(object):

    def __init__(self, percentage=True,sleeptime=1, server_ip=None,
        username=None, password=None):
        self.percentage = percentage
        self.sep = ' '
        self.sleeptime = sleeptime
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(server_ip, username=username, password=password)

    def update_cpu_stats(self):
        stdin,stdout,stderr = self.client.exec_command("cat /proc/stat")
        self.stats = stdout.readlines()

    def get_cpu_time(self):
        self.update_cpu_stats()
        cpu_infos = {} #collect here the information
        lines = [line.split(self.sep) for content in self.stats for line in content.split('\n') if line.startswith('cpu')]
        #compute for every cpu
        for cpu_line in lines:
            if '' in cpu_line: cpu_line.remove('')#remove empty elements
            cpu_line = [cpu_line[0]]+[float(i) for i in cpu_line[1:]]#type casting
            cpu_id,user,nice,system,idle,iowait,irq,softrig,steal,guest,guest_nice = cpu_line
            Idle=idle+iowait
            NonIdle=user+nice+system+irq+softrig+steal

            Total=Idle+NonIdle
            #update dictionionary
            cpu_infos.update({cpu_id:{'total':Total,'idle':Idle}})
        return cpu_infos

    def get_cpu_load(self):
        start = self.get_cpu_time()
        #wait a second
        sleep(self.sleeptime)
        stop = self.get_cpu_time()

        cpu_load = {}

        for cpu in start:
            Total = stop[cpu]['total']
            PrevTotal = start[cpu]['total']
            Idle = stop[cpu]['idle']
            PrevIdle = start[cpu]['idle']

            CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)*100
            cpu_load.update({cpu: CPU_Percentage})

        return cpu_load
