
import ConfigParser

class Global(object):
    snar_root = '/var/lib/warder' # '/var/lib/warder'
    work_root = '/tmp'
    @staticmethod
    def instance():
        return _globalInstance

class Config(object):
    
    name = None
    force = False
    root = None
    exclude = None
    exclude_file = None
    store_root = None
    
    def __init__(self):
        pass
 
_globalInstance = Global()   
# what to do if incremental package doesn't fit in store_root?'
# 1. stream to storage directly
# 2. provide alternate location