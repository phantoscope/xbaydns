#!/usr/bin/env python
# encoding: utf-8
"""
nsupdatetest.py

Created by Razor on 2007-11-29.
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

log = logging.getLogger('xbaydns.tests.nsupdatetest')
logging.basicConfig(level=logging.DEBUG)
from xbaydns.tools import initconf
from xbaydns.tools import namedconf
from xbaydns.tools import nsupdate
from xbaydns.conf import sysconf
from xbaydns.utils import shtools


class NSUpdateTest(basetest.BaseTestCase):
    def setUp(self):
        """初始化测试环境"""
        basetest.BaseTestCase.setUp(self)
        self._initnamedconf()
        
    def tearDown(self):
        """清洁测试环境"""
        basetest.BaseTestCase.tearDown(self)

    def _initnamedconf(self):
        returncode = initconf.main()
        namedconf_obj = namedconf.NamedConf()
        namedconf_obj.addDomain('', ['example.com'])
        namedconf_obj.save()
        os.system("rndc reload")
            
    def test_addRecord(self):
        self._initnamedconf()
        recordlist = [['foo', 3600, 'IN', 'A', ['192.168.1.1', '172.16.1.1'],
                            ['bar', 3600, 'ANY', 'CNAME', ['foo']],
                            ['', 86400, 'IN', 'MX', ['10 foo']]
        nsupobj = nsupdate.NSUpdate('127.0.0.1', 'example.com.')
        nsupobj.addRecord(recordlist)
        record_a = nsupobj.queryRecord('foo', rdtype='A')
        self.assertEqual(record_a, ['192.168.1.1', '172.16.1.1'])
        record_cname = nsupobj.queryRecord('bar', rdtype='CNAME')
        self.assertEqual(record_cname, ['foo.example.com'])
        record_mx = nsupobj.queryRecord('', rdtype='MX')
        self.assertEqual(record_mx, ['10 foo.example.com'])
        
    def test_removeRecord(self):
        self._initnamedconf()
        dbfile = open(sysconf.chroot_path+sysconf.namedconf+"/dynamic/.example.com.file", "a")
        dbfile.write("foo\t\tIN\tA\t192.168.1.1\n\t\t\t\t\t\t172.16.1.1\nexample.com. 86400\tIN\tMX\tfoo.example.com\nbar\t\tIN\tCNAME\tfoo.example.com.\n")
        dbfile.close()
        os.system("rndc reload")
        recordlist =  ['', 86400, 'IN', 'MX', ['10 foo']]
        nsupobj = nsupdate.NSUpdate('127.0.0.1', 'example.com.')
        nsupobj.removeRecord(recordlist)        
        recordlist = ['bar']
        nsupobj.removeRecord(recordlist, True)
        self.assertEqual(record_a, ['192.168.1.1', '172.16.1.1'])
        deleted = False
        try:
            record_cname = nsupobj.queryRecord('bar', rdtype='CNAME')
        except nsupdate.NSUpdateException:
            deleted = True
        self.assertTrue(deleted)
        deleted = False
        try:
            record_mx = nsupobj.queryRecord('', rdtype='MX')
        except nsupdate.NSUpdateException:
            deleted = True
        self.assertTrue(deleted)
        
    def test_queryRecord(self):
        self._initnamedconf()
        dbfile = open(sysconf.chroot_path+sysconf.namedconf+"/dynamic/.example.com.file", "a")
        dbfile.write("foo\t\tIN\tA\t192.168.1.1\n\t\t\t\t\t\t172.16.1.1\nexample.com. 86400\tIN\tMX\tfoo.example.com\nbar\t\tIN\tCNAME\tfoo.example.com.\n")
        dbfile.close()
        os.system("rndc reload")
        nsupobj = nsupdate.NSUpdate('127.0.0.1', 'example.com.')
        record_a = nsupobj.queryRecord('foo', rdtype='A')
        self.assertEqual(record_a, ['192.168.1.1', '172.16.1.1'])
        record_cname = nsupobj.queryRecord('bar', rdtype='CNAME')
        self.assertEqual(record_cname, ['foo.example.com'])
        record_mx = nsupobj.queryRecord('', rdtype='MX')
        self.assertEqual(record_mx, ['10 foo.example.com'])
        
def suite():
    """集合测试用例"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NSUpdateTest, 'test'))
    return suite

"""
单独运行command的测试用例
"""
if __name__ == '__main__':
    unittest.main(defaultTest='suite')
