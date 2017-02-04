# -*- encoding: utf-8 -*-
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from paramiko import util
from paramiko import RSAKey
from application.helpers import convert_size
import time
import threading

util.log_to_file("paramiko_log.log")

class Server(threading.Thread):
    name = None
    config = None
    session = None
    info = {} 

    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.session = self._open_ssh()
        threading.Thread.__init__(self)

    def run(self):
        while True:
            self.refresh()
            time.sleep(5)

    def _get_server_ip(self):
        server_ip = self.config["endpoint"].split(":")[1]
        server_ip = server_ip.replace("//","")
        return server_ip

    def _open_ssh(self):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        
        server_ip = self._get_server_ip()
        client.connect(
            server_ip,
            username=self.config["username"],
            password=self.config["password"],
        )
        return client
    
    def execute_ssh_command(self, command):
        client = self.session
        
        stdin, stdout, stderr = self.session.exec_command(command)
        return stdin, stdout, stderr    
    
    def refresh(self):
        data_paths = {
            "uptime" : "uptime",
            "lsb_release" : "lsb_release -a | grep Description",
            "meminfo": "cat /proc/meminfo",
            "iostat": "iostat -c 1 3 | sed -e 's/,/./g' | tr -s ' ' ';' | sed '/^$/d' | tail -1"
        }
        data = {}
        cdata = {}
        for k,v in data_paths.iteritems():
            stdin, stdout, stderr = self.execute_ssh_command(v)
            data[k] = stdout.readlines()

        sp = data.get('uptime')[0].split('load average:')
        cdata.update({'uptime' : sp[0].split('up')[1].split(',')[0].strip()})
        avg=sp[1].split(', ')
        cdata.update({'avg1' : avg[0].strip()})
        cdata.update({'avg5' : avg[1].strip()})
        cdata.update({'avg15' : avg[2].strip()})
        cdata.update({'lsb_release' : data.get('lsb_release')[0].split(':')[1].strip('\t').strip('\n')})
        
        for p in data.get('meminfo'):
            n = p.split(':')[0].strip()
            v = p.split(':')[1].strip()
            if n in ['MemTotal','MemFree','MemAvailable','SwapTotal', 'SwapFree']:              
                cdata.update({n : convert_size(1024*int(v.split(' ')[0]))})
        
        ios = data.get('iostat')[0].split(';')
        cdata.update({'iowait' : ios[5]})
        cdata.update({'cpu' : str(int(100-float(ios[6])))})
        
        self.info = cdata
            
    def get_info(self, attr=None, val_if_null=None):
        if attr:
            return self.info.get(attr, val_if_null)
        else:
            return self.info 
    
    
class Servers(object):
    config = None
    servers = {}
     
    def __init__(self, config):
        self.config = config
        for s in config:
            svr = Server(s, config.get(s))
            svr.start()
            self.servers.update({ s : svr })
        
    def get(self, server=None):
        if server:
            return self.servers.get(server)
        else:
            return self.servers    
        
    def get_display_info(self):
        d = {}
        for s in self.servers:
            d.update({s:{'servername' : self.servers.get(s).name } })
        return d
