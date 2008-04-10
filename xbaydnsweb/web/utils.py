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

def genRecordList(record):
    if record.record_type == 'A':
        return [[str(record.name),record.ttl,'IN','A',[str(record.record_info),]],]
    elif record.record_type == 'CNAME':
        return [[str(record.name),record.ttl,'IN','CNAME',[str(record.record_info),]],]
    elif record.record_type == 'NS':
        return [[str(record.name),record.ttl,'IN','NS',[str(record.record_info),]],]


def record_nsupdate(record):
    """调用NSUpdate更新record"""
    try:
        nsupobj = nsupdate.NSUpdate('127.0.0.1',"%s."%record.domain,view=record.viewname)
        #['foo', 3600, 'IN', 'A', ['192.168.1.1', '172.16.1.1']]#record style
        add_data=genRecordList(record)
        try:
            record_a = nsupobj.queryRecord('%s.%s'%(record.name,record.domain), rdtype=record.record_type)
            print "record_a",record_a
            if len(record_a)!=0:
                del_data=genRecordList(record)
                nsupobj.removeRecord(del_data)
        except:
            print traceback.print_exc()
            print "query error"
        print "add_data",add_data
        nsupobj.addRecord(add_data)
        nsupobj.commitChanges()
    except:
        print traceback.print_exc()
        print "NSUpdate Error!"
    print "NSUpdate OK"
    
def record_delete(record):
    try:
        nsupobj = nsupdate.NSUpdate('127.0.0.1',"%s."%record.domain,view=record.viewname)
        try:
            record_a = nsupobj.queryRecord('%s.%s'%(record.name,record.domain), rdtype=record.record_type)
            print "record_a",record_a
            if len(record_a)!=0:
                del_data=genRecordList(record)
                nsupobj.removeRecord(del_data)
        except:
            print traceback.print_exc()
            print "query error"
        nsupobj.commitChanges()
    except:
        print traceback.print_exc()

def genResult():
    """生成计算碎集所需要的数据结构"""
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
    
def getResults(ip):
    """将Result的结果按照域名合并汇总并返回"""
    records={}
    for result in Result.objects.filter(ip=ip):
        k="%s.%s"%(result.record.name,result.record.domain)
        if k not in records:
            records[k]=[]
        records[k].append([str(result.record.record_info),str(result.record.record_type.record_type)])
    return records

def updateDomain():
    """发出nsupdate请求,更新所有record和更新默认机房的记录"""
    class My(object):pass
    for view in IPArea.objects.all():
        ip=eval(view.ip)[0]
        records=getResults(ip)
        print "view,ip",view.view,ip
        for k,info in records.items():
            print "k,ips",k,info
            m=My()
            name=k.split('.')
            m.name,m.domain=name[0],'.'.join(name[1:])
            m.ip=info[0]
            m.recordtype=info[1]
            m.viewname=view.view
            print m.name,m.domain,m.viewname,m.ip
            record_nsupdate(m)
    """更新默认机房的记录"""
    for r in Record.objects.filter(is_defaultidc=True):
        m=My()
        m.name,m.domain=r.name,r.domain
        m.ip=[str(r.record_info),]
        m.viewname="view_default"
        print m.name,m.domain,m.viewname,m.ip
        record_nsupdate(m)

def genNamedConf(path):
    """生成所有named配置文件"""
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
    #domain_matchs = map(lambda x:'%s'%x.domain,Record.objects.all())
    domain_matchs = map(lambda x:'%s'%x.name,Domain.objects.all())
    nc.addDomain(domain_matchs)
    nc.save(path)
    nc.reload()
        
#保存所有配置,生成所有bind需要的配置文件
def saveAllConf(path=os.path.join(sysconf.chroot_path,sysconf.namedconf)):
    map(lambda x:x.delete(),IPArea.objects.all())
    genNamedConf(path)
    updateDomain()
    
