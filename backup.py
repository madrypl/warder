import os
import shutil
import time
import errno
from config import Config
from config import ConfigManager
import subprocess


class Backup(object):

    def __init__(self, config, dry):
        self._config = config
        self._dry_run = dry
        
    def _backup_archive_name(self):
        return self._config.store_root + '/' \
            + self._config.name \
            + '_' \
            + str(self._timestamp) \
            + '.tgz'
            
    def _backup_name(self):
        return ConfigManager.instance().work_root + '/' \
            + self._config.name \
            + '_' \
            + str(self._timestamp) \
            + '.tgz'
            
    def _snar_archive_name(self):
        return self._config.store_root + '/' \
            + self._config.name \
            + '_' \
            + str(self._timestamp) \
            + '.snar.bkp'
            
    def _snar_name(self):
        return ConfigManager.instance().snar_root + '/' + self._config.name + '.snar'
    
    def _validate(self):
        if not os.path.isfile(self._snar_name()):
            pass
        if not os.path.isdir(self._config.root):
            pass
        
    def _make_excludes(self):
        excludes = []
        for p in self._config.exclude.split(';'):
            excludes += [ '--exclude=' + p ]
        return excludes
        
    def _make_args(self):
        args = []
        if self._config.force:
            args += [ '--level=0' ]
            
        args += [ '-g', self._snar_name() ]
        args += [ '-C', self._config.root ]
        
        if self._config.exclude_file and os.path.isfile(self._config.exclude_file):
            args += [ '-X', self._config.exclude_file ]
            
        args += self._make_excludes()
        args += [ '-czf', self._backup_name() ]
        args += [ '.' ]
        return args
    
    def _check_or_make_path(self, path):
        if not os.path.isdir(path):
            try:
                if self._dry_run:
                    print "mkdir -p " + path
                else:
                    os.makedirs(path)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise
    
    def _execute_tar(self):
        tar = ['tar']
        tar += self._make_args()
        if not self._dry_run:
            subprocess.call(tar)
        else:
            print ' '.join(tar,)
    
    def _store(self):
        if not self._dry_run:
            shutil.move(self._backup_name(), self._backup_archive_name())
            shutil.copy2(self._snar_name(), self._snar_archive_name())
        else:   
            print "mv " + self._backup_name() + " " + self._backup_archive_name()
            print "cp " + self._snar_name() + " " + self._snar_archive_name()
    
    def _make_paths(self):
        self._check_or_make_path(ConfigManager.instance().snar_root)
        self._check_or_make_path(ConfigManager.instance().work_root)
        self._check_or_make_path(self._config.store_root)
    
    def create(self):
        self._timestamp = int(time.time())
        self._make_paths()
        self._execute_tar()
        self._store()
            
    
if __name__ == '__main__':
    cfg = Config()
    cfg.name = 'artur_home'
    cfg.force = False
    cfg.root = '/home/artur'
    cfg.exclude = '.cache'
    cfg.store_root = '/opt/backups'
    
    bkp = Backup(cfg, True)
    bkp.create()
    
