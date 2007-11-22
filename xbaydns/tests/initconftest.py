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
import time
import unittest

log = logging.getLogger('xbaydns.tests.initconftest')
logging.basicConfig(level=logging.DEBUG)

from xbaydns.tools import initconf

class InitConfTest(basetest.BaseTestCase):
	def setUp(self):
		"""初始化测试环境"""
		self.basedir = os.path.realpath(tempfile.mkdtemp(suffix='xbaydns_test'))
		basetest.BaseTestCase.setUp(self)

	def tearDown(self):
		"""清洁测试环境"""
		shutil.rmtree(self.basedir)
		basetest.BaseTestCase.tearDown(self)

	def test_acl_file(self):
		"""测试acl_file调用"""
		acl_content = initconf.acl_file( dict(cnc=('192.168.1.1', '202.106.1.1')) )
		#log.debug("acl content is:" + acl_content)
		self.assertEqual(acl_content,'acl "cnc" { 192.168.1.1; 202.106.1.1; };\n')

	def _create_dir(self, *path):
		cur = self.basedir
		for part in path:
			cur = os.path.join(cur, part)
			os.mkdir(cur)
		return cur[len(self.basedir) + 1:]

	def _create_file(self, *path):
		filename = os.path.join(self.basedir, *path)
		fd = file(filename, 'w')
		fd.close()
		return filename[len(self.basedir) + 1:]

	def test_muti_acl_file(self):
		"""test muti record acl acl_file"""
		acl_content = initconf.acl_file( dict(
			cnc=('1.1.1.1','2.2.2.2','3.3.3.3'),
			telcom=('4.4.4.4','5.5.5.5') ))
		self.assertEqual(acl_content,'acl "telcom" { 4.4.4.4; 5.5.5.5; };\nacl "cnc" { 1.1.1.1; 2.2.2.2; 3.3.3.3; };\n')

	def test_defaultzone_file(self):
		"""defaultzone_file test"""
		defaultzone = initconf.defaultzone_file()
		#log.debug("defaultzone is:%s"%defaultzone)
		self.assertTrue( 'zone "." { type hint; file "named.root"; };' in defaultzone )
	
	def test_error_default_file(self):
		curset = initconf.TMPL_DEFAULTZONE
		initconf.TMPL_DEFAULTZONE = "中华人民共和国"
		returncode = initconf.defaultzone_file()
		initconf.TMPL_DEFAULTZONE = curset
		self.assertFalse( returncode )

	def test_named_root_file(self):
		"""named_root_file test"""
		rootfile = initconf.named_root_file()
		self.assertTrue('A.ROOT-SERVERS.NET.      3600000      A' in rootfile )

	def test_error_named_root_file(self):
		curset = initconf.TMPL_NAMEDROOT
		initconf.TMPL_NAMEDROOT = "中华人民共和国"
		returncode =  initconf.named_root_file()
		initconf.TMPL_NAMEDROOT = curset
		self.assertFalse(returncode)

	def test_backup_conf(self):
		"""backup_conf test"""
		tmpdir = self._create_dir("namedb")
		self.assertTrue( initconf.backup_conf(self.basedir,"") )
		filename = "namedconf_%s.tar.bz2"%(time.strftime("%y%m%d%H%M"))
		log.debug("backup file is:%s"%(os.path.join(self.basedir,filename)))
		self.assertTrue( os.path.isfile(os.path.join(self.basedir,filename)) )

	def test_create_destdir(self):
		"""create_destdir test"""
		tmpdir = initconf.create_destdir()
		log.debug("create tmpdir is:%s"%tmpdir)
		self.assertTrue( os.path.isdir("%s/namedb/acl"%tmpdir) )
		self.assertTrue( os.path.isdir("%s/namedb/dynamic"%tmpdir) )
		self.assertTrue( os.path.isdir("%s/namedb/master"%tmpdir) )
		self.assertTrue( os.path.isdir("%s/namedb/slave"%tmpdir) )
		shutil.rmtree(tmpdir)

	def test_create_conf(self):
		"""create_conf test"""
		tmpdir = initconf.create_destdir()
		self.assertTrue( initconf.create_conf(tmpdir) )

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