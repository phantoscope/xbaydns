# encoding: utf-8
"""
namedconf.py

Created by QingFeng on 2007-11-22.
Copyright (c) 2007 yanxu. All rights reserved.
"""

import logging.config
import os,tempfile
from xbaydns.conf import sysconf

log = logging.getLogger('xbaydns.tests.namedconftest')
logging.basicConfig(level=logging.DEBUG)

def pathIsExists(func):
	def wrapper(*args):
		path=args[1]
		try:
			acl_path=os.path.join(path,'acl/')
			print os.stat(acl_path)
		except OSError:
			os.mkdir(acl_path)
		try:
			view_path=os.path.join(path,'view/')
			print os.stat(view_path)
		except OSError:
			os.mkdir(view_path)
		func(args[0],args[1])
	return wrapper
	
class NamedConf(object):
	def __init__(self):
		self.acls={}
		self.views={}
		self.acl_include=[]
	'''
	add acl (acl,aclmatch) 增加一个acl 
	参数说明： 
	acl 要增加的acl的名称 
	aclmatech 增加的acl中的match地址
	'''
	def addAcl(self,acl,aclmatch):
		s='''
			acl "%s" { %s; };
		'''%(acl,';'.join(aclmatch))
		self.acls[acl]=s
		return s
		
	'''
	del acl(acl) 删除一个acl 

	参数说明： 
	acl 要删除的acl的名称
	'''
	def delAcl(self,acl):
		if acl in self.acls:
			del self.acls[acl]
			return True
		return False
	
	'''
	add view(view,match-client) 

	增加view 

	参数说明： 
	view 增加的view的名称 
	match-client 匹配于该view的acl汇总
	'''
	def addView(self,view,matchClient=[],tsig=[]):
		tsig=map(lambda x:'key %s'%x,tsig)
		s='''view "%s" { match-clients { %s; }; };
		'''%(view,';'.join(matchClient+tsig))
		self.views[view]=s
		return s
	
	'''
	update view(view,match-client) 更新view 

	参数说明： 
	view 增加的view的名称 
	match-client 匹配于该view的acl汇总
	'''
	def updateView(self,view,matchClient=[],tsig=[]):
		return self.addView(view,matchClient,tsig)
	
	'''
	del view(view) 删除view 

	参数说明： 
	view 增加的view的名称
	'''
	def delView(self,view):
		if view in self.views:
			del self.views[view]
			return True
		return False
	
	'''
	用于校验生成出的配置文件
	'''
	def __checkfile(self):
		pass
		
	'''
	cp正确的文件到指定位置
	'''
	def __cpfile(self):
		pass
	
	'''
	保存所有acl配置文件
	'''
	@pathIsExists
	def __saveAcls(self,path=sysconf.namedconf):
		for k,v in self.acls.items():
			fname=os.path.join('acl/',k+'.conf')
			pathname=os.path.join(path,fname)
			self.acl_include.append('include "%s";'%fname)
			open(pathname,'w').write(v)
		
	'''
	保存所有view配置文件
	'''
	@pathIsExists
	def __saveViews(self,path=sysconf.namedconf):
		for k,v in self.views.items():
			fname=os.path.join('view/',k+'.conf')
			pathname=os.path.join(path,fname)
			self.acl_include.append('include "%s";'%fname)
			open(pathname,'w').write(v)
	
	'''
	保存acldef.conf文件,保存所有生成的include语句
	'''
	@pathIsExists
	def __saveAcldef(self,path):
		acl_file=os.path.join(
				path,sysconf.filename_map['acl'])
		open(acl_file,'w').write('\n'.join(self.acl_include))
	'''
	保存acl和views的配置文件
	'''	
	def save(self,path=sysconf.namedconf):
		self.__saveAcls(path)
		self.__saveViews(path)
		self.__saveAcldef(path)
