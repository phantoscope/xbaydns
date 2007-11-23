# encoding: utf-8
"""
namedconftest.py

Created by yanxu on 2007-11-23.
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

from xbaydns.tools import namedconf

class InitConfTest(basetest.BaseTestCase):
	def setUp(self):
		"""初始化测试环境"""
		self.basedir = os.path.realpath(tempfile.mkdtemp(suffix='xbaydns_test'))
		basetest.BaseTestCase.setUp(self)

	def tearDown(self):
		"""清洁测试环境"""
		shutil.rmtree(self.basedir)
		basetest.BaseTestCase.tearDown(self)

	def test_addAcl(self):
		namedconf.addAcl('internal',['127.0.0.1',])

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