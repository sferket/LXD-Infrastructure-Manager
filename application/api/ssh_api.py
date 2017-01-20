# -*- encoding: utf-8 -*-
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from paramiko import util
from paramiko import RSAKey
from application.api.cpu_load_api import GetCpuLoad
util.log_to_file("paramiko_log.log")


class SshApi(object):

    def __init__(self, config):
        self.config = config
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        """
        **TRIED A COUPLE WAYS OF ADDING KEY, NONE WORKED**
        self.key_file = "application/keys/client_eng1-lxd1.key"
        self.client.load_host_keys("application/keys/client_eng1-lxd1.key")
        self.client.load_host_keys("application/keys/client_eng1-lxd2.key")
        try:
            self.client.load_host_keys("application/keys/client_eng1-lxd1.key")
            self.client.set_missing_host_key_policy(self.client.get_host_keys())
        except Exception, e:
            print "e: %s" % e
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        try:
            self.client.load_system_host_keys("application/keys/client_eng1-lxd1.key")
            #self.client.set_missing_host_key_policy(AutoAddPolicy())
            keys = self.client.get_host_keys()
            print "keys.__dict__: %s" % keys.__dict__
        except IOError, e:
            print "e: %s" % e
        except Exception, e:
            print "e: %s" % e
        """

    def execute_ssh_command(self, server, command):
        server_ip = self._get_server_ip(server)
        self.client.connect(
            server_ip,
            username=self.config[server]["username"],
            password=self.config[server]["password"],
        )
        print "execute_ssh_command"
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdin, stdout, stderr

    def _get_server_ip(self, server):
        server_ip = self.config[server]["endpoint"].split(":")[1]
        server_ip = server_ip.replace("//","")
        return server_ip

    def get_server_info(self, server):
        return {}, {}, {}, {}
        data_paths = {
            "meminfo": "cat /proc/meminfo",
            "stat": "cat /proc/stat",
            "uptime": "cat /proc/uptime",
            "misc": "cat /proc/misc",
        }
        data = {}
        for k,v in data_paths.iteritems():
            stdin, stdout, stderr = self.execute_ssh_command(server, v)
            data[k] = stdout.readlines()

        meminfo_dict = {}
        for i in data["meminfo"]:
            i = i.replace("\n","")
            i_array = i.split(":")
            meminfo_dict[i_array[0]] = i_array[1]

        misc_dict = {}
        for i in data["misc"]:
            i = i.replace("\n", "")
            i_array = i.split(" ")
            misc_dict[i_array[-1]] = i_array[-2]

        return meminfo_dict, misc_dict, {}, {}

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
