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
from paramiko import SSHClient, AutoAddPolicy
from cpu_load_api import *


class SshApi(object):

    def __init__(self, config):
        self.config = config
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())


    def _execute_ssh_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.readlines()

    def _get_server_ip(self, server):
        server_ip = self.config[server]["endpoint"].split(":")[1]
        server_ip = server_ip.replace("//","")
        return server_ip

    def get_server_info(self, server):
        server_ip = self._get_server_ip(server)
        self.client.connect(
            server_ip,
            username=self.config[server]["username"],
            password=self.config[server]["password"]
        )
        meminfo = self._execute_ssh_command("cat /proc/meminfo")
        stat = self._execute_ssh_command("cat /proc/stat")
        uptime = self._execute_ssh_command("cat /proc/uptime")
        misc = self._execute_ssh_command("cat /proc/misc")
        self.client.close()

        meminfo_dict = {}
        for i in meminfo:
            i = i.replace("\n","")
            i_array = i.split(":")
            meminfo_dict[i_array[0]] = i_array[1]

        misc_dict = {}
        for i in misc:
            i = i.replace("\n", "")
            i_array = i.split(" ")
            misc_dict[i_array[-1]] = i_array[-2]

        return meminfo_dict, misc_dict, stat, uptime

    def get_cpu_info(server):
        server_ip = self._get_server_ip(server)
        username = self.config[server]["username"]
        password = self.config[server]["password"]
        cpu_parser = GetCpuLoad(
            server_ip=server_ip,
            username=username,
            password=password
        )
        data = cpu_parser.getcpuload()
        return data
