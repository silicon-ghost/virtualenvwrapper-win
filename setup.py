#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.install import install as _setuptools_install
import io
import codecs
import os
import sys
import shutil


here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst', 'CHANGES.rst')

__version__ = '0.9.1a1'
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

import sys

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
                        shutil.move(fname, newname)
                        fname = newname
                newlist.append(fname)
            with codecs.open(self.record, 'w', 'utf-8') as f:
                f.write('\n'.join(newlist))


setup(
    cmdclass={'install': install},
    name='virtualenvwrapper-wintcc',
    version=__version__,
    url='https://github.com/silicon-ghost/virtualenvwrapper-wintcc',
    license='MIT License',
    author='Matthew Zaleski',
    install_requires=['virtualenv>=1.9.1'],
    author_email='silicon_ghost25@zaleski.net',
    description="Port of David Marble's virtualenvwrapper-win (and Doug Hellman's virtualenvwrapper)"
                "Windows batch scripts to JPSoft's Take Command/TCC",
    long_description=long_description,
    keywords="setuptools deployment installation distutils virtualenv virtualenvwrapper virtualenvwrapper-win",
    #include_package_data=True,
    platforms=['WIN32', 'WIN64',],
    scripts=[scripts_loc + script for script in scripts],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console', 
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        ],
    zip_safe=False,
)
