import os 
from glob import glob
import importlib
import sys
import inspect

#http://stackoverflow.com/questions/972/adding-a-method-to-an-existing-object-instance

def _concat_files(dir):
    ret = ''
    print '+Check:%s' % dir
    if os.path.isdir(dir):
        print '+isdir'
        for d in glob('%s/*.html'%dir):
            ret +=  open(d, 'r').read()
            print '+%s' % ret
    return ret


class Host(object):

    def __init__(self):
        print 'Init Host'

class Tmp():
    tmp = 'not changed'
    def __init__(self):
        print 'tmp'
    

class Container(object):

    def __init__(self, container):
        print 'Init Container %s' % container

class Load():
    addons = {}
    #hosts = None
    host_functions = {}
    host_modals = {}
    host_buttons = {}
    host_sections = ''
    
    def _get_addons_from_directory(self, dir):
        #self.hosts = hosts
        for d in os.listdir(dir):
            if os.path.exists(os.path.join(dir,d,'__manifest__.py')):
                manifest = eval(open(os.path.join(dir,d,'__manifest__.py')).read())
                if manifest.get('type') == 'host':
                    manifest.update({'path' : os.path.join(dir,d) })
                    self.addons.update({d:manifest})
    
    def _remove_buildin_attrs(self,attrs):
        new = []
        for d in dir(attrs):
            if not d.startswith('__'):
                new += [d]
        return new
        
    def __init__(self, addons_path):
        for path in addons_path.split(','):
            self._get_addons_from_directory(path)
            sys.path.append(path)

        for mod, manifest in self.addons.iteritems():
            tst = importlib.import_module(mod)
            self.host_modals.update({mod:_concat_files(os.path.join(manifest.get('path') ,'modals'))})
            self.host_buttons.update({mod:_concat_files(os.path.join(manifest.get('path') ,'buttons'))})
            #self.host_sections.update({mod:_concat_files(os.path.join(manifest.get('path') ,'sections'))})
            self.host_sections += _concat_files(os.path.join(manifest.get('path') ,'sections'))
            
            
        print self.host_modals
        #modals = []
        for sc in Host.__subclasses__():
            inst = sc()
            if 'update' in dir(sc):
                self.host_functions.update({sc.__module__.split('.')[0] : sc.update.__func__})
            
            #print '***********>%s' % self.addons
            #sys.exit()
            #modals += [getattr(inst, 'modals')()]
            #print modals
                
           
            

    def inject_hosts_update_methods(self, hosts):
        for mod, funct in self.host_functions.iteritems():
            setattr(hosts, "update_%s" % mod, funct)
            hosts.sections = self.host_sections
            
        #modals = {}
        #buttons = {}
        #sections = {}
         
        
#         print '++>%s' % self.host_functions
#         print Host.__subclasses__()
#         c = Host.__subclasses__()[0]
#         #MyClass = getattr(tst, c.__name__)
#         #instance = MyClass()#         tst = importlib.import_module('test_module_20170220')
#         #instance.update1()
#         #instance = getattr(c, 'HostStats')
#         instance = c()
#         instance.update1()
#         tmp = Tmp()
#         tmp.update1 = c.update1
#         print '--'
#         print tmp.tmp
#         tmp.update1()
#         print tmp.tmp 
        
#         print tst
#         print tst.__name__
#         for mod in sys.modules:
#             print '->%s' % mod
#         sys.modules['test_module_20170220'].method.test()
#         classes = inspect.getmembers(sys.modules['test_module_20170220'], inspect.isclass)
#         print lxd_infrastructure_manager.host.Host.__subclasses__()
#         print classes
#         sys.exit()


        
    
