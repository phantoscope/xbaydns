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
import unittest

log = logging.getLogger('xbaydns.tests.sysintergratetest')
logging.basicConfig(level=logging.DEBUG)


class SysIntergrateTest(basetest.BaseTestCase):

    def setUp(self):
        self.basedir = os.path.realpath(tempfile.mkdtemp(suffix='xbaydns_sys'))
        basetest.BaseTestCase.setUp(self)

    def tearDown(self):
        """清洁测试环境"""
        shutil.rmtree(self.basedir)
        basetest.BaseTestCase.tearDown(self)

    def _create_dir(self, *path):
        cur = self.basedir
        for part in path:
            cur = os.path.join(cur, part)
            os.mkdir(cur)
        return cur

    def init_conf(self):
        """为各种操作系统初始化named.conf,注意，这将清除系统中的原有文件。原有文件请提前备份。"""
        pass



def suite():
    """集合测试用例"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SysIntergrateTest, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main()