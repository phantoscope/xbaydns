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
    rtstr = record.record_type.record_type
    if rtstr == 'A':
        return [[str(record.name),record.ttl,'IN','A',[str(record.record_info),]],]
    elif rtstr == 'CNAME':
        return [[str(record.name),record.ttl,'IN','CNAME',[str(record.record_info),]],]
    elif rtstr == 'NS':
        return [[str(record.name),record.ttl,'IN','NS',[str(record.record_info),]],]


def record_nsupdate(record):
    """调用NSUpdate更新record"""
    try:
        nsupobj = nsupdate.NSUpdate('127.0.0.1',"%s."%record.domain,view=record.viewname)
        #['foo', 3600, 'IN', 'A', ['192.168.1.1', '172.16.1.1']]#record style
        add_data=genRecordList(record)
        try:
            record_a = nsupobj.queryRecord('%s.%s'%(record.name,record.domain), rdtype=record.record_type.record_type)
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
            record_a = nsupobj.queryRecord('%s.%s'%(record.name,record.domain), rdtype=record.record_type.record_type)
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

def getRecords(iparea):
    """将Result的结果按照域名合并汇总并返回"""
    records=[]
    for domain_name,idc_alias in list(iparea.service_route):
        records.append(Record.objects.filter(name=domain_name,idc__alias=idc_alias))
    return records

def updateDomain():
    """发出nsupdate请求,更新所有record和更新默认机房的记录"""
    for iparea in IPArea.objects.all():
        records=getRecords(view)
        for record in records:
            print "record ",record
            record.viewname=view.view
            print record.name,record.domain,record.viewname
            record_nsupdate(record)
    """更新默认机房的记录"""
    for record in Record.objects.filter(is_defaultidc=True):
        record.viewname="view_default"
        print record.name,record.domain,record.viewname
        record_nsupdate(record)

def genNamedConf(path):
    """生成所有named配置文件"""
    nc = NamedConf()
    ipareas = IPArea.objects.all()
    if result!=1:
        for i,iparea in enumerate(ipareas):
            aclname='acl_acl%s'%i
            print "aclname",aclname
            ipareas.acl = aclname
            nc.addAcl(aclname,list(ipare.ip))
            #每个View对应一种ACL
            viewname='view_view%s'%i
            nc.addView(viewname,[aclname,])
            ipareas.view = viewname
            ipareas.save()
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
    genNamedConf(path)
    updateDomain()
   
def update_allow_transfer(slaveip, path=os.path.join(sysconf.chroot_path,sysconf.namedconf)):

    named_conf_path = os.path.join(path, "named.conf")
    named_conf_string = open(named_conf_path, 'r').read()
    
    p = re.compile('allow-transfer\s*{ (?P<allows> [^}]* ) }', re.VERBOSE)
    l = p.findall(named_conf_string)
    if len(l) == 0:
        return False
 
    allows=[]
    for ip in l[0].split(';'):
        cip = ip.strip()
        if len(cip) == 0 or cip == 'none':
            pass
        else:
            allows.append(cip)

    if ip in allows:
        return True

    allows.append(slaveip)
    allows.append('')
    allow_list = 'allow-transfer{ %s }' % '; '.join(allows)

    s = p.sub(allow_list, named_conf_string)
    open(named_conf_path, 'w').write(s)

    nc = NamedConf()
    nc.reload()
    return True