#!/usr/bin/env python
# encoding: utf-8
"""
setup.py

Created by 黄 冬 on 2007-11-19.
Copyright (c) 2007 __MyCompanyName__. All rights reserved.
"""

import os
from setuptools import setup, find_packages
import sys


setup(
	name = 'xbaydns',
	version = '0.1',
	description = 'Easy DNS Interface',
	long_description = \
"""Easy DNS Interface.""",
	author = 'xBayDNS Team',
	author_email = 'huangdong@gmail.com',
	license = 'BSD License',
	url = 'http://xbaydns.googlecode.com',
	download_url = 'http://xbaydns.googlecode.com',
	zip_safe = False,

	packages = find_packages(exclude=['*.tests*']),
	test_suite = 'xbaydns.tests.suite'
)
