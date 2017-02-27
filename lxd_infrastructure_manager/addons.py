import os 
from glob import glob

def _concat_files(self, dir):
    ret = ''
    if os.direxists(dir):
        for d in glob('./%s/*.html'%dir):
            ret +=  open(d, 'r').read()
    return ret


class Host(object):

    def __init__(self, host):
        print 'Init Host %s' % host

    def modals(self):
        return _concat_files('modals')

    def buttons(self):
        return _concat_files('buttons')
    

class Container(object):

    def __init__(self, container):
        print 'Init Container %s' % container

    def modals(self):
        return self._concat_files('modals')

    def buttons(self):
        return self._concat_files('buttons')
    
        
    
