# 代码书写 #
## 目录 ##
测试用例代码应该放在/xbaydns/tests目录中。测试文件命名为xxxxtest.py。
## 代码 ##
所有的测试用例均需要import basetest，我们的测试类均为basetest.BaseTestCase的子类。在setUp和tearDown中要执行父类的相应方法。如下代码为例：
```
import basetest
import logging.config
import os
import shutil
import tempfile
import time
import unittest

from xbaydns.tools import initconf

log = logging.getLogger('xbaydns.tests.initconftest')
logging.basicConfig(level=logging.DEBUG)

class InitConfTest(basetest.BaseTestCase):
	def setUp(self):
		"""初始化测试环境"""
		self.basedir = os.path.realpath(tempfile.mkdtemp(suffix='xbaydns_test'))
		basetest.BaseTestCase.setUp(self)

	def tearDown(self):
		"""清洁测试环境"""
		shutil.rmtree(self.basedir)
		basetest.BaseTestCase.tearDown(self)
```

# Django unittest #
在相应app目录下建立一个tests.py,在里面写我们的测试用例
代码例子:
```
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
        
    def tearDown(self):
        """清洁测试环境"""
        pass

    def test_Acl(self):
        self.assertEquals(str(self.acl1), 'internal')
        
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
```
关于django测试,更多见这里
http://www.djangoproject.com/documentation/0.96/testing/

一个用于测试django合页面是否可以正确访问的工具

http://www.mysoftparade.com/blog/django-profile-sql-performance/


# 执行测试 #
## 单独执行 ##
可以到tests目录中自己执行，如：
```
# sudo python initconftest.py
```
## 全部测试用例的执行 ##
使用setup.py进行测试：
```
# sudo python setup.py test
```

# 系统集成测试环境初始化说明 #
## osx测试环境初始化 ##

# 集成测试服务器的建立 #
由于xbaydns的服务器是google code提供的，但是它除了wiki、svn之外并没有提供集成测试环境，所以xbaydns为了做每日甚至是每个版本在各种操作系统平台、操作系统版本、bind版本上的持续集成，使用了基于trac、bitten的集成测试服务器。

在这里，我们说明如何快速搭建出一个本地的集成测试服务器。这个集成测试服务器基于FreeBSD 7.0，其它的操作系统安装也不应该很困难，如果有人有相应的心得也请放到这页wiki中来。

## 在FreeBSD中建立集成测试服务器 ##
### 安装apche 2.2 ###
它需要apache做为web服务器，所以我们首先需要安装apache2.2：
```
cd /usr/ports/www/apache22
sudo make WITH_AUTH_MODULES=yes WITH_DAV_MODULES=yes WITH_SSL_MODULES=yes WITH_LDAP_MODULES=yes WITH_BERKELEYDB=db42 install clean
```
### 安装Subversion ###
为了从google code sync svn的库，我们需要subversion：
```
cd /usr/ports/devel/subversion 
sudo make WITH_MOD_DAV_SVN=yes WITH_APACHE2_APR=yes WITH_PYTHON=yes WITH_ASVN=yes install clean
```
### 安装mod\_python3 ###
mod\_python是跑trac所需要的，我们会使用mod\_python来运行trac：
```
cd /usr/ports/www/mod_python3
sudo make install clean
```
### 安装trac ###
trac的安装还是很简单的：
```
cd /usr/ports/www/trac 
sudo make install clean
```
安装时选择上SILVERCITY、DOCUTILS和SUBVERSION。
### 安装trac的插件 ###
#### trac-webadmin ####
webadmin是需要的东东哟 :)
```
cd /usr/ports/www/trac-webadmin 
sudo make install clean
```
#### trac-webadmin ####

### 初始化trac项目 ###