'''
Created on 24 sty 2016

@author: artur
'''

from distutils.core import setup

setup(name = 'warder',
      version='0.1',
      description='Incremental backup utility',
      author='Artur Madrzak',
      author_email='artur@madrzak.eu',
      license="BSD",
      url="https://madrzak.eu",
      py_modules=['config', 'warder_app', 'backup'],
      scripts=['warder'],
      data_files=[('/etc/warder', ['warder.conf'])])