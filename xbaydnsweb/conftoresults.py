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
from operator import itemgetter

def findFastSpeed(agents,times):
    times=map(lambda x:float(x.strip()),times)
    values=dict(zip(agents,times))
    values_sort=sorted( values.items(), key=itemgetter(1) )
    print "values_sort",values_sort
    return values_sort

def main():
    map(lambda x:x.delete(),Result.objects.all())
    
    for i,r in enumerate(open("/tmp/idcview_out.txt")):
        if i==0:
            agents=r.split(',')
            agents=map(lambda x:x.strip(),agents)
            continue
        r=r.split(',')
        ip,times=r[0],r[1:]
        print ip
        flag={}
        for j,(idc,fasttime) in enumerate(findFastSpeed(agents,times)):
            records=Record.objects.filter(idc__alias=idc)
            if len(records)>0:
                print records
                flagkey='%s.%s'%(records[0].name,records[0].domain)
                print "flagkey",flagkey,flag.get(flagkey,False)
                if flag.get(flagkey,False):
                    print "True:True"
                    continue
            print "XXXXXXXXX"
            for record in records:
                Result.objects.create(ip=ip,record=record,idc=record.idc)
                flagkey='%s.%s'%(record.name,record.domain)
                print "flagkey2",flagkey
                flag[flagkey]=True
    for record in Record.objects.filter(is_defaultidc=True):
        Result.objects.create(ip='any',record=record,idc=record.idc)

if __name__ == '__main__':
    main()

