from lxd_infrastructure_manager.addons import Host
 
class HostStats(Host):
    def update(self):
        self.cmd_async('*', 'status.meminfo')
    
    

    