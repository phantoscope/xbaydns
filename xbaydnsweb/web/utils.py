#!/usr/bin/env python
# encoding: utf-8
"""
utils.py

Created by QingFeng on 2007-12-02.
Copyright (c) 2007 yanxu. All rights reserved.
"""
import logging.config
from xbaydnsweb.web.models import *
from xbaydns.dnsapi.namedconf import *
from xbaydns.conf import sysconf

log = logging.getLogger('xbaydnsweb.web.utils')
#logging.basicConfig(level=logging.DEBUG)

def saveAllConf(path=sysconf.namedconf):
    nc = NamedConf()
    #将分组来源IP追加到一个ACL
    allip={}
    for result in Result.objects.all():
        k=result.idc.alias
        if k not in allip:
            allip[k]=[]
        allip[k].append(result.ip)
    print "allip",allip
    for idc in allip.keys():
        aclname='acl_%s'%idc
        print "aclname",aclname
        nc.addAcl(aclname,allip[idc])
        #每个View对应一种ACL
        nc.addView('view_%s'%idc,[aclname,])
    #追加所有的Domain
    domain_matchs = map(lambda x:'%s.%s'%(x.name,x.domain),Record.objects.all())
    nc.addDomain(domain_matchs)
    nc.save(path)

# def saveAllConf(path=sysconf.namedconf):
#     nc = NamedConf()
#     for acl in Acl.objects.all():
#         matchs=map(lambda x:x.aclMatch,
#                 AclMatch.objects.filter(acl=acl))
#         nc.addAcl(acl.aclName,matchs)
#     for view in View.objects.all():
#         view_matchs=[]
#         for aclmatch in view.aclmatch.all():
#             view_matchs.append(aclmatch.acl.aclName)
#         nc.addView(view.viewName,view_matchs)
#     domain_matchs = map(lambda x:x.zone,Domain.objects.all())
#     nc.addDomain(domain_matchs)
#     nc.save(path)
