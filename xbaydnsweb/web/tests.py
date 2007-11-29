#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

Created by QingFeng on 2007-11-28.
Copyright (c) 2007 yanxu. All rights reserved.
"""

import xbaydns.tests.basetest as basetest
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

class ModelsTest(basetest.BaseTestCase,TestCase):
    def setUp(self):
        """初始化测试环境"""
        self.basedir = os.path.realpath(tempfile.mkdtemp(suffix='xbaydns_test'))
        basetest.BaseTestCase.setUp(self)
        
        self.acl1=Acl.objects.create(aclName='internal')
        self.aclM1=AclMatch.objects.create(acl=self.acl1,aclMatch='127.0.0.1')
        
        self.acl2=Acl.objects.create(aclName='home1')
        self.aclM2=AclMatch.objects.create(acl=self.acl2,aclMatch='10.10.10.10')
        
        self.acl3=Acl.objects.create(aclName='home2')
        self.aclM3=AclMatch.objects.create(acl=self.acl3,aclMatch='10.10.10.1')
        self.aclM4=AclMatch.objects.create(acl=self.acl3,aclMatch='10.10.10.2')
        
        self.view1=View.objects.create(viewName='home')
        
    def tearDown(self):
        """清洁测试环境"""
        #shutil.rmtree(self.basedir)
        basetest.BaseTestCase.tearDown(self)

    def test_Acl(self):
        self.assertEquals(str(self.acl1), 'internal')
    def test_View(self):
        self.assertEquals(str(self.view1), 'home')
    def test_saveToFile(self):
        self.acl1.saveConf(self.basedir)
        Acl.saveAllConf(self.basedir)
        self.assertTrue(os.stat(os.path.join(self.basedir,'acl/internal.conf')))
        self.assertTrue(os.stat(os.path.join(self.basedir,'acl/home1.conf')))
        self.assertTrue(os.stat(os.path.join(self.basedir,'acl/home2.conf')))
        
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