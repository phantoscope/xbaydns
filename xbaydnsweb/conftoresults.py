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
    sql='''SELECT web_record.name,web_domain.name,web_idc.alias FROM web_recordtype,web_record,web_domain,web_idc WHERE 
    web_domain.id=web_record.domain_id AND web_idc.id=web_record.idc_id AND web_recordtype.id =web_record.record_type_id AND web_recordtype.record_type ='A' 
    GROUP BY web_record.name,web_domain.name,web_idc.alias'''
    cursor = connection.cursor()
    cursor.execute(sql)
    for r in cursor.fetchall():
        key = '%s.%s'%(r[0],r[1])
        if key in service_reg:
            service_reg[key].append(r[2])
        else:
            service_reg.setdefault(key,[r[2]])
    return service_reg

def getRegions():
    from xbaydnsweb.web.models import IDC
    regions = IDC.objects.all()
    return map(lambda x:x.alias,regions)

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
    from xbaydns.tools.algorithms2 import quicksort,getRoute,PerformanceMatrix
    from types import ListType
    
    CONF_FILE='%s/idcview/idcview.current'%sysconf.xbaydnsdb
    
    map(lambda x:x.delete(),Result.objects.all())
    map(lambda x:x.delete(),IPArea.objects.filter(ip='0'))
    
    for iparea in IPArea.objects.all():
        iparea.ip = '0'
        iparea.save()
    
    services = getServiceRegions()
    regions_alias = getRegions()
    
    print "services: ",str(services)
    pmatrix = PerformanceMatrix(services)
    for i,r in enumerate(open(CONF_FILE)):
        if i==0:
            agents=r.split(',')
            agents=map(lambda x:x.strip(),agents)
            continue
        r=r.split(',')
        ip,times=r[0],r[1:]
        speeds_dict ={}
        for agent,time in zip(agents,times):
            if agent in regions_alias:
                speeds_dict.update({agent:time})
        pmatrix.ip(ip,speeds_dict)
    iparea =pmatrix.partitions()
#    for k,v in pmatrix.ips.items():
#        for d,i in v:
#            Result.objects.create(ip=k,record=i,idc=IDC.objects.filter(alias=d)[0])
    for k,v in iparea.items():
        service_route_list = zip(services,eval(k))
        if services.items() != service_route_list:
            service_route=[]
            for service,idcs in service_route_list:
                if type(idcs) == ListType:
                    for idc in idcs:
                        service_route.append((service,idc))
                else:
                    service_route.append((service,idcs))
            IPArea.objects.create(ip=str(list(v)),acl='',view='',service_route=str(service_route))

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'xbaydnsweb.settings'
    main()

