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

log = logging.getLogger('xbaydns.tests.namedconftest')
logging.basicConfig(level=logging.DEBUG)

from xbaydns.tools.namedconf import *

class InitConfTest(basetest.BaseTestCase):
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
		self.assertTrue(cmd,'acl {127.0.0.1;}')
	def test_delAcl(self):
		cmd=self.nc.delAcl('internal')
		self.assertTrue(cmd,'include "acl/internal.conf";')

def suite():
	"""集合测试用例"""
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(InitConfTest, 'test'))
	return suite

"""
单独运行command的测试用例
"""
if __name__ == '__main__':
	unittest.main(defaultTest='suite')