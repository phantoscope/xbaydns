#!/opt/local/bin/python2.5
# encoding: utf-8
"""
conftoresults.py

Created by QingFeng on 2008-03-26.
Copyright (c) 2008 xBayDNS Team. All rights reserved.
"""

import os,sys
sys.path.append('/Users/yanxu/python/xbaydns/source/trunk/xbaydns')
sys.path.append(os.path.join('/Users/yanxu/python/xbaydns/source/trunk/xbaydnsweb', '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'xbaydnsweb.settings'

from xbaydnsweb.web.models import IDC,Result,Record
from xbaydns.dnsapi import nsupdate
import traceback
from operator import itemgetter

CONF_FILE='/tmp/idcview_out.txt'

def findFastSpeed(agents,times):
    times=map(lambda x:float(x.strip()),times)
    if reduce(lambda x,y:x==y, times):return []
    values=dict(zip(agents,times))
    values_sort=sorted( values.items(), key=itemgetter(1) )
    print "values_sort",values_sort
    return values_sort

def record_nsupdate(record):
    try:
        nsupobj = nsupdate.NSUpdate('127.0.0.1',"%s."%record.domain,view="view_%s"%record.idc.alias)
        #['foo', 3600, 'IN', 'A', ['192.168.1.1', '172.16.1.1']]#record style
        add_data=[[str(record.name),3600,'IN','A',[str(record.ip),]],]
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

def main():
    map(lambda x:x.delete(),Result.objects.all())
    for i,r in enumerate(open(CONF_FILE)):
        if i==0:
            agents=r.split(',')
            agents=map(lambda x:x.strip(),agents)
            continue
        r=r.split(',')
        ip,times=r[0],r[1:]
        print ip
        flag={}
        for idc,fasttime in findFastSpeed(agents,times):
            if fasttime==-1.00:continue
            records=Record.objects.filter(idc__alias=idc)
            print records
            for j,record in enumerate(records):
                print record
                flagkey='%s.%s'%(record.name,record.domain)
                print "flagkey",flagkey,flag.get(flagkey,False),j
                if flagkey in flag:
                    if j!=0:
                        #if record.name!=records[j-1].name or record.domain!=records[j-1].domain:
                        if flag.get(flagkey,'')!=records[j-1].idc:
                            print "True:True"
                            continue
                    elif j==0:
                        if flagkey in flag:
                            print "True:True"
                            continue
                print "GOGO"
                Result.objects.create(ip=ip,record=record,idc=record.idc)
                flag[flagkey]=record.idc
                record_nsupdate(record)
    for record in Record.objects.filter(is_defaultidc=True):
        Result.objects.create(ip='any',record=record,idc=record.idc)
        record_nsupdate(record)

if __name__ == '__main__':
    main()

