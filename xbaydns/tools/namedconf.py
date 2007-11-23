# encoding: utf-8
"""
namedconf.py

Created by QingFeng on 2007-11-22.
Copyright (c) 2007 yanxu. All rights reserved.
"""

import logging.config
import os

log = logging.getLogger('xbaydns.tests.namedconftest')
logging.basicConfig(level=logging.DEBUG)

class NamedConf(object):
	def __init__(self):
		self.path='acl/'
		self.fname='acldef.conf'
	'''
	add acl (acl,aclmatch) 增加一个acl 
	参数说明： 
	acl 要增加的acl的名称 
	aclmatech 增加的acl中的match地址
	'''
	def addAcl(self,acl,aclmatch):
		return '''
			acl "%s" { %s; };
		'''%(acl,';'.join(aclmatch))
		
	'''
	del acl(acl) 删除一个acl 

	参数说明： 
	acl 要删除的acl的名称
	'''
	def delAcl(self,acl):
		'''去除include文字'''
		fname=os.path.join(self.path,acl+'.conf')
		return 'include "%s";'%fname
	
	'''
	add view(view,match-client) 

	增加view 

	参数说明： 
	view 增加的view的名称 
	match-client 匹配于该view的acl汇总
	'''
	def addView(self,view,matchClient):
		return '''
			view "%s" { match-clients { %s; }; };
		'''%(view,';'.join(matchClient))
	
	'''
	update view(view,match-client) 更新view 

	参数说明： 
	view 增加的view的名称 
	match-client 匹配于该view的acl汇总
	'''
	def updateView(self,view,matchClient):
		pass
	
	'''
	del view(view) 删除view 

	参数说明： 
	view 增加的view的名称
	'''
	def delView(self,view):
		pass
		
	def save(self):
		pass
