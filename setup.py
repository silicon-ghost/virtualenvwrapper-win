#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()

PROJECT = 'virtualenvwrapper-wintcc'
AUTHOR = 'Matthew Zaleski'
EMAIL = 'silicon_ghost25@zaleski.net'
DESCRIPTION = ("Port of David Marble's virtualenvwrapper-win "
               "Windows batch scripts to JPSoft's Take Command/TCC (tested with 12.x)") 
VERSION = '0.9'
PROJECT_URL = 'https://github.com/silicon_ghost/%s/' % (PROJECT)
scripts_loc = 'scripts/'
scripts = [
    'add2virtualenv.btm',
    'cd-.btm',
    'cdproject.btm',
    'cdsitepackages.btm',
    'cdvirtualenv.btm',
    'lssitepackages.btm',
    'lsvirtualenv.btm',
    'mkvirtualenv.btm',
    'rmvirtualenv.btm',
    'setprojectdir.btm',
    'toggleglobalsitepackages.btm',
    'whereis.btm',
    'workon.btm',
]

import os
import sys
import shutil
import codecs
from setuptools import setup
from setuptools.command.install import install as _setuptools_install

long_description = ''
try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    pass

PYTHONHOME = sys.exec_prefix

class install(_setuptools_install):
    def run(self):
        # pre-install
        _setuptools_install.run(self)
        # post-install
        # Re-write install-record to take into account new file locations
        if self.record:
            newlist = []
            with codecs.open(self.record, 'r', 'utf-8') as f:
                files = f.readlines()
            for f in files:
                fname = f.strip()
                for script in scripts:
                    if fname.endswith(script):
                        newname = fname.replace('Scripts\\','')
                        # try:
                        #     os.remove(dst)
                        # except:
                        #     pass
                        shutil.move(fname, newname)
                        fname = newname
                newlist.append(fname)
            with codecs.open(self.record, 'w', 'utf-8') as f:
                f.write('\n'.join(newlist))

setup(
    cmdclass={'install': install},
    name=PROJECT,
    version=VERSION,

    description=DESCRIPTION,
    long_description=long_description,

    author=AUTHOR,
    author_email=EMAIL,
    url=PROJECT_URL,
    license="MIT License",
    keywords="setuptools deployment installation distutils virtualenv virtualenvwrapper virtualenvwrapper-win",

    platforms=['WIN32', 'WIN64',],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Win32 (MS Windows)',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 2.4',
        #'Programming Language :: Python :: 2.5',
        #'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.0',
        #'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Intended Audience :: Developers',
        'Environment :: Console', ],

    scripts=[scripts_loc + script for script in scripts],

    install_requires=['virtualenv>=1.9.1',],
    
    # extras
    # pywin==0.2

    zip_safe=False,
)