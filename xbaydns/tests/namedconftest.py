# encoding: utf-8
"""
namedconftest.py

Created by QingFeng on 2007-11-23.
Copyright (c) 2007 yanxu. All rights reserved.
"""

import basetest
import logging.config
import os
import shutil
import tempfile
import time
import unittest
import base64

log = logging.getLogger('xbaydns.tests.namedconftest')
logging.basicConfig(level=logging.DEBUG)

from xbaydns.tools.namedconf import *

class NamedConfTest(basetest.BaseTestCase):
    def setUp(self):
        """初始化测试环境"""
        self.basedir = os.path.realpath(tempfile.mkdtemp(suffix='xbaydns_test'))
        basetest.BaseTestCase.setUp(self)
        self.nc=NamedConf()

    def tearDown(self):
        """清洁测试环境"""
        shutil.rmtree(self.basedir)
        basetest.BaseTestCase.tearDown(self)

    def test_addAcl(self):
        cmd = self.nc.addAcl('internal',['127.0.0.1',])
        self.assertEqual(cmd.strip(),'acl "internal" { 127.0.0.1; };')
    def test_delAcl(self):
        self.nc.addAcl('internal',['127.0.0.1',])
        self.assertTrue(self.nc.delAcl('internal'))
        self.assertFalse(self.nc.delAcl('home'))
    def test_addView(self):
        cmd = self.nc.addView('internal',['127.0.0.1',])
        self.assertEqual(cmd.strip(),'view "internal" { match-clients { 127.0.0.1; }; %s };')
        cmd = self.nc.addView('internal-tsig',tsig=['telcome',])
        self.assertEqual(cmd.strip(),'view "internal-tsig" { match-clients { key telcome; }; %s };')
    def test_updateView(self):
        cmd = self.nc.updateView('internal',['127.0.0.1',])
        self.assertEqual(cmd.strip(),'view "internal" { match-clients { 127.0.0.1; }; %s };')
    def test_loadViewKey(self):
        key = self.nc.loadViewKey('internal')
        self.assertEqual(base64.b64decode(key),"internal-key")
    def test_delView(self):
        self.nc.addView('internal',['127.0.0.1',])
        self.assertTrue(self.nc.delView('internal'))
        self.assertFalse(self.nc.delView('home'))
    def test_addDomain(self):
        cmd = self.nc.addDomain('internal',['sina.com.cn','mail.sina.com.cn'])
        self.assertEqual(cmd.replace("  ", "").replace("\n","").strip(),'''
                zone "sina.com.cn" {
                    type master;
                    file "internal.sina.com.cn.file";
                };
                zone "mail.sina.com.cn" {
                    type master;
                    file "internal.mail.sina.com.cn.file";
                };
                '''.replace("  ", "").replace("\n","").strip())
    def test_delDomain(self):
        self.nc.addDomain('internal',['sina.com.cn','mail.sina.com.cn'])
        self.assertTrue(self.nc.delDomain('internal','sina.com.cn'))
        self.assertFalse(self.nc.delDomain('home','a.sina.com.cn'))
    def test_save(self):
        self.nc.addAcl('internal',['127.0.0.1',])
        self.nc.addAcl('home',['127.0.0.1',])
        self.nc.addAcl('fx-subnet',['192.253.254/24',])
        self.nc.addView('internal',['fx-subnet',])
        self.nc.addDomain('internal',['sina.com.cn','mail.sina.com.cn'])
        self.nc.save(self.basedir)
        self.assertTrue(os.stat(os.path.join(self.basedir,'acl/internal.conf')))
        self.assertTrue(os.stat(os.path.join(self.basedir,'acl/home.conf')))
        self.assertTrue(os.stat(os.path.join(self.basedir,'acl/fx-subnet.conf')))
        self.assertTrue(os.stat(os.path.join(self.basedir,'view/internal.conf')))
        self.assertTrue(os.stat(os.path.join(self.basedir,'acl/acldef.conf')))
        self.assertTrue(os.stat(os.path.join(self.basedir,'dynamic/internal.sina.com.cn.file')))
        self.assertTrue(os.stat(os.path.join(self.basedir,'dynamic/internal.mail.sina.com.cn.file')))

def suite():
    """集合测试用例"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NamedConfTest, 'test'))
    return suite

"""
单独运行command的测试用例
"""
if __name__ == '__main__':
    unittest.main(defaultTest='suite')