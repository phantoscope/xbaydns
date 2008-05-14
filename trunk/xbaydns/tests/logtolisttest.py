#!/usr/bin/env python
# encoding: utf-8
"""
logtolisttest.py

Created by QingFeng on 2007-11-19.
Copyright (c) 2007 xBayDNS Team. All rights reserved.
"""

import basetest
import logging.config
import os
import pwd
import shutil
import tempfile
import time
import unittest

log = logging.getLogger('xbaydns.tests.logtolisttest')
#logging.basicConfig(level=logging.DEBUG)

from xbaydns.tools import logtolist

class LogToListTest(basetest.BaseTestCase):
    def setUp(self):
        """初始化测试环境"""
        self.basedir = os.path.realpath(tempfile.mkdtemp(suffix='xbaydns_test'))
        basetest.BaseTestCase.setUp(self)

    def tearDown(self):
        """清洁测试环境"""
        shutil.rmtree(self.basedir)
        basetest.BaseTestCase.tearDown(self)
        
    def test_logtolist(self):
        log='''
        queries: info: client 60.190.58.178#2370: view view_any: query: www.xxx.cn IN A +
        queries: info: client 210.36.16.33#32773: view view_any: query: bbs.xxx.cn IN A -E
        '''
        ips=logtolist.logtolist(log)
        self.assertTrue(isinstance(ips,list))
        print ips

def suite():
    """集合测试用例"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LogToListTest, 'test'))
    return suite

"""
单独运行command的测试用例
"""
if __name__ == '__main__':
    unittest.main(defaultTest='suite')
