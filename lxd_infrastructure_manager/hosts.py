import salt.client
import salt.version
print salt.version.__saltstack_version__
print salt
import salt.utils
import threading
import time
import salt.utils.event

host_discover_target = '*'#'salt-test'

def event_callback(hosts):
    while True:  
        print 'Callback?' 
        hosts.callback_expected.wait(60)
        for it in hosts.salt_client.get_event_iter_returns(hosts.jid, '*'):
            print '--->%s' % it
            if len(it.keys()) > 0:
                host = it.keys()[0]
                for key, ret in it.get(host).get('ret').items():
                    #print ret
                    hosts.get_host(host).add_info(key, ret)
            #print hosts.get_host(host).get()
        hosts.callback_expected.clear()
    
class Host():
    name = None
    fun = {}
    
    def __init__(self, name):
        self.name = name
    
    def add_info(self, fun, output):
        self.fun.update({fun : output})

    def get_info(self):
        return self.get()
              
    def get(self):
        return {self.name : self.fun}


class Hosts():
    salt_client = None
    hosts = {}
    jid = None
    callback_expected = threading.Event()

    def __init__(self):
        self.salt_client = salt.client.LocalClient()
        self.jid = salt.utils.jid.gen_jid()
        self.callback_expected.clear()
        self._th = threading.Thread(target=event_callback,  args=(self,))
        self._th.daemon = True
        self._th.start()
        self.update_static_info()
        #self.cmd_async(host_discover_target, 'status.meminfo')
        
        #self.cmd_async(host_discover_target, 'status.cpuinfo')
        
        #self.cmd_async(host_discover_target, ('status.meminfo', 'status.cpuinfo'), ('', '') )
        #self.cmd_async(host_discover_target, ['status.meminfo'], [[]] )
        #self.cmd_async(host_discover_target, 'status.meminfo')
        #self.cmd_async(host_discover_target, 'status.cpuinfo')
        print 2


    def get_host(self, name):
        if not self.hosts.has_key(name):
            self.hosts.update({ name : Host(name) })
        return self.hosts.get(name)

    def update_static_info(self):
        # Get status host information
        print 'b1'
        static_info = ['lsb_distrib_description', 'num_cpus', 'mem_total', 'cpu_model'
                       , 'saltversion', 'lsb_distrib_codename']
        print 'b2'
        self.cmd_async(host_discover_target, 'grains.item', static_info)
        print 'b3'
        
    def cmd_async(self, *args):
        print 'c1'
        # Convert to list, to enforce the calling function in the return  
        args2=[]
        if type(args[1]) != type([]):
            args2 += [args[0]]
            args2 += [[args[1]]]
            if len(args) > 2:
                args2 += [[args[2]]]
            else:
                args2 += [[[]]]
        else:
            args2=args
        kwargs = {'jid':self.jid}
        print self.salt_client
        print 'c2'
        #print salt.master.log.critical("dd") #.client.log.error("bla bla")
        self.salt_client.cmd_async(*args2, **kwargs)
        #print self.salt_client.run_job('*', 'test.ping')
        print 'c3'
        
#         #print self.salt_client.cmd_async('*', 'test.ping', jid=self.jid )
#         jid = self.salt_client.cmd_async('sandbox-16.lxd', 'test.ping')
#         #jid = self.salt_client.run_job('*', 'test.ping')
#         #jid = jid.get('jid')
#         #for gen in self.salt_client.get_cli_returns(jid, '*'):
#         #    print 'gen:%s' % gen
#         time.sleep(1)
#         #ret = self.salt_client.cmd_iter_no_block('*', 'test.ping')
#         #print ret
#         #for i in ret:
#         #    print(i)
#         for it in self.salt_client.get_event_iter_returns(jid, '*'):
#             print '+++>%s' % it
#         print 'c4'
        self.callback_expected.set()
        print 'c5'

    def get(self, host=None):
        if host:
            return self.hosts.get(host)
        else:
            return self.hosts
      
    def get_display_info(self):
        d = {}
        for s in self.hosts:
            d.update({s: {'servername' : s, 'uptime':'56', 'sections' : self.sections}})
            #d.update({})
        return d
              

    def do_updates(self):
        for func in dir(self):
            if func.startswith('update_'):
                getattr(self, func)()
            
#hosts = Hosts()
#time.sleep(20)
