# -*- encoding: utf-8 -*-
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from paramiko import util
from paramiko import RSAKey
from application.helpers import convert_size
import time
import threading
import re
from pylxd import client
from ws4py.client import WebSocketBaseClient
import json
from datetime import datetime

util.log_to_file("paramiko_log.log")

#tmp = 'Hi hi'

class _WebsocketClient(WebSocketBaseClient):
    """A basic websocket client for the LXD API.

    This client is intentionally barebones, and serves
    as a simple default. It simply connects and saves
    all json messages to a messages attribute, which can
    then be read are parsed.
    """
    #clientupdaterequest = threading.Event()
    
    def __init__(self, url, protocols=None, extensions=None, heartbeat_freq=None,
                 ssl_options=None, headers=None, svr=None):
        WebSocketBaseClient.__init__(self, url, protocols, extensions, heartbeat_freq,
                                     ssl_options, headers=headers)
        self._th = threading.Thread(target=self.run, name='WebSocketClient')
        self._th.daemon = True
        self.server = svr

#     def setUpdateReq(self, clientupdaterequest):
#         self.clientupdaterequest = clientupdaterequest
        
    def setServer(self, server):
        self.server = server    

    @property
    def daemon(self):
        """
        `True` if the client's thread is set to be a daemon thread.
        """
        return self._th.daemon

    @daemon.setter
    def daemon(self, flag):
        """
        Set to `True` if the client's thread should be a daemon.
        """
        self._th.daemon = flag

    def getmes(self):
        return self.mes
    
    def handshake_ok(self):
        self._th.start()

    def received_message(self, message):
        False
#         mes = json.loads(message.data.decode('utf-8'))
#         #print mes
#         timestamp = mes.get("timestamp")
#         type = mes.get("type")
#         type = mes.get("type")
#         level = ""
#         method = ""
#         url = ""
#         message = ""
#         
#         metadata = mes.get("metadata", {}) 
#         if metadata.has_key("context"):
#             method = metadata.get("context").get("method", "")
#             url = metadata.get("context").get("url", "")
#             
#         if metadata.has_key("level"):
#             level = metadata.get("level", "")
#         if metadata.has_key("message"):
#             message = metadata.get("message", "")
# 
#         if type == 'operation' and metadata.get('class') == 'task' and metadata.get('status') == 'Success':              
#             self.server.refresh_container_info()

class ContainerInfo(object):

    def __init__(self, ws_client, container_name):
        self.resp = self._get_container_info(ws_client, container_name)
        self._parse_container_info()

    def _get_container_info(self, client, name):
        container = client.api.containers["%s/state" % name]
        res = container.get().json()
        return res

    def _parse_container_info(self):
        ip = ''
        for k, v in self.resp.get('metadata',{}).iteritems():
            
            if k == 'network':
                if v:
                    eth = v.get("eth0")
                    if eth:
                        for adr in eth["addresses"]:
                            if adr.get("family") == "inet":
                                ip = adr["address"]   
                    v = ip
            if k == 'memory':
                for k1 in v:
                    v.update({k1:convert_size(v.get(k1))})
                
            setattr(self, k, v if v else 'NA')


class Server(threading.Thread):
    name = None
    config = None
    session = None
    info = {} 
    ws_client = None
    ev_client = None
    clientupdaterequest = None
    containers = {}
    containers_cpudata = {}

    def __init__(self, name, config, clientupdaterequest):
        #tmp = "Yestt htis is it"
        print "2.1"
        self.name = name
        self.config = config
        print "2.2"
        self.clientupdaterequest = clientupdaterequest
        print "2.3"
        self.session = self._open_ssh()
        print "2.4"
        cert = (self.config.get("certfile"), self.config.get("keyfile"))
        print "2.5"
        ssl_options = {"keyfile": self.config.get("keyfile"),"certfile": self.config.get("certfile")}
        print "2.6"
        self.ws_client = client.Client(
            endpoint=self.config.get("endpoint"),
            cert=cert,
            verify=False
        )
        print "2.7"
        
        
        self.ev_client = self.ws_client.events(_WebsocketClient)
        print "2.8"
        #self.ev_client.setUpdateReq(clientupdaterequest)
        self.ev_client.setServer(self)
        print "2.9"
        self.ev_client.ssl_options=ssl_options
        print "2.10"
        self.ev_client.connect()
        print "2.11"
        self.refresh()
        print "2.12"
        self.refresh_container_info()
        print "2.13"

        threading.Thread.__init__(self)
        print "2.14"

    def run(self):
        while True:
            self.refresh()
            time.sleep(60)

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
        def get_zpool_list(val):
            val = [x for x in val.split('\n') if x]
            header = [x for x in val[0].split(' ') if x]  
            pools =[]
            for pool in val[1:]:
                pool = [x for x in pool.split(' ') if x]
                cnt = 0
                pl = {}
                for h in header:
                    pl.update({h : pool[cnt]})
                    cnt += 1
                pools += [pl]
            
            return pools
        
            
            
        def get_zpool_status(val):
            pools = {}
            for pool in val.strip().split('pool:'):
                if len(pool.split('state:')) > 1:
                    pools.update({ pool.split('state:')[0].strip() : pool.split('state:')[1] })
            
            return pools
        
        def parse_zpool_info(info):
            dt = info.split('<zpool list>')[0].strip('\n')
            pools = get_zpool_list(info.split('<zpool list>')[1].split('<zpool status>')[0])
            stats = get_zpool_status(info.split('<zpool list>')[1].split('<zpool status>')[1])
            
            for pool in pools:
                pool.update({ 'STATS' : stats.get(pool.get('NAME')) })
        
            return dt, pools

# */10 * * * * { echo `date +"%F%H:%M:%S.%N"` && echo "<zpool list>" && zpool list && echo "<zpool status>" && zpool status; } > /tmp/zpool.stats
        
# TO DO::: Only root can run these commands, so on server cron spool to /tmp .....
# root@eng-lxd1:/home/openadmin# zpool status
#   pool: lxd
#  state: ONLINE
#   scan: scrub repaired 0 in 0h1m with 0 errors on Sun Jan  8 00:25:39 2017
# config:
# 
#     NAME        STATE     READ WRITE CKSUM
#     lxd         ONLINE       0     0     0
#       mirror-0  ONLINE       0     0     0
#         sda     ONLINE       0     0     0
#         sdb     ONLINE       0     0     0
#     logs
#       sdc       ONLINE       0     0     0
#     cache
#       sdd       ONLINE       0     0     0
# 
# errors: No known data errors
        
        
        
        
        data_paths = {
            "uptime" : "uptime",
            "lsb_release" : "lsb_release -a | grep Description",
            "meminfo": "cat /proc/meminfo",
            "iostat": "iostat -c 1 3 | sed -e 's/,/./g' | tr -s ' ' ';' | sed '/^$/d' | tail -1",
            "df": "df -hx devtmpfs -x tmpfs",
            "zpool" : "cat /tmp/zpool.stats"
        }
        data = {}
        cdata = {'servername' : self.name}
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
        
        #print data.get('iostat')
        ios = data.get('iostat')[0].split(';')
        cdata.update({'iowait' : ios[5]})
        cdata.update({'cpu' : str(int(100-float(ios[6])))})
        
        disks = []
        for d in data.get('df')[1:]:
            dst = re.sub( '\s+', ' ', d ).strip().split(' ')
            ds = {}
            ds.update({'Filesystem' : dst[0]})
            ds.update({'Size' : dst[1]})
            ds.update({'Used' : dst[2]})
            ds.update({'Avail' : dst[3]})
            ds.update({'Use' : dst[4]})
            ds.update({'MountedOn' : dst[5]})
            disks += [ds]
        
        cdata.update({'disks' : disks})
        
#         if (len(data.get('zpool')) > 0):
#             print '------------------zpool'
#             print data.get('zpool')
#             cdata.update({'zpoolupdate' : parse_zpool_info(''.join(data.get('zpool')))[0]})
#             cdata.update({'zpool' : parse_zpool_info(''.join(data.get('zpool')))[1]})
            
            
               
        
        
        self.info = cdata
        
        #self.refresh_container_stats()
        self.clientupdaterequest.set()
            
    def get_info(self, attr=None, val_if_null=None):
        if attr:
            return self.info.get(attr, val_if_null)
        else:
            return self.info 

    def get_containers(self):
        return self.containers
    
    def refresh_container_stats(self):
        def convert_cpu_data(cpu_data):
            ret_data = {}
            for i in cpu_data:
                if i.find(' ') > 0:
                    k,v = i.split(' ')
                    ret_data.update({k:v})
            ret_data.update({'date' : datetime.strptime(ret_data.get('date')[0:25], '%Y-%m-%d%H:%M:%S.%f') })
            return ret_data
        
        # Intentionally separated from refresh_container_info because this takes less resources and can be called more often
        for cont in self.containers:
            if cont.get('status') == 'Running':
                c = "echo CLK_TCK `getconf CLK_TCK` && echo date `date +\"%F%H:%M:%S.%N\"` && cat /sys/fs/cgroup/cpu/lxc/" + cont.get('name') + "/cpuacct.stat" 
                stdin, stdout, stderr = self.execute_ssh_command(c)
                data = stdout.read()
                data = data.split('\n')
                cpu_dat = convert_cpu_data(data)
                us = 'NA'
                if self.containers_cpudata.has_key(cont.get('name')):
                    data1 = self.containers_cpudata.get(cont.get('name'))
                    data2 = cpu_dat
                    td = (data2.get('date') - data1.get('date')).seconds
                    cpu =  (int(data2.get('user')) + int(data2.get('system'))- (int(data1.get('user'))+int(data1.get('system'))) )
                    us = ((float(cpu) / int(data2.get('CLK_TCK')))/td)*100  
                    us = '%.0f' % us  
                cont.update({'cpu' : us})
                self.containers_cpudata.update( {cont.get('name') : cpu_dat} ) 
        
    def refresh_container_info(self):
        print '3.1'
        cont_names = []
        for cont in self.ws_client.containers.all():
            print cont
            if cont.name in self.config.get('excluded_containers', ()):
                    continue 
            print '3.2'
            x = ContainerInfo(self.ws_client, cont.name)
            print '3.3'   
            data_dict = {
                "architecture": cont.architecture,
                "config": cont.config,
                "created_at": cont.created_at,
                "devices": cont.devices,
                "ephemeral": cont.ephemeral,
                "expanded_config": cont.expanded_config,
                "expanded_devices": cont.expanded_devices,
                "name": cont.name,
                "profiles": cont.profiles,
                "status": cont.status,
                "status_code": cont.status_code,
                "stateful": cont.stateful,
                #"snapshots": self.get_snapshot_list(cont, cont.name),
                #"snapshots": cont.snapshots.all(),
                "snapshots": [c.name for c in cont.snapshots.all()],
                "mac": cont.expanded_config["volatile.eth0.hwaddr"],
                "inet" : x.network,
                "memory" : x.memory
               }
            print '3.4'
            cont_names.append(data_dict)
            print '3.5'
            
        print '3.6'
        self.containers = cont_names
        print '3.7'
        #self.refresh_container_stats()
        print '3.8'
        self.clientupdaterequest.set()
        print '3.9'
        

    
class Servers(object):
    config = None
    servers = {}
    clientupdaterequest = threading.Event()
     
    def __init__(self, config):
        print '1.1'
        self.clientupdaterequest.clear()
        print '1.2'
        self.config = config
        print '1.3'
        for s in config:
            print s
            svr = Server(s, config.get(s), self.clientupdaterequest)
            print '1.4'
            svr.start()
            print '1.5'
            self.servers.update({ s : svr })
            print '1.6'
        
    def get(self, server=None):
        if server:
            return self.servers.get(server)
        else:
            return self.servers    
        
    def get_display_info(self):
        d = {}
        for s in self.servers:
            d.update({s: self.servers.get(s).get_info()})
        return d
    
    def get_client_update(self):
        return self.clientupdaterequest
    
    def get_containers(self):
        conts = {}
        for s in self.servers:
            conts.update({ s : self.servers.get(s).get_containers()})
        return conts   
