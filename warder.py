#!/usr/bin/python
import re
import os
import glob
import shutil
import time
import subprocess

class Backup(object):
    _full_bkp = False
    _exclude = 'etc/exclude'
    _snar = 'var/backup.snar'
    _bkp_root = '/home/madrzaka/streams/ws_amadrzak1/build'
    _archive_path = 'storage/'


    def _archiveName(self):
        self._timestamp = int(time.time())
        return 'backup_' + str(self._timestamp) + '.tgz'

    def _snarBackupName(self):
        return 'backup_' + str(self._timestamp) + '.snar'

    def _backupSnar(self):
        shutil.copy2(self._snar, self._archive_path + self._snarBackupName())
        pass

    def _restoreSnar(self):
        re_snar = re.compile('.*\.snar')                 
        files = filter(lambda x: re_snar.match(x) and os.path.isfile(self._archive_path + x), 
                       os.listdir(self._archive_path))
        if files:
            files.sort(key=lambda x: os.stat(os.path.join(self._archive_path, x)).st_ctime)
            shutil.copy2(self._archive_path + files[0], self._snar)
            print "Restored " + files[0]
        else:
            print "No snar backup found"

    def _makeArgs(self):
        args = []
        if self._full_bkp:
            args += [ '--level=0' ]
        if not os.path.isfile(self._snar):
            print "Warning: no snar file detected"
            self._restoreSnar()
        args += [ '-g', self._snar ]
        args += [ '-C', self._bkp_root ]
        if os.path.isfile(self._exclude):
            args += [ '-X', self._exclude ]
        args += [ '-czf', self._archive_path + self._archiveName() ]
        return args

    def _makeUntarArgs(self, name):
        args = []
        args += [ '-g', '/dev/null' ]
        args += [ '-C', self._bkp_root + '/../restoration' ]
        args += [ '-xzf', self._archive_path + name ]
        return args

    def _tar(self):
        tar = [ 'tar' ]
        tar += self._makeArgs()
        tar += [ '.' ]
        print tar
        rv = subprocess.call(tar)

    def _untar(self, name):
        tar = [ 'tar' ]
        tar += self._makeUntarArgs(name)
        print tar
        rv = subprocess.call(tar)

    def do(self):
        self._tar()
        self._backupSnar()
        pass

    def restore(self):
        re_tgz = re.compile('.*\.tgz')                 
        files = filter(lambda x: re_tgz.match(x) and os.path.isfile(self._archive_path + x), 
                       os.listdir(self._archive_path))
        if not os.path.isdir(self._bkp_root + '/../restoration'):
            os.mkdir(self._bkp_root + '/../restoration')
        if files:
            files.sort(key=lambda x: os.stat(os.path.join(self._archive_path, x)).st_ctime)
            for f in files:
                print "Restoring", f
                self._untar(f)
                
b = Backup()
b.restore()
