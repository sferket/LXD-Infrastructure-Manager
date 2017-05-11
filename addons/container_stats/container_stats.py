from lxd_infrastructure_manager.addons import Container
import time
 
class ContInfo(Container):
    def update(self):
        print 'CONT UPDATE...................................'
        #self.cmd_async('*', 'status.uptime')
        #self.cmd_async('*', 'status.loadavg')
        #self.cmd_async('*', 'status.meminfo')
        #self.cmd_async('*', 'ps.cpu_percent')
        #static_info = ['status.uptime', 'num_cpus', 'cpu_model']
        #self.cmd_async('*', 'grains.item', static_info)

    
    

    