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
    version = '1.0.1',
    description = 'xBayDNS System',
    long_description = \
"""DNS and GSLB Manager System""",
    author = 'xBay Team',
    author_email = 'huangdong@gmail.com',
    license = 'BSD License',
    url = 'http://xbaydns.googlecode.com',
    download_url = 'http://code.google.com/p/xbaydns/downloads/list',
    zip_safe = False,

    packages = find_packages(exclude=['*tests*']),
    include_package_data = True,
    scripts = [
        'xbaydns/tools/xdgenview', 
        'xbaydns/tools/xdweb',
        'xbaydns/tools/xdsetup',
        'xbaydns/tools/xdmaster',
        'xbaydns/tools/xdslave'],
    test_suite = 'xbaydns.tests.suite',
    entry_points = {
        'console_scripts': [
            'xdinitbind = xbaydns.tools.initconf:main',
            'xdsync = xbaydns.tools.confsync:main',
            'xdwherepkg = xbaydns.utils.pkg:main',
            'xdidc2view = xbaydns.tools.prober.idcview:main',
            'xdreg = xbaydns.tools.xdreg:main'
        ]
    }
)
