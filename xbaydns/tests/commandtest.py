#!/usr/bin/env python
# encoding: utf-8
"""
commandtest.py

Created by 黄 冬 on 2007-11-19.
Copyright (c) 2007 XBayDNS Team. All rights reserved.

完成了command的用例测试，同时也是一个command使用的例程
"""

import unittest
import basetest
import logging.config

from xbaydns.utils import shtools

log = logging.getLogger('xbaydns.tests.commandtest')

"""
command的测试用例类
"""
class CommandTest(basetest.BaseTestCase):
	def setUp(self):
		basetest.BaseTestCase.setUp(self)

	def testExecute(self):
		returncode = shtools.execute("ls")
		self.assertTrue(returncode==0)

	def testExecuteError(self):
		returncode = shtools.execute("中华人民共和国")
		self.assertTrue(returncode>0)

"""
测试用例结合
"""
def suite():
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(CommandTest, 'test'))
	return suite

"""
单独运行command的测试用例
"""
if __name__ == '__main__':
	unittest.main(defaultTest='suite')
