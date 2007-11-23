# encoding: utf-8
"""
namedconf.py

Created by yanxu on 2007-11-22.
Copyright (c) 2007 yanxu. All rights reserved.
"""

import logging.config
import cPickle as pickle

log = logging.getLogger('xbaydns.tests.namedconftest')
logging.basicConfig(level=logging.DEBUG)

aclConf={}
def loadAclConf(func):
	try:
		aclConf=pickle.load(open('/tmp/aclconf.pickle'))
	except:
		pass
	return func

@loadAclConf
def addAcl(acl,aclmatch):
	return '''
		acl "%s" { %s; };
		'''%(acl,';'.join(aclmatch))

def delAcl(acl):
	pass
	
def addView(view,matchClient):
	pass
	
def updateView(view,matchClient):
	pass

def delView(view):
	pass
