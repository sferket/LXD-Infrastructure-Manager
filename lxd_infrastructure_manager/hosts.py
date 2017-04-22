import salt.client
import salt.version
#print salt.version.__saltstack_version__
#print salt
import salt.utils
import threading
import time
import salt.utils.event

host_discover_target = '*'#'salt-test'

def event_callback(hosts):
#     while True:  
#         hosts.callback_expected.wait(60)
#         for it in hosts.salt_client.get_event_iter_returns(hosts.jid, '*'):
#             print '>>>>>%s' % it
#             if len(it.keys()) > 0:
#                 #print '--+>%s' % it.keys()[0]
#                 host = it.keys()[0]
#                 print 'EVENT_CALLBACK(%s)->%s' % (host, it)
#                 for key, ret in it.get(host).get('ret').items():
#                     hosts.get_host(host).add_info(key.replace('.', '_'), ret)
#         hosts.callback_expected.clear()
    for ret in hosts.salt_client.event.iter_events():
        if ret.has_key('return') and len(ret.get('return')) > 0:
            for key, val in ret.get('return').iteritems():
                print '99999999999999999999999999999999999999999999999999999999999999999'
                print '%s ---> %s -> %s' % (ret.get('id'), key.replace('.', '_'), val)
                hosts.get_host(ret.get('id')).add_info(key.replace('.', '_'), val)

    
    
class Host():
    name = None
    fun = {}
    
    def __init__(self, name):
        self.name = name
        self.fun = {'servername' : name}
    
    def add_info(self, func, output):
        if func == 'grains_item':
            print '--UPDATE(%s)-->%s' % (self.name, func) 
        #print '--UPDATE2(%s)-->%s' % (self.name, self.fun)
        self.fun.update({func : output})
        #print '--UPDATE3(%s)-->%s' % (self.name, self.fun)

    def get_info(self):
        return self.get()
              
    def get(self):
        #return {self.name : self.fun}
        return self.fun


class Hosts():
    salt_client = None
    hosts = {}
    containers = {}
    #hosts = { 'eng-lxd1' : Host('eng-lxd1'), 'sandbox-16.lxd' : Host('sandbox-16.lxd')}
    #jid = None
    callback_expected = threading.Event()

    def __init__(self):
        self.salt_client = salt.client.LocalClient()
        #self.jid = salt.utils.jid.gen_jid()
        self.callback_expected.clear()
        self._th = threading.Thread(target=event_callback,  args=(self,))
        self._th.daemon = True
        self._th.start()


    def get_host(self, name):
        if not self.hosts.has_key(name):
            self.hosts.update({ name : Host(name) })
        return self.hosts.get(name)

    def update_static_info(self):
        # Get status host information
        static_info = ['lsb_distrib_description', 'num_cpus', 'mem_total', 'cpu_model'
                       , 'saltversion', 'lsb_distrib_codename', 'kernelrelease', 'ip4_interfaces']
        #static_info = ['lsb_distrib_description','status.uptime', 'num_cpus', 'cpu_model']
        self.cmd_async(host_discover_target, 'grains.item', static_info)

    def update_container_info(self):
        print 'oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'
        #salt '*' 
        # Avaialble commands: https://github.com/pcdummy/saltstack-lxd-formula/blob/master/_modules/lxd.py
        self.cmd_async(host_discover_target, 'lxd.container_get')
        self.cmd_async(host_discover_target, 'lxd.snapshots_all')
        # salt '*' lxd.container_state
        # Snapshots seem to be missing,alternative: salt 'sandbox-16.lxd' cmd.run "lxc info test123"
    
    def exec_container_cmd(self,server, container, method, tar_name):
        print method
        if method == 'create_snapshot':
            self.salt_client.cmd_async(server, 'lxd.snapshots_create', [container, tar_name])
        elif method == "delete_snapshot":
            self.salt_client.cmd_async(server, 'lxd.snapshots_delete', [container, tar_name])
        elif method == "activate_snapshot":
            data = {"type": "copy",
                    "source": "%s/%s" % (container, tar_name.get('name'))}
            self.cmd_async(server, 'lxd.container_create', [tar_name.get('name'), data])
        
            

        
    def cmd_async(self, *args):
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
        #kwargs = {'jid':self.jid}
        kwargs = {}
        #print salt.master.log.critical("dd") #.client.log.error("bla bla")
        print 'cmd_async'
        print args2
        print kwargs
        self.salt_client.cmd_async(*args2, **kwargs)
        #print self.salt_client.run_job('*', 'test.ping')
        
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

    def get(self, host=None):
        if host:
            return self.hosts.get(host)
        else:
            return self.hosts
      
    def get_display_info(self):
        d = {}
        for s in self.hosts:
            d.update({s: self.hosts.get(s).fun })

        print '++++++++++++++++>%s' % d.get('sandbox-16.lxd')
        return d
              

    def do_updates(self):
        for func in dir(self):
            if func.startswith('update_'):
                getattr(self, func)()
            
#hosts = Hosts()
#time.sleep(20)
