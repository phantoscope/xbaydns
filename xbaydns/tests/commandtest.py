#!/usr/bin/env python
# encoding: utf-8
"""
commandtest.py

Created by 黄 冬 on 2007-11-19.
Copyright (c) 2007 XBayDNS Team. All rights reserved.

完成了command的用例测试，同时也是一个command使用的例程
"""

import basetest
import os
import shutil
import sys
import tempfile
import unittest
import logging.config

from xbaydns.utils import shtools
from xbaydns.utils.command import CommandLine,_combine,TimeoutError
log = logging.getLogger('xbaydns.tests.commandtest')

"""
command的测试用例类
"""
class CommandTest(basetest.BaseTestCase):
	def setUp(self):
		self.basedir = os.path.realpath(tempfile.mkdtemp(suffix='xbaydns_test'))
		basetest.BaseTestCase.setUp(self)

	def tearDown(self):
		shutil.rmtree(self.basedir)
		basetest.BaseTestCase.tearDown(self)

	def _create_file(self, name, content=None):
		filename = os.path.join(self.basedir, name)
		fd = file(filename, 'w')
		if content:
		    fd.write(content)
		fd.close()
		return filename

	def testExecute(self):
		returncode = shtools.execute("ls")
		self.assertTrue(returncode==0)

	def testExecuteError(self):
		returncode = shtools.execute("中华人民共和国")
		self.assertTrue(returncode>0)

	def test_extract_lines(self):
		cmdline = CommandLine('test', [])
		data = ['foo\n', 'bar\n']
		lines = cmdline._extract_lines(data)
		self.assertEqual(['foo', 'bar'], lines)
		self.assertEqual([], data)

	def test_extract_lines_spanned(self):
		cmdline = CommandLine('test', [])
		data = ['foo ', 'bar\n']
		lines = cmdline._extract_lines(data)
		self.assertEqual(['foo bar'], lines)
		self.assertEqual([], data)

	def test_extract_lines_trailing(self):
		cmdline = CommandLine('test', [])
		data = ['foo\n', 'bar']
		lines = cmdline._extract_lines(data)
		self.assertEqual(['foo'], lines)
		self.assertEqual(['bar'], data)

	def test_combine(self):
		list1 = ['foo', 'bar']
		list2 = ['baz']
		combined = list(_combine(list1, list2))
		self.assertEqual([('foo', 'baz'), ('bar', None)], combined)

	def test_single_argument(self):
		cmdline = CommandLine('python', ['-V'])
		stdout = []
		stderr = []
		for out, err in cmdline.execute(timeout=5.0):
			if out is not None:
				stdout.append(out)
			if err is not None:
				stderr.append(err)
		py_version = '.'.join([str(v) for (v) in sys.version_info[:3]])
		self.assertEqual(['Python %s' % py_version], stderr)
		self.assertEqual([], stdout)
		self.assertEqual(0, cmdline.returncode)

	def test_multiple_arguments(self):
		script_file = self._create_file('test.py', content="""
import sys
for arg in sys.argv[1:]:
	print arg
""")
		cmdline = CommandLine('python', [script_file, 'foo', 'bar', 'baz'])
		stdout = []
		stderr = []
		for out, err in cmdline.execute(timeout=5.0):
			stdout.append(out)
			stderr.append(err)
		py_version = '.'.join([str(v) for (v) in sys.version_info[:3]])
		self.assertEqual(['foo', 'bar', 'baz'], stdout)
		self.assertEqual([None, None, None], stderr)
		self.assertEqual(0, cmdline.returncode)

	def test_output_error_streams(self):
		script_file = self._create_file('test.py', content="""
import sys, time
print>>sys.stdout, 'Hello'
print>>sys.stdout, 'world!'
sys.stdout.flush()
time.sleep(.1)
print>>sys.stderr, 'Oops'
sys.stderr.flush()
""")
		cmdline = CommandLine('python', [script_file])
		stdout = []
		stderr = []
		for out, err in cmdline.execute(timeout=5.0):
			stdout.append(out)
			stderr.append(err)
		py_version = '.'.join([str(v) for (v) in sys.version_info[:3]])
		self.assertEqual(['Hello', 'world!', None], stdout)
		self.assertEqual([None, None, 'Oops'], stderr)
		self.assertEqual(0, cmdline.returncode)

	def test_input_stream_as_fileobj(self):
		script_file = self._create_file('test.py', content="""
import sys
data = sys.stdin.read()
if data == 'abcd':
	print>>sys.stdout, 'Thanks'
""")
		input_file = self._create_file('input.txt', content='abcd')
		input_fileobj = file(input_file, 'r')
		try:
			cmdline = CommandLine('python', [script_file], input=input_fileobj)
			stdout = []
			stderr = []
			for out, err in cmdline.execute(timeout=5.0):
				stdout.append(out)
				stderr.append(err)
			py_version = '.'.join([str(v) for (v) in sys.version_info[:3]])
			self.assertEqual(['Thanks'], stdout)
			self.assertEqual([None], stderr)
			self.assertEqual(0, cmdline.returncode)
		finally:
			input_fileobj.close()

	def test_input_stream_as_string(self):
		script_file = self._create_file('test.py', content="""
import sys
data = sys.stdin.read()
if data == 'abcd':
	print>>sys.stdout, 'Thanks'
""")
		cmdline = CommandLine('python', [script_file], input='abcd')
		stdout = []
		stderr = []
		for out, err in cmdline.execute(timeout=5.0):
			stdout.append(out)
			stderr.append(err)
		py_version = '.'.join([str(v) for (v) in sys.version_info[:3]])
		self.assertEqual(['Thanks'], stdout)
		self.assertEqual([None], stderr)
		self.assertEqual(0, cmdline.returncode)

	def test_timeout(self):
		script_file = self._create_file('test.py', content="""
import time
time.sleep(2.0)
print 'Done'
""")
		cmdline = CommandLine('python', [script_file])
		iterable = iter(cmdline.execute(timeout=.5))
		self.assertRaises(TimeoutError, iterable.next)


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
