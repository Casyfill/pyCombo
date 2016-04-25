#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for pycombo.

    This file was generated with PyScaffold 2.5.5, a tool that easily
    puts up a scaffold for your new Python project. Learn more under:
    http://pyscaffold.readthedocs.org/
"""

import sys
from setuptools import setup


def setup_package():
    needs_sphinx = {'build_sphinx', 'upload_docs'}.intersection(sys.argv)
    sphinx = ['sphinx'] if needs_sphinx else []
    setup(setup_requires=['six', 'pyscaffold>=2.5a0,<2.6a0'] + sphinx,
          use_pyscaffold=True)


if __name__ == "__main__":
    setup_package()

LONG_DESCRIPTION = """

tbd
"""

MAJOR = 0

INSTALL_REQUIRES = ['networkx']
FULLVERSION = '1.1.0'


setup(name='pycombo',
      version=FULLVERSION,
      description='Combo graph partition wrapper',
      license='MIT',
      author='Philipp Kats',
      author_email='casyfill@gmail.com',
      url='https://github.com/Casyfill/pyCOMBO',
      long_description=LONG_DESCRIPTION,
      packages=['combo', 'pyCombo'],
      install_requires=INSTALL_REQUIRES)

