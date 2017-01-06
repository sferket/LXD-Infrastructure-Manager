# -*- encoding: utf-8 -*-
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from application.api.cpu_load_api import GetCpuLoad


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
