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

	def test_acl_file(self):
		"""测试acl_file调用"""
		acl_content = initconf.acl_file( dict(cnc=('192.168.1.1', '202.106.1.1')) )
		#log.debug("acl content is:" + acl_content)
		self.assertEqual(acl_content,'acl "cnc" { 192.168.1.1; 202.106.1.1; };\n')

	def test_muti_acl_file(self):
		"""test muti record acl acl_file"""
		acl_content = initconf.acl_file( dict(
			cnc=('1.1.1.1','2.2.2.2','3.3.3.3'),
			telcom=('4.4.4.4','5.5.5.5') ))
		self.assertEqual(acl_content,'acl "telcom" { 4.4.4.4; 5.5.5.5; };\nacl "cnc" { 1.1.1.1; 2.2.2.2; 3.3.3.3; };\n')

	def test_defaultzone_file(self):
		"""defaultzone_file test"""
		defaultzone = initconf.defaultzone_file()
		#log.debug(defaultzone)
		self.assertTrue( 'zone "." { type hint; file "named.root"; };' in defaultzone )

	def test_named_root_file(self):
		"""named_root_file test"""
		rootfile = initconf.named_root_file()
		self.assertTrue('A.ROOT-SERVERS.NET.      3600000      A' in rootfile )

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