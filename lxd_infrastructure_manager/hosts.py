import salt.client
import salt.version
import salt.utils
import threading
import time
import salt.utils.event

host_discover_target = '*'#'salt-test'

def event_callback(hosts):
    for ret in hosts.salt_client.event.iter_events():
        if ret.has_key('return') and len(ret.get('return')) > 0:
            for key, val in ret.get('return').iteritems():
                #print 'RET0:%s' % (ret)
                #print 'RET:%s - %s' % (key, val)
                if not (type(val) == str):  # Ignore Python error messages
                    hosts.get_host(ret.get('id')).add_info(key, val)
                if key in ['lxd.container_delete', 'lxd.container_create']:
                    hosts.do_updates() 
                #hosts.setUpdateEvent()
            
    
class Host():
    name = None
    fun = {}
    
    def __init__(self, name):
        self.name = name
        self.fun = {'servername' : name}
    
    def add_info(self, func, output):
        self.fun.update({func : output})

    def get_info(self):
        return self.get()
              
    def get(self):
        return self.fun


class Hosts():
    salt_client = None
    hosts = {}
    containers = {}
    updateEvent = None

    def __init__(self):
        self.salt_client = salt.client.LocalClient()
        #self.callback_expected.clear()
        self._th = threading.Thread(target=event_callback,  args=(self,))
        self._th.daemon = True
        self._th.start()

    def initUpdateEvent(self, updateEvent):
        self.updateEvent = updateEvent 

    def setUpdateEvent(self):
        print 'SET UPDATE EVENT'
        if self.updateEvent:
            self.updateEvent.set()

    def get_host(self, name):
        if not self.hosts.has_key(name):
            self.hosts.update({ name : Host(name) })
        return self.hosts.get(name)

    def update_static_info(self):
        #print 'UPDATE STATIC INFO........................'
        static_info = ['lsb_distrib_description', 'num_cpus', 'mem_total', 'cpu_model'
                       , 'saltversion', 'lsb_distrib_codename', 'kernelrelease', 'ip4_interfaces']
        self.cmd_async(host_discover_target, 'grains.item', static_info)

    def update_container_info(self):
        self.cmd_async(host_discover_target, 'lxd.container_get')
        self.cmd_async(host_discover_target, 'lxd.snapshots_all')
        self.cmd_async(host_discover_target, 'lxd.profile_list')
        self.cmd_async(host_discover_target, 'lxd.image_list')
    
    def exec_container_cmd(self,server, container, method, tar_name):
        if method == 'create_snapshot':
            self.salt_client.cmd_async(server, 'lxd.snapshots_create', [container, tar_name])
        elif method == "delete_snapshot":
            self.salt_client.cmd_async(server, 'lxd.snapshots_delete', [container, tar_name])
        elif method == "activate_snapshot":
            data = {"type": "copy",
                    "source": "%s/%s" % (container, tar_name.get('name'))}
            self.cmd_async(server, 'lxd.container_create', [tar_name.get('name'), data])
        elif method == "delete":
            self.cmd_async(server, 'lxd.container_delete', [container])
            #print 'Delete not implemented for now'
        
    def cmd_async(self, *args):
        # Convert to list, to enforce the calling function in the return  
        print 'cmd_async: %s' % ([args])
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
        kwargs = {}
        self.salt_client.cmd_async(*args2, **kwargs)
        #self.callback_expected.set()

    def get(self, host=None):
        if host:
            return self.hosts.get(host)
        else:
            return self.hosts
      
    def get_display_info(self):
        d = {}
        for s in self.hosts:
            d.update({s: self.hosts.get(s).fun })
        return d
              
    def get_tree_list(self, checksum):
        print 'TREEEEEEEEEEEEEEEEEEEE TREE'
        nodes = {}
        for hostname,hostitems in self.hosts.iteritems():
            nodeID = 'host.%s' % hostname
            nodes.update ({ nodeID : {'parent' : None
                       , 'name' : hostname
                       , 'host' : hostname 
                       , 'nodeId': nodeID
                       , 'type' : 'host'
                       , 'image' : "/static/img/container-host.png"
                       , 'expanded' : False}
                       })
            if hostitems.get_info().has_key('lxd.container_get'):
                for containers in hostitems.get_info().get('lxd.container_get'):
                    for k,v in containers.iteritems():
                        nodeID = 'container.%s' % k
                        parent = 'host.%s' % hostname
                        if v.get('config').get('user.parent'):
                            #if  hostitems.get_info().get('lxd.container_get').has_key(v.get('config').get('user.parent')):
                            parent = 'container.%s' % v.get('config').get('user.parent')
                        nodes.update ({ nodeID : {'parent' : parent
                                   , 'name' : k
                                   , 'host' : hostname
                                   , 'container' : k
                                   , 'nodeId': nodeID 
                                   , 'type' : 'container'
                                   , 'image' : "/static/img/container-green.png"
                                   , 'expanded' : False }
                                 
                                   })

        # check for missing parents....
        missing_nodes = {}
        for k,v in nodes.iteritems():
            p = v.get('parent')
            if p not in nodes.keys():
                if v.get('type') == 'container':
                    nodeID = p #'map.%s' % p.replace('container.', '')
                    parent = 'host.%s' % v.get('host')
                    missing_nodes.update ({ nodeID : {'parent' : parent
                               , 'name' : p.replace('container.', '')
                               , 'nodeId': nodeID 
                               , 'type' : 'map'
                               , 'expanded' : False }  
                                })                  
        for k,v in missing_nodes.iteritems():
            nodes.update({k : v})
            
        parents = {}
        for k,v in nodes.iteritems():
            p = v.get('parent')
            if p not in nodes.keys():
                p = None
            if not parents.has_key(p):
                parents.update({p : []})
            parents[p] += [k]
        
        def pop_list(node, children, level=0):
            childs = []
            if len(children) > 0:
                for c in sorted(children):
                    n = pop_list(c, parents.get(c, []), level=level+1)
                    childs += [n]
                    
            if node:
                p = nodes[node]
                p.update({'children' : childs})
                return p
            else: 
                return childs
 
        res = pop_list(None, parents.get(None))
        cs = str(hash(repr(res)))
        hash(repr(res))
        print 'TREE:%s-%s' % (checksum,cs)
        return cs, (res if cs != checksum else False)
              
    def do_updates(self):
        for func in dir(self):
            if func.startswith('update_'):
                getattr(self, func)()
            
