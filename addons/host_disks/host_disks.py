from lxd_infrastructure_manager.addons import Host
#import time
 
class HostStats(Host):
    def update(self):
        self.cmd_async('*', 'disk.usage')

    
    

    