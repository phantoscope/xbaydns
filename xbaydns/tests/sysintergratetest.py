#!/usr/bin/env python
# encoding: utf-8
"""
sysintergratetest.py

Created by 黄 冬 on 2007-11-26.
Copyright (c) 2007 xBayDNS Team. All rights reserved.

这个测试是一个集成的系统测试。它从一个什么都不知道的环境开始进行测试。这里包括初始化环境，增加相关的配置，一步步的到齐全的环境。这里将会有很多的挑战，但是完成这个测试，
我们就完成了一个用户的典型操作过程。
"""

import basetest
import logging.config
import os
import shutil
import tempfile
import unittest

log = logging.getLogger('xbaydns.tests.sysintergratetest')
logging.basicConfig(level=logging.DEBUG)

from xbaydns.tools import initconf
from xbaydns.conf import sysconf

class SysIntergrate_ConfigInit_Test(basetest.BaseTestCase):

    def setUp(self):
        self.basedir = os.path.realpath(tempfile.mkdtemp(suffix='xbaydns_sys'))
        shutil.rmtree(os.path.join(sysconf.chroot_path,sysconf.namedconf,"acl"),ignore_errors=True)
        shutil.rmtree(os.path.join(sysconf.chroot_path,sysconf.namedconf,"master"),ignore_errors=True)
        shutil.rmtree(os.path.join(sysconf.chroot_path,sysconf.namedconf,"slave"),ignore_errors=True)
        shutil.rmtree(os.path.join(sysconf.chroot_path,sysconf.namedconf,"dynamic"),ignore_errors=True)
        basetest.BaseTestCase.setUp(self)

    def tearDown(self):
        """清洁测试环境"""
        shutil.rmtree(self.basedir)
        basetest.BaseTestCase.tearDown(self)

    def test_intergrate(self):
        """测试操作系统的named.conf初始化。
        为各种操作系统初始化named.conf,注意，这将清除系统中的原有文件。原有文件请提前备份。
        另一方面，请不要将本机的域名解晰放在127.0.0.1上，这样将会在测试失败时让你的机器也无法工作。"""
        initconf.main()
        self.assertTrue(os.path.isfile(os.path.join(sysconf.chroot_path,sysconf.namedconf,"named.conf")))
        self.assertTrue(os.path.isfile(os.path.join(sysconf.chroot_path,sysconf.namedconf,"defaultzone.conf")))
        self.assertTrue(os.path.isdir(os.path.join(sysconf.chroot_path,sysconf.namedconf,"acl")))
        self.assertTrue(os.path.isfile(os.path.join(sysconf.chroot_path,sysconf.namedconf,"acl","acldef.conf")))
        self.assertTrue(os.path.isdir(os.path.join(sysconf.chroot_path,sysconf.namedconf,"master")))
        self.assertTrue(os.path.isfile(os.path.join(sysconf.chroot_path,sysconf.namedconf,"master","empty.db")))
        self.assertTrue(os.path.isfile(os.path.join(sysconf.chroot_path,sysconf.namedconf,"master","localhost-forward.db")))
        self.assertTrue(os.path.isfile(os.path.join(sysconf.chroot_path,sysconf.namedconf,"master","localhost-reverse.db")))
        self.assertTrue(os.path.isdir(os.path.join(sysconf.chroot_path,sysconf.namedconf,"slave")))
        self.assertTrue(os.path.isdir(os.path.join(sysconf.chroot_path,sysconf.namedconf,"dynamic")))

def suite():
    """集合测试用例"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SysIntergrate_ConfigInit_Test, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main()