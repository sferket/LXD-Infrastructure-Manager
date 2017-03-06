import salt.client
import salt.utils.event
import sys
import importlib
import os
from types import MethodType
import threading
import time



    
    
    

class Client():
    name = None
    salt_client = None
    hosts = None

    def __init__(self):
        print '2.1'
        self.salt_client = salt.client.LocalClient()
        print '2.2:%s' % self.salt_client
        #self.init_hosts()
        self.hosts = Hosts(self.salt_client)
        print '2.3'
        print 'Clinet:%s' % self.salt_client
      
#     def get_host(self, name):
#         if not self.hosts.has_key(name):
#             self.hosts.update({ name : Host(name, self.salt_client) })
#         return self.hosts.get(name)
          
#     def init_hosts(self):
#         # Get status host information
#         static_info = ['lsb_distrib_description', 'num_cpus', 'mem_total', 'cpu_model'
#                        , 'saltversion', 'lsb_distrib_codename']
#         self.update_host_info('*', 'grains.item', static_info)

#     def update_host_info(self, host, function, arguments):
#         jid = self.salt_client.cmd_async(host, function, arguments)
#         for it in self.salt_client.get_event_iter_returns(jid, '*', 2):
#             host = it.keys()[0]
#             self.get_host(host).add_info(function, it.get(host).get('ret'))

    
client = Client()
#client.update_host_info('eng-lxd1', 'grains.item', ['lsb_distrib_description', 'num_cpus', 'mem_total', 'cpu_model'])
for hst in client.hosts.hosts:
    print client.hosts.hosts.get(hst).get()
    #print client.hosts.get(hst).get()

import addons
print addons.Host.__name__    
print os.getcwd()    
sys.path.append('/home/ferkets/git/LXD-Infrastructure-Manager/addons')
sys.path.append('/home/ferkets/git/LXD-Infrastructure-Manager/lxd_infrastructure_manager')
tst = importlib.import_module('host_stats')
print tst.__name__
print tst

time.sleep(20)
#for mod in sys.modules:
#    print '->%s' % mod
#print tst.host_stats.sf()
#client.hosts.get('salt-test').update_host_stats =  lambda: tst.host_stats.HostStats.update(client.hosts.get('salt-test'))
client.hosts.get('salt-test').update_host_stats = MethodType(tst.host_stats.update, client.hosts.get('salt-test'), Host)
client.hosts.get('salt-test').update_host_stats()
for hst in client.hosts:
    print client.hosts.get(hst).get()

 
#print client.update_hosts()