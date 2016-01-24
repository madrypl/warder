

class Global(object):
    snar_root = '/var/lib/warder' # '/var/lib/warder'
    work_root = '/tmp'
    @staticmethod
    def instance():
        return _globalInstance

class Config(object):
    """ name - identifier string. Backup file names are based on this string """
    name = None
    """ force - do level 0 backup instead incremental """
    force = False
    """ root - path to be backup"""
    root = None
    """ exclude - list of patterns passed to tar as '--exclude' directive. 
        Elements are separated by ';'.
        Example: .cache;.tmp;.git """
    exclude = None
    """ exclude_file - file within exclude paths are defined """
    exclude_file = None
    
    """ store_root - path where backup will be stored """
    store_root = None
    
    def __init__(self):
        pass
 
_globalInstance = Global()   
# what to do if incremental package doesn't fit in store_root?'
# 1. stream to storage directly
# 2. provide alternate location
