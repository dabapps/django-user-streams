#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from setuptools import setup, find_packages


version = '0.1.0'


if sys.argv[-1] == 'publish':
    subprocess.call(['python', 'setup.py', 'sdist', 'upload'])
    print "You probably want to also tag the version now:"
    print "  git tag -a %s -m 'Tag version %s'" % (version, version)
    print "  git push --tags"
    sys.exit()


setup(
    name='django-user-streams',
    version=version,
    description='Simple, fast user news feeds for Django',
    author='Jamie Matthews',
    url='https://github.com/dabapps/django-user-streams',
    packages=find_packages(),
    license='BSD',
)
