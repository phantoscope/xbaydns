#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

Created by QingFeng on 2007-11-28.
Copyright (c) 2007 yanxu. All rights reserved.
"""

#import basetest
import logging.config
import shutil
import tempfile
import time
import unittest
import base64

log = logging.getLogger('xbaydnsweb.web.tests')
logging.basicConfig(level=logging.DEBUG)

from django.test.utils import *
from django.test import TestCase
from django.conf import settings
from xbaydnsweb.web.models import *

class ModelsTest(TestCase):
    def setUp(self):
        """初始化测试环境"""
        self.acl1=Acl.objects.create(aclName='internal')
        self.view1=View.objects.create(viewName='home')
        
    def tearDown(self):
        """清洁测试环境"""
        pass

    def test_Acl(self):
        self.assertEquals(str(self.acl1), 'internal')
    def test_View(self):
        self.assertEquals(str(self.view1), 'home')
        
def suite():
    """集合测试用例"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ModelsTest, 'test'))
    return suite

"""
单独运行command的测试用例
"""
if __name__ == '__main__':
    unittest.main(defaultTest='suite')    