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
from xbaydns.dnsapi import nsupdate

log = logging.getLogger('xbaydnsweb.web.utils')
#logging.basicConfig(level=logging.DEBUG)

def record_nsupdate(record):
    try:
        nsupobj = nsupdate.NSUpdate('127.0.0.1',"%s."%record.domain,view="view_%s"%record.idc)
        #['foo', 3600, 'IN', 'A', ['192.168.1.1', '172.16.1.1']]#record style
        add_data=[[str(record.name),3600,'IN','A',record.ip],]
        try:
            record_a = nsupobj.queryRecord('%s.%s'%(record.name,record.domain), rdtype='A')
            print "record_a",record_a
            if len(record_a)!=0:
                del_data=[[record.name,3600,'IN','A',record_a],]
                nsupobj.removeRecord(del_data)
        except:
            print traceback.print_exc()
        print add_data
        nsupobj.addRecord(add_data)
        nsupobj.commitChanges()
    except:
        print traceback.print_exc()
        print "NSUpdate Error!"
    return None
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
    domain_matchs = map(lambda x:'%s'%x.domain,Record.objects.all())
    nc.addDomain(domain_matchs)
    nc.save(path)
    nc.reload()
    
    class My(object):pass
    for r in Record.objects.all():
        records=Record.objects.filter(name=r.name,domain=r.domain,idc=r.idc)
        m=My()
        m.name,m.domain=r.name,r.domain
        m.ip=map(lambda x:str(x.ip),records)
        m.idc=r.idc.alias
        print m.name,m.domain,m.idc,m.ip
        record_nsupdate(m)
    