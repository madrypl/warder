import ConfigParser

class ConfigManager(object):
    snar_root = '/var/lib/warder'
    work_root = '/tmp'
    configs = []
    @staticmethod
    def instance():
        return _configManagerInstance

    def _load_global(self, config):
        if not config.has_section('Global'):
            raise Exception('Section \'Global\' must be present')
        self.snar_root = config.get('Global', 'snar_root')
        self.work_root = config.get('Global', 'work_root')
        
    def _load_configs(self, config):
        cfgs = config.sections()
        cfgs.remove('Global')
        self.configs = []
        for name in cfgs:
            cfg = Config.load(name, config)
            self.configs.append(cfg)
        
    def load(self, path):
        config = ConfigParser.RawConfigParser()
        config.read(path)
        self._load_global(config)
        self._load_configs(config)
        

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
    
    @staticmethod
    def load(name, config):
        c = Config()
        c.name = name;
        c.root = config.get(name, 'root')
        c.store_root = config.get(name, 'store_root')
        if config.has_option(name, 'exclude'):
            c.exclude = config.get(name, 'exclude')
        if config.has_option(name, 'exclude_file'):
            c.exclude_file = config.get(name, 'exclude_file')
        if config.has_option(name, 'force'):
            c.force = config.get(name, 'force')
        return c
    
_configManagerInstance = ConfigManager()   


if __name__ == '__main__':
    ConfigManager.instance().load('warder.conf')
    pass