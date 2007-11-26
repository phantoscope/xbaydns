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
		self.assertEqual(cmd.strip(),'acl "internal" { 127.0.0.1; };')
	def test_delAcl(self):
		self.nc.addAcl('internal',['127.0.0.1',])
		self.assertTrue(self.nc.delAcl('internal'))
		self.assertFalse(self.nc.delAcl('home'))
	def test_addView(self):
		cmd = self.nc.addView('internal',['127.0.0.1',])
		self.assertEqual(cmd.strip(),'view "internal" { match-clients { 127.0.0.1; }; };')
		cmd = self.nc.addView('internal-tsig',tsig=['telcome',])
		self.assertEqual(cmd.strip(),'view "internal-tsig" { match-clients { key telcome; }; };')
	def test_updateView(self):
		cmd = self.nc.updateView('internal',['127.0.0.1',])
		self.assertEqual(cmd.strip(),'view "internal" { match-clients { 127.0.0.1; }; };')
	def test_delView(self):
		self.nc.addView('internal',['127.0.0.1',])
		self.assertTrue(self.nc.delView('internal'))
		self.assertFalse(self.nc.delView('home'))
	def test_save(self):
		self.nc.addAcl('internal',['127.0.0.1',])
		self.nc.addAcl('home',['127.0.0.1',])
		self.nc.addAcl('fx-subnet',['192.253.254/24',])
		self.nc.addView('internal',['fx-subnet',])
		self.nc.save(self.basedir)
		self.assertTrue(os.stat(os.path.join(self.basedir,'acl/internal.conf')))
		self.assertTrue(os.stat(os.path.join(self.basedir,'acl/home.conf')))
		self.assertTrue(os.stat(os.path.join(self.basedir,'acl/fx-subnet.conf')))
		self.assertTrue(os.stat(os.path.join(self.basedir,'view/internal.conf')))
		self.assertTrue(os.stat(os.path.join(self.basedir,'acl/acldef.conf')))

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