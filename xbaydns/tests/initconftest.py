#!/usr/bin/env python
# encoding: utf-8
"""
initconftest.py

Created by 黄 冬 on 2007-11-19.
Copyright (c) 2007 __MyCompanyName__. All rights reserved.
"""

import basetest
import logging.config
import os
import shutil
import tempfile
import unittest

from xbaydns.tools import initconf

log = logging.getLogger('xbaydns.tests.initconftest')
logging.basicConfig(level=logging.DEBUG)

class InitConfTest(basetest.BaseTestCase):
	"""
	对初始化配置
	"""
	def setUp(self):
		self.basedir = os.path.realpath(tempfile.mkdtemp(suffix='xbaydns_test'))
		basetest.BaseTestCase.setUp(self)

	def tearDown(self):
		shutil.rmtree(self.basedir)
		basetest.BaseTestCase.tearDown(self)

	def test_create_dir(self):
		"""测试目录创建create_dir"""
		createdir = initconf.create_dir(self.basedir + "/tmp_create")
		log.debug("createdir is:" + createdir[len(self.basedir)+1:])
		self.assertEqual(createdir[len(self.basedir)+1:],"tmp_create")


"""
测试用例结合
"""
def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(InitConfTest, 'test'))
	return suite

"""
单独运行command的测试用例
"""
if __name__ == '__main__':
	unittest.main(defaultTest='suite')