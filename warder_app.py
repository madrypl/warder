'''
Created on 24 sty 2016

@author: artur
'''
import argparse
from config import ConfigManager
from backup import Backup

class WarderApp(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.arguments()
        
    def arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--full', action='store_true',
                            help='Do full backup instead incremental (level0)')
        parser.add_argument('-d', '--dry-run', action='store_true',
                            help='Print instead execute commands')
        parser.add_argument('-c', '--config', help='Configuration file path', 
                            default='/etc/warder/warder.conf')
        parser.add_argument('command', help='Must be create')
        self._args = parser.parse_args()
        if not hasattr(self, self._args.command):
            print 'Unrecognized command'
            parser.print_usage()
            exit(1)
        getattr(self, self._args.command)()
        
    def create(self):
        configManager = ConfigManager.instance()
        configManager.load(self._args.config)
        for cfg in configManager.configs:
            print 'Backuping ' + cfg.name
            bkp = Backup(cfg, self._args.dry_run)
            bkp.create()
        pass
        
if __name__ == '__main__':
    WarderApp()
    pass
