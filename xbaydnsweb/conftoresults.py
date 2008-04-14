#!/opt/local/bin/python2.5
# encoding: utf-8
"""
conftoresults.py

Created by QingFeng on 2008-03-26.
Copyright (c) 2008 xBayDNS Team. All rights reserved.
"""
import os,sys
import traceback
from operator import itemgetter

def getServiceRegions():
    from django.db import connection
    service_reg={}
    sql='''SELECT web_record.name,web_domain.name,web_idc.alias FROM web_record,web_domain,web_idc WHERE web_domain.id=web_record.domain_id AND web_idc.id=web_record.idc_id GROUP BY web_record.name,web_domain.name,web_idc.alias'''
    cursor = connection.cursor()
    cursor.execute(sql)
    for r in cursor.fetchall():
        key = r[0].join(r[1])
        service_reg.setdefault(key,[])
        if key in service_reg:
            service_reg[key].append(r[2])
        else:
            service_reg.setdefault(r[0].join(r[1]),r[2])

def findFastSpeed(agents,times):
    times=map(lambda x:float(x.strip()),times)
    if reduce(lambda x,y:x==y, times):return []
    values=dict(zip(agents,times))
    values_sort=sorted( values.items(), key=itemgetter(1) )
    print "values_sort",values_sort
    return values_sort

def main():
    from xbaydns.conf import sysconf
    from xbaydnsweb.web.models import IDC,Result,Record,IPArea
    from xbaydns.tools.algorithms2 import *
    
    CONF_FILE='%s/idcview/idcview.current'%sysconf.xbaydnsdb
    
    map(lambda x:x.delete(),Result.objects.all())
    services = getServiceRegions()
    pmatrix = PerformanceMatrix(services)
    for i,r in enumerate(open(CONF_FILE)):
        if i==0:
            agents=r.split(',')
            agents=map(lambda x:x.strip(),agents)
            continue
        r=r.split(',')
        ip,times=r[0],r[1:]
        print ip
        speeds_dict ={}
        for agent,time in zip(agents,times):
            speeds_dict.update({agent:time})
        pmatrix.ip(ip,speeds_dict)
    iparea =pmatrix.partitions()
    for k,v in pmatrix.ips.items():
        Result.objects.create(ip=k,record=v[1],idc=IDC.objects.filter(alias=v[0]))
    for k,v in iparea.items():
        service_route=[]
        for service,idc in zip(services,k.split(',')):
            service_route.append((service,idc))
        IPArea.objects.create(ip=str(list(v)),acl='',view='',service_route=service_route)

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'xbaydnsweb.settings'
    main()

