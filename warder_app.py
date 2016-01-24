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
        parser.add_argument('-c', '--config', help='Configuration file path', 
                            default='/etc/warder/warder.conf')
        self._args = parser.parse_args()
        self.create()
        
    def create(self):
        configManager = ConfigManager.instance()
        configManager.load(self._args.config)
        for cfg in configManager.configs:
            print 'Backuping ' + cfg.name
            bkp = Backup(cfg, True)
            bkp.create()
        pass
        
if __name__ == '__main__':
    WarderApp()
    pass
