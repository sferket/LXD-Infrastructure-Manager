# -*- encoding: utf-8 -*-
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from paramiko import util
from paramiko import RSAKey
from application.api.cpu_load_api import GetCpuLoad
from application.helpers import convert_size
util.log_to_file("paramiko_log.log")


class SshApi(object):

    def __init__(self, config):
        print 'init ssh'
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
        #print "execute_ssh_command"
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdin, stdout, stderr

    def _get_server_ip(self, server):
        server_ip = self.config[server]["endpoint"].split(":")[1]
        server_ip = server_ip.replace("//","")
        return server_ip

    def get_server_info(self, server):
        #return {}, {}, {}, {}
        print 123
        data_paths = {
#             "meminfo": "cat /proc/meminfo",
#             "stat": "cat /proc/stat",
#             "uptime": "cat /proc/uptime",
#             "misc": "cat /proc/misc",
            "uptime" : "uptime",
            "lsb_release" : "lsb_release -a | grep Description",
            "meminfo": "cat /proc/meminfo",
            "iostat": "iostat -c 1 3 | sed -e 's/,/./g' | tr -s ' ' ';' | sed '/^$/d' | tail -1"
        }
        data = {}
        cdata = {}
        for k,v in data_paths.iteritems():
            stdin, stdout, stderr = self.execute_ssh_command(server, v)
            data[k] = stdout.readlines()

        print  data.get('uptime')[0]
        sp = data.get('uptime')[0].split('load average:')
        print 1
        print sp
        print 2
        cdata.update({'uptime' : sp[0].split('up')[1].split(',')[0].strip()})
        print cdata
        avg=sp[1].split(', ')
        cdata.update({'avg1' : avg[0].strip()})
        cdata.update({'avg5' : avg[1].strip()})
        cdata.update({'avg15' : avg[2].strip()})
        
        
        print cdata
        cdata.update({'lsb_release' : data.get('lsb_release')[0].split(':')[1].strip('\t').strip('\n')})
        
        
        for p in data.get('meminfo'):
            n = p.split(':')[0].strip()
            v = p.split(':')[1].strip()
            if n in ['MemTotal','MemFree','MemAvailable','SwapTotal', 'SwapFree']:              
                cdata.update({n : convert_size(1024*int(v.split(' ')[0]))})
                
        print cdata
        print 
        
        ios = data.get('iostat')[0].split(';')
        cdata.update({'iowait' : ios[5]})
        cdata.update({'cpu' : str(int(100-float(ios[6])))})
        
        print cdata
# tmp = '12:56:45 up  4:25,  1 user,  load average: 0,75, 0,58, 0,54'
# 
# sp = tmp.split('load average:')
# uptime = sp[0].split('up')[1].split(',')[0].strip()
# print uptime
# avg=sp[1].split(', ')
# print avg
# avg1 = avg[0].strip()
# avg5 = avg[1].strip()
# avg15 = avg[2].strip()
# 
# print avg1
# print avg5
# print avg15        
#         meminfo_dict = {}
#         for i in data["meminfo"]:
#             i = i.replace("\n","")
#             i_array = i.split(":")
#             meminfo_dict[i_array[0]] = i_array[1]
# 
#         misc_dict = {}
#         for i in data["misc"]:
#             i = i.replace("\n", "")
#             i_array = i.split(" ")
#             misc_dict[i_array[-1]] = i_array[-2]

#        -misc (uptime, kernel, ubuntu version)
#        -cpu (total cpu's , ht?), average overall usgae 1-minute, 5-minute and 15-minute
#        -mem total, used (+swap)
#        disk io
        
        return cdata

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
