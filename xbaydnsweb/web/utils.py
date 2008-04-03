#!/opt/local/bin/python2.5
# encoding: utf-8
"""
utils.py

Created by QingFeng on 2007-12-02.
Copyright (c) 2007 yanxu. All rights reserved.
"""
from django.core.management import setup_environ
from xbaydnsweb import settings
setup_environ(settings)

import logging.config
from xbaydnsweb.web.models import *
from xbaydns.dnsapi.namedconf import *
from xbaydns.conf import sysconf
from xbaydns.dnsapi import nsupdate
from xbaydns.tools import algorithms

log = logging.getLogger('xbaydnsweb.web.utils')
#logging.basicConfig(level=logging.DEBUG)

def record_nsupdate(record):
    try:
        nsupobj = nsupdate.NSUpdate('127.0.0.1',"%s."%record.domain,view=record.viewname)
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

def genResult():
    result,ips={},[]
    for record in Record.objects.all():
        for r in Result.objects.filter(record=record):
            k='%s.%s'%(record.name,record.domain)
            if k not in result:
                result[k]={}
            idc=str(record.idc)
            if idc not in result[k]:
                result[k][idc]=[]
            result[k][idc].append(str(r.ip))
    for domain,idcs in result.items():
        print domain
        domainip=[]
        for idc,ip in idcs.items():
            print idc,ip
            domainip.append( list(set(ip)) )
        ips.append( domainip )
    return algorithms.ecintersection(*ips)

def saveAllConf(path=sysconf.namedconf):
    map(lambda x:x.delete(),IPArea.objects.all())
    nc = NamedConf()
    result=genResult()
    if result!=1:
        for i,ips in enumerate(result):
            aclname='acl_acl%s'%i
            print "aclname",aclname
            nc.addAcl(aclname,list(ips))
            #每个View对应一种ACL
            viewname='view_view%s'%i
            nc.addView(viewname,[aclname,])
            IPArea.objects.create(ip=str(list(ips)),acl=aclname,view=viewname)
    #增加any的ACL和View
    nc.addAcl('acl_default',['any',])
    nc.addView('view_default',['any',])
    #追加所有的Domain
    domain_matchs = map(lambda x:'%s'%x.domain,Record.objects.all())
    nc.addDomain(domain_matchs)
    nc.save(path)
    nc.reload()
    
    class My(object):pass
    for r in Record.objects.all():
        for viewname in IPArea.objects.values('view').distinct():
            records=Record.objects.filter(name=r.name,domain=r.domain,idc=r.idc)
            m=My()
            m.name,m.domain=r.name,r.domain
            m.ip=map(lambda x:str(x.ip),records)
            m.viewname=viewname
            print m.name,m.domain,m.viewname,m.ip
            record_nsupdate(m)
