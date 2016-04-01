#!/usr/bin/env/python
"""Installation script
Version handling borrowed from pandas project.
"""

import sys
import os
import warnings

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

LONG_DESCRIPTION = """

tbd
"""

MAJOR = 0
MINOR = 1
MICRO = 0
ISRELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
QUALIFIER = ''

if os.environ.get('READTHEDOCS', False) == 'True':
    INSTALL_REQUIRES = []
else:
    INSTALL_REQUIRES = ['networkx']

FULLVERSION = VERSION
if not ISRELEASED:
    FULLVERSION += '.dev'
    try:
        import subprocess
        try:
            pipe = subprocess.Popen(["git", "rev-parse", "--short", "HEAD"],
                                    stdout=subprocess.PIPE).stdout
        except OSError:
            # msysgit compatibility
            pipe = subprocess.Popen(
                ["git.cmd", "describe", "HEAD"],
                stdout=subprocess.PIPE).stdout
        rev = pipe.read().strip()
        # makes distutils blow up on Python 2.7
        if sys.version_info[0] >= 3:
            rev = rev.decode('ascii')

        FULLVERSION = '%d.%d.%d.dev-%s' % (MAJOR, MINOR, MICRO, rev)

    except:
        warnings.warn("WARNING: Couldn't get git revision")
else:
    FULLVERSION += QUALIFIER


def write_version_py(filename=None):
    cnt = """\
version = '%s'
short_version = '%s'
"""
    if not filename:
        filename = os.path.join(
            os.path.dirname(__file__), 'geopandas', 'version.py')

    a = open(filename, 'w')
    try:
        a.write(cnt % (FULLVERSION, VERSION))
    finally:
        a.close()

write_version_py()

setup(name='pycombo',
      version=FULLVERSION,
      description='Combo graph partition wrapper',
      license='MIT',
      author='Philipp Kats',
      author_email='casyfill@gmail.com',
      url='https://github.com/Casyfill/pyCOMBO',
      long_description=LONG_DESCRIPTION,
      packages=['combo','pyCombo'],
      install_requires=INSTALL_REQUIRES)